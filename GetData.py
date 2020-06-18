import pandas as pd
import numpy as np

def Dataset():
    data = pd.read_csv("IoTTestData.xls")
    beacons = data.keys()
    beacons = beacons[1:]

    for x in range(len(beacons)):
        data[beacons[x]] = data[beacons[x]].replace(np.nan, -150)

    np_data = data.to_numpy()

    X = np_data[:, 1:]
    y = np_data[:, 0]
    X = X[:5000]
    y = y[:5000]

    return X, y

