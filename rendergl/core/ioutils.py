import os
import numpy as np
from PIL import Image

def isfile(filename):
    """
        Check if file exists
    """
    if os.path.isfile(filename):
        return True
    return False

def readfile(filename):
    """
        Read the current file entirely and return a 
        string variable with all the content with
        special characters like new_line, etc..
    """
    result = None
    if isfile(filename):
        with open(filename,'r') as file:
            result = file.read()
    return result


def load_image(filename, bpp=8):
    #Load the image using the path configured
    image = Image.open(filename).transpose(Image.FLIP_TOP_BOTTOM)
    if (bpp == 32):
        dtype = np.uint32
    elif (bpp == 16):
        dtype = np.uint16
    else:
        dtype = np.uint8
    # Convert the image to a numpy string. Converto to uint8 image.
    image_data = np.array(image.getdata(), dtype)
    return [image_data, image.size]