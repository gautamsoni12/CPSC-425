from PIL import Image, ImageDraw
import numpy as np
import random
import os.path
import pickle



##############################################################################
#                        Functions for you to complete                       #
##############################################################################

def ComputeSSD(TODOPatch, TODOMask, textureIm, patchL):
    patch_rows, patch_cols, patch_bands = np.shape(TODOPatch)
    # print(patch_rows, patch_cols, patch_bands)
    # print(patchL)
    # print(TODOMask.shape)

    textureIm = textureIm * 1.0         # Change elements of textureIm to floating point
    TODOPatch = TODOPatch * 1.0         # Change elements of textureIm to floating point

    tex_rows, tex_cols, tex_bands = np.shape(textureIm)

    ssd_rows = tex_rows - 2 * patchL
    ssd_cols = tex_cols - 2 * patchL
    SSD = np.zeros((ssd_rows, ssd_cols))

    for r in range(ssd_rows):
        for c in range(ssd_cols):
            for x in range(patch_rows):                         # for each pixel in patch_rows
                for y in range (patch_cols):                    # for each pixel in patch_cols
                    if TODOMask[x][y] == 0:                     # if TODOMask at x & y coordinates is not empty
                        for d in range(patch_bands):            # for each of the RGB channels
                            # Compute SSD at each r & c by finding the difference between Texture Image and Patch for
                            #  each RGB channel and squaring it.
                            SSD[r][c] += ((textureIm[r][c][d] - TODOPatch[x][y][d])**2)

    return SSD


def CopyPatch(imHole, TODOMask, textureIm, iPatchCenter, jPatchCenter, iMatchCenter, jMatchCenter, patchL):

    patchSize = 2 * patchL + 1

    # print(empty_pixels)
    # print(patchSize)
    a,b,c = np.shape(textureIm)

    for i in range(patchSize):
        for j in range(patchSize):
            if TODOMask[i][j] == 1:                     # Check if TODOMask if empty at i and j coordinates
                iHole = i + (iPatchCenter - patchL)     # Compute i point of hole
                jHole = j + (jPatchCenter - patchL)     # Compute j point of hole

                iImage = i + (iMatchCenter - patchL)    # Compute i point of image
                jImage = j + (jMatchCenter - patchL)    # Compute i point of image

                for d in range(c):
                    # For each channel in RGB, equate the hole in image to the texture image.
                    imHole[int(iHole)][int(jHole)][d] = textureIm[int(iImage)][int(jImage)][d]

    return imHole


##############################################################################
#                            Some helper functions                           #
##############################################################################

def DrawBox(im, x1, y1, x2, y2):
    draw = ImageDraw.Draw(im)
    draw.line((x1, y1, x1, y2), fill="white", width=1)
    draw.line((x1, y1, x2, y1), fill="white", width=1)
    draw.line((x2, y2, x1, y2), fill="white", width=1)
    draw.line((x2, y2, x2, y1), fill="white", width=1)
    del draw
    return im


def Find_Edge(hole_mask):
    [cols, rows] = np.shape(hole_mask)
    edge_mask = np.zeros(np.shape(hole_mask))
    for y in range(rows):
        for x in range(cols):
            if (hole_mask[x, y] == 1):
                if (hole_mask[x - 1, y] == 0 or
                        hole_mask[x + 1, y] == 0 or
                        hole_mask[x, y - 1] == 0 or
                        hole_mask[x, y + 1] == 0):
                    edge_mask[x, y] = 1
    return edge_mask


##############################################################################
#                           Main script starts here                          #
##############################################################################

#
# Constants
#

# Change patchL to change the patch size used (patch size is 2 *patchL + 1)
patchL = 10
patchSize = 2 * patchL + 1

# Standard deviation for random patch selection
randomPatchSD = 1

# Display results interactively
showResults = True

#
# Read input image
#

im = Image.open('apple.png').convert('RGB')
im_array = np.asarray(im, dtype=np.uint8)
imRows, imCols, imBands = np.shape(im_array)

#
# Define hole and texture regions.  This will use files fill_region.pkl and
#   texture_region.pkl, if both exist, otherwise user has to select the regions.
if os.path.isfile('fill_region.pkl') and os.path.isfile('texture_region.pkl'):
    fill_region_file = open('fill_region.pkl', 'rb')
    fillRegion = pickle.load(fill_region_file)
    fill_region_file.close()

    texture_region_file = open('texture_region.pkl', 'rb')
    textureRegion = pickle.load(texture_region_file)
    texture_region_file.close()
else:
    # ask the user to define the regions
    print("Specify the fill and texture regions using polyselect.py")
    exit()

#
# Get coordinates for hole and texture regions
#

