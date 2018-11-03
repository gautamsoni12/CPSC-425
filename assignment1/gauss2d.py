import numpy as np
import math
from scipy import signal
from gauss1d import gauss1d


def gauss2d(sigma):
    g2d_array = gauss1d(sigma)[np.newaxis]
    #print("G2D array - ", g2d_array)

    g2d_array_transpose = g2d_array.T
    #print("G2D array transpose - ", g2d_array_transpose)

    result = signal.convolve2d(g2d_array, g2d_array_transpose)
    #print("Result - ", result)

    return result


# Running function
gauss2d(0.5)

gauss2d(1)
