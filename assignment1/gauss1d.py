# from PIL import Image
import numpy as np
import math
from scipy import signal


# paramenter: Sigma -> dimension of array matrix
# return a numpy array with dimension n

def gauss1d(sigma):
    if sigma > 0:  # check if sigma is greater than 0
        try:

            array_length = int(math.ceil(float(sigma) * 6))

            if (array_length % 2 == 0):
                array_length += 1

            centre = array_length / 2
            # print("Center - ", centre)

            array = np.arange(-centre + 1, centre + 1)

            array = np.floor(array)
            # print("Floor array -  ", array)

            result = np.exp(-1 * (array ** 2) / (2 * sigma ** 2))

            result = result / np.sum(result)
            # print("Normalized result - ", result)

            return result

        except ValueError:
            print("Sigma is a negative ")


# Running function
# gauss1d(0.3)
# gauss1d(0.5)
# gauss1d(1)
# gauss1d(2)