fill_indices = fillRegion.nonzero()
nFill = len(fill_indices[0])  # number of pixels to be filled
iFillMax = max(fill_indices[0])
iFillMin = min(fill_indices[0])
jFillMax = max(fill_indices[1])
jFillMin = min(fill_indices[1])
assert ((iFillMin >= patchL) and
        (iFillMax < imRows - patchL) and
        (jFillMin >= patchL) and
        (jFillMax < imCols - patchL)), "Hole is too close to edge of image for this patch size"

texture_indices = textureRegion.nonzero()
iTextureMax = max(texture_indices[0])
iTextureMin = min(texture_indices[0])
jTextureMax = max(texture_indices[1])
jTextureMin = min(texture_indices[1])
textureIm = im_array[iTextureMin:iTextureMax + 1, jTextureMin:jTextureMax + 1, :]
texImRows, texImCols, texImBands = np.shape(textureIm)
assert ((texImRows > patchSize) and
        (texImCols > patchSize)), "Texture image is smaller than patch size"

#
# Initialize imHole for texture synthesis (i.e., set fill pixels to 0)
#

imHole = im_array.copy()
imHole[fill_indices] = 0

#
# Is the user happy with fillRegion and textureIm?
#
if showResults == True:
    # original
    im.show()
    # convert to a PIL image, show fillRegion and draw a box around textureIm
    im1 = Image.fromarray(imHole).convert('RGB')
    im1 = DrawBox(im1, jTextureMin, iTextureMin, jTextureMax, iTextureMax)
    im1.show()
    print("Are you happy with this choice of fillRegion and textureIm?")
    Yes_or_No = False
    while not Yes_or_No:
        answer = "Yes" # input("Yes or No: ")
        if answer == "Yes" or answer == "No":
            Yes_or_No = True
    assert answer == "Yes", "You must be happy. Please try again."

#
# Perform the hole filling
#

while (nFill > 0):
    print("Number of pixels remaining = ", nFill)

    # Set TODORegion to pixels on the boundary of the current fillRegion
    TODORegion = Find_Edge(fillRegion)
    edge_pixels = TODORegion.nonzero()
    nTODO = len(edge_pixels[0])

    while (nTODO > 0):
        # Pick a random pixel from the TODORegion
        index = np.random.randint(0, nTODO)
        iPatchCenter = edge_pixels[0][index]
        jPatchCenter = edge_pixels[1][index]

        # Define the coordinates for the TODOPatch
        TODOPatch = imHole[iPatchCenter - patchL:iPatchCenter + patchL + 1,
                    jPatchCenter - patchL:jPatchCenter + patchL + 1, :]
        TODOMask = fillRegion[iPatchCenter - patchL:iPatchCenter + patchL + 1,
                   jPatchCenter - patchL:jPatchCenter + patchL + 1]

        #
        # Compute masked SSD of TODOPatch and textureIm
        #
        ssdIm = ComputeSSD(TODOPatch, TODOMask, textureIm, patchL)

        # Randomized selection of one of the best texture patches
        ssdIm1 = np.sort(np.copy(ssdIm), axis=None)
        ssdValue = ssdIm1[min(round(abs(random.gauss(0, randomPatchSD))), np.size(ssdIm1) - 1)]
        ssdIndex = np.nonzero(ssdIm == ssdValue)
        iSelectCenter = ssdIndex[0][0]
        jSelectCenter = ssdIndex[1][0]

        # adjust i, j coordinates relative to textureIm
        iSelectCenter = iSelectCenter + patchL
        jSelectCenter = jSelectCenter + patchL
        selectPatch = textureIm[iSelectCenter - patchL:iSelectCenter + patchL + 1,
                      jSelectCenter - patchL:jSelectCenter + patchL + 1, :]

        #
        # Copy patch into hole
        #
        imHole = CopyPatch(imHole, TODOMask, textureIm, iPatchCenter, jPatchCenter, iSelectCenter, jSelectCenter,
                           patchL)

        # Update TODORegion and fillRegion by removing locations that overlapped the patch
        TODORegion[iPatchCenter - patchL:iPatchCenter + patchL + 1, jPatchCenter - patchL:jPatchCenter + patchL + 1] = 0
        fillRegion[iPatchCenter - patchL:iPatchCenter + patchL + 1, jPatchCenter - patchL:jPatchCenter + patchL + 1] = 0

        edge_pixels = TODORegion.nonzero()
        nTODO = len(edge_pixels[0])

    fill_indices = fillRegion.nonzero()
    nFill = len(fill_indices[0])

#
# Output results
#
if showResults == True:
    Image.fromarray(imHole).convert('RGB').show()

Image.fromarray(imHole).convert('RGB').save('results.jpg')
