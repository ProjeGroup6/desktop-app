import numpy as np
import time


def readFromFile(filename):
    # read file
    data = np.loadtxt(filename, dtype=np.uint8)
    data = np.append(data, np.zeros(2048 * 2048 - data.shape[0], dtype=np.uint8))
    data = data.reshape(2048, 2048)

    print(data)


while True:
    readFromFile("testmap.txt")
    time.sleep(3)
