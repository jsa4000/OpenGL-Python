from collections import OrderedDict as dict
import os
import numpy as np
from PIL import Image

__all__ = ['file_exists', 
           'read_file',
           'load_image', 
           'is_collection',
           'empty', 
           'normalize',
           'length', 
           'round',
           'nparray', 
           'ParseDict', 
           'get_cmd_parameters']

def file_exists(filename):
    """
        Check if file exists
    """
    if os.path.isfile(filename):
        return True
    return False

def read_file(filename):
    """
        Read the current file entirely and return a 
        string variable with all the content with
        special characters like new_line, etc..
    """
    result = None
    if file_exists(filename):
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

def is_collection(value):
    """ Function that check whether the value is a collection type
    or a single value, like an object or basic types like int, str..
    """
    collection_types =  (list, dict, np.ndarray, tuple, set)
    if isinstance(value,collection_types):
        return True
    return False
        

def empty(value):
    """
        Ths function will return is some list or variable is empty.
        For list, dict or any other collection will check there is 
        more that one element. For other variables the condition
        will check if the object is None.
    """    
    if isinstance(value, (list, dict, np.ndarray, tuple, set)):
        if len(value) > 0:
            return False
    else:
        if value is not None:
            return False
    return True

def normalize(value):
    """Normalize the value passed by parameteres
    It can be vectors, arrays, matrices, etc...
    """
    return np.around(value/np.linalg.norm(value),5)

def length(value):
    """ Return the magnitude of a vector (A - B)
    """
    return np.linalg.norm(value)

def round(alue, decimals=3):
    """Round a float or array elements using decimals count
    """
    return np.around(value,decimals)

def nparray(value, dtype=np.float32):
    """ Convert the curren value or array of elements into 
    the specified datatype
    """
    return np.array(value,dtype)

class ParseDict(object):
    """ Parse a dictionary a convert it into a class
    """
    def __init__(self, dictionary):
        """Constructor
        """
        for key in dictionary:
            setattr(self, key, dictionary[key])
    def __repr__(self):
        """"""
        return "<ParseDict: {}>".format(self.__dict__)

def get_cmd_parameters(args, parameters):
    """ Function to load the parameters using cmd. >>> sys.argv
    
        If parameters are not found (options) the it will use (default) values
        It will return a object with the elements in paramters:
        
        parameters = {"width"  : {"options" : ["width","W"]  , "default": 800 },
                     "height" : {"options" : ["height","H"] , "default": 600 },
                     "fps"    : {"options" : ["fps","F"]    , "default": 60 }}

        Output: 
            <ParseDict: {'fps': '60', 'width': '800', 'height': '600'}>
    """
    # Dictionar yo be filled
    result = dict()
    # First set default parameters
    for params in parameters:
        # Set default value if not found
        if "default" in  parameters[params]:
            result[params] = parameters[params]["default"]
    # Itereate trhrough the parameters (step by two)
    for index in range(1, len(args), 2):
        # Search for this param into the loop
        for params in parameters:
            for option in parameters[params]["options"]:
                if option in args[index]:
                    #print ("{}:{}".format(params,args[index + 1] ))
                    result[params] = args[index + 1]
                    break
    # Return the parameters read or default
    return ParseDict(result)

