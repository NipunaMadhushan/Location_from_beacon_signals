import paho.mqtt.client as mqtt
import json
import numpy as np
import pandas as pd
import cv2 as cv
from New.TrainModel import test_model, predict_location, linear_train_model, logistic_train_model, svm_train_model, \
    rf_train_model


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("IoT_Project")


def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("Message: ", msg)
    data = get_data(msg)
    pred = predict_location(classifier, data)
    print("Current Location: ", pred)
    map_location(pred)


def get_data(msg):
    data = {"f0:ec:af:cf:6c:e1": -150, "c9:a6:4d:9b:c0:8c": -150, "c2:b6:6e:70:fa:f7": -150,
              "d9:5f:f5:4f:10:89": -150, "c4:52:32:5c:31:e7": -150, "e9:3c:4a:34:13:fb": -150,
              "ed:61:e4:e8:22:30": -150, "ea:01:26:75:a4:c3": -150, "d0:4e:10:2e:cb:84": -150,
              "e4:e0:0a:ae:fd:e2": -150, "fa:35:76:56:6f:e3": -150, "d5:b7:dc:69:ca:ae": -150,
              "ca:81:7a:d7:55:49": -150, "e7:2b:ea:2f:95:c5": -150, "d4:32:fc:b5:f0:b5": -150}
    all_beacons = list(data.keys())

    msg_json = json.loads(msg)
    beacons = list(msg_json.keys())
    for x in beacons:
        data[x] = msg_json[x]

    data_list = []
    for y in all_beacons:
        data_list.append(data[y])

    return data_list


def map_location(prediction):
    map = cv.imread("map.jpeg")
    locations = [(275, 215), (75, 240), (135, 300), (208, 270), (355, 270), (420, 390), (320, 335), (535, 215),
                 (520, 275), (410, 260), (430, 215), (580, 180), (200, 230), (440, 360), (250, 255), (395, 290),
                 (320, 240), (360, 340), (380, 390), (250, 320), (410, 330), (480, 190), (460, 260)]
    cv.circle(map, locations[prediction-1], 10, (0, 0, 255), thickness=5)
    cv.imshow("Location", map)
    cv.waitKey()
    cv.destroyAllWindows()


# Train the model
classifier = rf_train_model()
test_model(classifier)

# Subscribe to topic
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipse.org", 1883, 60)
client.loop_forever()
