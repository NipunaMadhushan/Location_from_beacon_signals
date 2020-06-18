#include <BLEDevice.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <Arduino_JSON.h>
#include <WiFi.h>
#include <PubSubClient.h>

#define WIFI_SSID "Nipuna4G"
#define WIFI_PASSWORD "Kanthi1961"
const char* mqtt_server = "mqtt.eclipse.org";
const int mqttPort = 1883;

int device_count = 0;

BLEScan* pBLEScan;

WiFiClient espClient;
PubSubClient client(espClient);

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
    }
};


void setup() {
  Serial.begin(115200);
}

String readData(){

  Serial.println("Scanning for iBeacons...");
  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true);
//  pBLEScan->setInterval(100);
//  pBLEScan->setWindow(99);
  
  BLEScanResults foundDevices = pBLEScan->start(3, false);

  device_count = foundDevices.getCount();
  Serial.printf("Device Count: %d\n", device_count);

  JSONVar data_r;
  data_r["id"] = "22";
  
  for (uint32_t i = 0; i < device_count; i++)
  {
    
    BLEAdvertisedDevice device = foundDevices.getDevice(i);
    
    int RSSI_data = (int)device.getRSSI();
    String MAC_address = (String)device.getAddress().toString().c_str();

    Serial.printf("RSSI =  %d --- ", RSSI_data);
    Serial.printf("MAC Address =  %s", MAC_address);
    Serial.println();

    //setting json values
   
    data_r[MAC_address] = RSSI_data;
    
    delay(500);
    
  }

  String jsonString = JSON.stringify(data_r);
  return(jsonString);
}

void connectWiFi(){

  Serial.print("Connecting to Wi-Fi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED)
  {
      Serial.print(".");
      delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();
 
}

void reconnect_mqtt(const char* JSONmessage) {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    //String clientId = "ESP32Client-";
    //clientId += String(random(0xffff), HEX);
    String clientId = "ESP32Client-Nipuna";
   
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
  
      Serial.println("connected");
  
      if (client.publish("SAN", JSONmessage)) {
        Serial.println("Success sending message");
        Serial.println(JSONmessage);
      } else {
        Serial.println("Error sending message");
      }
      client.loop();
      Serial.println("-------------");
   
  
    } else {
  
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
   
    }
  }
}

  
void loop() {

  connectWiFi();
  client.setServer(mqtt_server, 1883);
  
  String JSONmessage = readData();

  reconnect_mqtt(JSONmessage.c_str());
  
  Serial.println("iBeacon Scan done!");
  pBLEScan->clearResults();   // delete results fromBLEScan buffer to release memory
  Serial.println("......................................................");
  delay(100);

}
