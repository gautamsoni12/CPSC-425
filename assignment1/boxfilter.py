#from PIL import Image
import numpy as np
import math
from conda import exceptions
from scipy import signal

# paramenter: n -> dimension of array matrix
# return a numpy array with dimension n
def boxfilter(n):   
    if n % 2 == 1:            # check if n is odd
        try:
            a = np.ones((n,n))
            b = np.size(a)
            return a / b


        except ValueError:
            print("Assertion Error: Dimensions must be odd")

    else:
         raise exceptions.ArgumentError("Dimensions must be odd")


# Running box filter
print(boxfilter(3))
print(boxfilter(4))
print(boxfilter(5))
