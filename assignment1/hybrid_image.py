from PIL import Image
import numpy as np
import math
from scipy import signal
from gauss1d import gauss1d
from gauss2d import gauss2d
from gaussconvolve2d import gaussconvolve2d

# Get R,G,B channels
#
# dog_image = Image.open("/Users/gautamsoni/Desktop/CPSC 425/assignment1/hw1/0b_dog.bmp")
# data = dog_image.getdata()
#
# # Suppress specific bands (e.g. (255, 120, 65) -> (0, 120, 0) for g)
# r = [(d[0], 0, 0) for d in data]
# g = [(0, d[1], 0) for d in data]
# b = [(0, 0, d[2]) for d in data]
#
# dog_image.putdata(r)
# dog_image.save('r.png')
# dog_image.putdata(g)
# dog_image.save('g.png')
# dog_image.putdata(b)
# dog_image.save('b.png')

# Part 1

dog_image = Image.open('/Users/gautamsoni/Desktop/CPSC 425/assignment1/hw1/4a_bird.bmp')
dog_image.show()

sigma = 2
r, g, b = dog_image.split()

b_array = np.asarray(b)
g_array = np.asarray(g)
r_array = np.asarray(r)

b_gauss = gaussconvolve2d(b_array, sigma)[:,:,np.newaxis]
g_gauss = gaussconvolve2d(g_array, sigma)[:,:,np.newaxis]
r_gauss = gaussconvolve2d(r_array, sigma)[:,:,np.newaxis]

new_blurr_dog = np.concatenate((r_gauss, g_gauss, b_gauss), axis=2)

blurr_dog_image = Image.fromarray(new_blurr_dog.astype('uint8'))
blurr_dog_image.show()

# Part 2.2

cat_image = Image.open("/Users/gautamsoni/Desktop/CPSC 425/assignment1/hw1/4b_plane.bmp")
cat_image.show()

cat_image_array = np.asarray(cat_image)

r_cat, g_cat, b_cat = cat_image.split()

b_array_cat = np.asarray(b_cat)
g_array_cat = np.asarray(g_cat)
r_array_cat = np.asarray(r_cat)

b_gauss_cat = gaussconvolve2d(b_array_cat, sigma)[:,:,np.newaxis]
g_gauss_cat = gaussconvolve2d(g_array_cat, sigma)[:,:,np.newaxis]
r_gauss_cat = gaussconvolve2d(r_array_cat, sigma)[:,:,np.newaxis]

new_blurr_cat = np.concatenate((r_gauss_cat, g_gauss_cat, b_gauss_cat), axis=2)

new_blurr_cat_image = Image.fromarray(new_blurr_cat.astype('uint8'))
new_blurr_cat_image.show()

high_frequency_cat = np.subtract(cat_image_array,new_blurr_cat)

high_frequency_cat_image = Image.fromarray(high_frequency_cat.astype('uint8') + 128)
high_frequency_cat_image.show()

# Part 2.3

hybrid_image_array = np.add(high_frequency_cat, new_blurr_dog)

hybrid_image = Image.fromarray(hybrid_image_array.astype('uint8'))
hybrid_image.show()
