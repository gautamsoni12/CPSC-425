from PIL import Image
import numpy as np

im = Image.open('peacock.png')

print im.size, im.mode, im.format

im.show()

im = im.convert('L')

im2 = im.crop((475,130,575,230))

im2.save('peacock_head.png','PNG')

im2_array = np.asarray(im2)

average = np.mean(im2_array)

im3_array = im2_array.copy()

for x in range(0,100):
    for y in range(0,100):
        im3_array[y,x] = min(im3_array[y,x] + 50,255)

im3 = Image.fromarray(im3_array)
im3.save('peacock_head_bright.png', 'PNG')

im4_array = im2_array.copy()

im4_array = im4_array *0.5

im4_array = im4_array.astype('uint8')

im4 = Image.fromarray(im4_array)
im4.save('peacock_head_dark.png', 'PNG')

grad = np.arange(0,256)

grad = np.tile(grad,[256,1])

im5 = Image.fromarray(grad.astype('uint8'))
im5.save('gradient.png','PNG')
                      
