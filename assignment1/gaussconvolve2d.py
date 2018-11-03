from PIL import Image
import numpy as np
import math
from scipy import signal
from gauss1d import gauss1d
from gauss2d import gauss2d


def gaussconvolve2d(array, sigma):
    if sigma > 0:
        try:
            gauss2d_filter = gauss2d(sigma)

            convolve_array = signal.convolve2d(array, gauss2d_filter, 'same')

            # dog_image = Image.open('/dog.jpg')
            # dog_image.show()

            # print("test -", list(np.asarray(dog_image)))

            return convolve_array


        except ValueError:
            print("Sigma is negative")


# calling functions

dog_image = Image.open('/Users/gautamsoni/Desktop/CPSC 425/assignment1/dog.jpg')
dog_image.show()
dog_image_grey = dog_image.convert("L")
dog_image_array = np.asarray(dog_image_grey)
# gaussconvolve2d(dog_image_array, 7)

gauss_dog = gaussconvolve2d(dog_image_array, 7)

new_dog = Image.fromarray(gauss_dog.astype('uint8'))
new_dog.save('/Users/gautamsoni/Desktop/CPSC 425/assignment1/new_dog_coloured.jpg')
new_dog.show()

r, g, b = dog_image.split()

b_array = np.asarray(b)
g_array = np.asarray(g)
r_array = np.asarray(r)

b_gauss = gaussconvolve2d(b_array, 7)[:,:,np.newaxis]
g_gauss = gaussconvolve2d(g_array, 7)[:,:,np.newaxis]
r_gauss = gaussconvolve2d(r_array, 7)[:,:,np.newaxis]

print(b_gauss.shape)
print(g_gauss.shape)
print(r_gauss.shape)

new_blurr_dog = np.concatenate((r_gauss, g_gauss, b_gauss), axis=2)

print(new_blurr_dog.shape)

blurr_dog_image = Image.fromarray(new_blurr_dog.astype('uint8'))
blurr_dog_image.show()
