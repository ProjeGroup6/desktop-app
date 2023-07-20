import numpy as np
import time


def writeToFile(filename):
    # write 2d numpy array(0 or 1)seperated by commas to file
    arr = np.random.randint(2, size=(2048, 2048))
    np.savetxt(filename, arr, delimiter=",", fmt="%d")
    print("wrote to file")


while True:
    writeToFile("testmap.txt")
    time.sleep(3)
