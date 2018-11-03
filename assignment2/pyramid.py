from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import ncc
from PIL import ImageFilter


def MakePyramid(image, minsize):
    pyramid_array = []
    # print(pyramid_array)

    resize_factor = 0.75  # Set teh resize factor rate
    pyramid_array.append(image)  # initialize pyramid array with original image
    pyramid_image = image

    # generate smaller versions of image until a dimension of image is <= the minsize

    while (pyramid_image.size[0] > minsize) & (pyramid_image.size[1] > minsize):
        x, y = pyramid_image.size
        pyramid_image = pyramid_image.resize((int(x * resize_factor), int(y * resize_factor)), Image.BICUBIC)
        pyramid_image.filter(ImageFilter.BLUR)
        #print(pyramid_image.size)
        # pyramid_image.show()

        pyramid_array.append(pyramid_image)  # add each of the smaller image to the array

    return pyramid_array  # return the pyramid array


def ShowPyramid(pyramid):
    width = 1500  # Width of blank image
    height = 1000  # height of blank image
    w = pyramid[0].size[0]  # width of original image
    h = 0  # set h = 0

    blank_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # create a white blank space
    # blank_image.show()

    # for each image in pyramid array, paste each of the image on blank white image to create a pyramid

    for i in range(0, len(pyramid) - 1):
        if i == 0:
            blank_image.paste(pyramid[i], (0, 0))

        else:

            blank_image.paste(pyramid[i], (w, h))
            h = h + pyramid[i].size[1]

#     blank_image.show()
#
#
# im= Image.open("/Users/gautamsoni/Desktop/CPSC 425/hw2/faces/judybats.jpg")
# ShowPyramid(MakePyramid(im, 50))


def FindTemplate(pyramid, template, threshold):

    template_width = 20     #set template width

    np.seterr(divide='ignore', invalid='ignore')
    new_template_width = template_width
    # print("template.width ->",template.width)
    # print("template_width->", template_width)
    new_template_height = (template_width / template.width) * template.height   #set new template height proportional to the change in the width

    # resize the template
    template = template.resize((int(new_template_width), int(new_template_height)), Image.BICUBIC)

    output_image = pyramid[0]       # set output image as the original image
    output_image = output_image.convert('RGB')  # convert the output image ot RGB

    for index, im in enumerate(pyramid):
        nccImage = ncc.normxcorr2D(im, template)     # Get the normalized correlation of the template onto the image
        rectangle_width = new_template_width #* (0.75 ** index)  # Update template rectangle size
        rectangle_height = new_template_height #* (0.75 ** index)    # Update template rectangle size
        for row in range(nccImage.shape[0]):
            for col in range(nccImage.shape[1]):
                if nccImage[row][col] > threshold:            #compare each pixel to the threshold
                    scaledBackCol = col * ((1 / 0.75) ** index) #scale the column
                    scaledBackRow = row * ((1 / 0.75) ** index) #scale the row
                    draw = ImageDraw.Draw(output_image)
                    draw.rectangle([scaledBackCol - rectangle_width , scaledBackRow - rectangle_height,
                                    scaledBackCol + rectangle_width ,
                                    scaledBackRow + rectangle_height ], fill=None, outline="red")
                    del draw

    output_image.show()


threshold = 0.525

minsize = 50

# Fan IMAGE
fan_image = Image.open("/Users/gautamsoni/Desktop/CPSC 425/hw2/faces/fans.jpg")
pyramid = MakePyramid(fan_image, minsize)
ShowPyramid(pyramid)
template = Image.open("/Users/gautamsoni/Desktop/CPSC 425/hw2/faces/template.jpg")
FindTemplate(pyramid, template, threshold)

# Family Image
fan_image = Image.open("/Users/gautamsoni/Desktop/CPSC 425/hw2/faces/family.jpg")
pyramid = MakePyramid(fan_image, minsize)
ShowPyramid(pyramid)
template = Image.open("/Users/gautamsoni/Desktop/CPSC 425/hw2/faces/template.jpg")
FindTemplate(pyramid, template, threshold)

# JudyBats
fan_image = Image.open("/Users/gautamsoni/Desktop/CPSC 425/hw2/faces/judybats.jpg")
pyramid = MakePyramid(fan_image, minsize)
ShowPyramid(pyramid)
template = Image.open("/Users/gautamsoni/Desktop/CPSC 425/hw2/faces/template.jpg")
FindTemplate(pyramid, template, threshold)

# Students
fan_image = Image.open("/Users/gautamsoni/Desktop/CPSC 425/hw2/faces/students.jpg")
pyramid = MakePyramid(fan_image, minsize)
ShowPyramid(pyramid)
template = Image.open("/Users/gautamsoni/Desktop/CPSC 425/hw2/faces/template.jpg")
FindTemplate(pyramid, template, threshold)

# Tree
fan_image = Image.open("/Users/gautamsoni/Desktop/CPSC 425/hw2/faces/tree.jpg")
pyramid = MakePyramid(fan_image, minsize)
ShowPyramid(pyramid)
template = Image.open("/Users/gautamsoni/Desktop/CPSC 425/hw2/faces/template.jpg")
FindTemplate(pyramid, template, threshold)

# Sports
fan_image = Image.open("/Users/gautamsoni/Desktop/CPSC 425/hw2/faces/sports.jpg")
pyramid = MakePyramid(fan_image, minsize)
ShowPyramid(pyramid)
template = Image.open("/Users/gautamsoni/Desktop/CPSC 425/hw2/faces/template.jpg")
FindTemplate(pyramid, template, threshold)
