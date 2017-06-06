from collections import OrderedDict as dict
from enum import Enum
import os
import json
import numpy as np
from PIL import Image


__all__ = ['file_exists', 
           'read_json',
           'read_file',
           'load_image', 
           'is_collection',
           'empty', 
           'normalize',
           'length', 
           'round',
           'nparray', 
           'ParseDict', 
           'get_cmd_parameters',
           'BasicCounter',
           'EnumBase',
           'ProgressBar',
           'timeit']

def file_exists(filename):
    """
        Check if file exists
    """
    if os.path.isfile(filename):
        return True
    return False

def read_json(filename, strict=False):
    """ Loads a JSON file
    """
    data = []
    with open(filename,'r') as file:
        data = json.load(file,strict=False)
    return data

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
    if isinstance(value, (np.ndarray)):
        if value.size > 1:
             return False
    elif isinstance(value, (list, dict, tuple, set)):
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
    def __init__(self, args=None, **kwargs):
        """Constructor
        """
        if args:
            for key in args:
                setattr(self, key, args[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
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

class BasicCounter(object):
    def __init__(self, default):
        self._counter = default
    def __call__(self):
        self._counter += 1
        return self._counter

class EnumBase(Enum):
    def __eq__(self, item):
        if isinstance(item, (Enum)):
            return self.value == item.value
        return self.value == item

import time

class ProgressBar:
    """
        Progress bar to show the progress in the terminal.
        Following as example of how to use:
            with ProgressBar(filesize) as pbar:
                for i in range(10):
                    pbar.update(1)
                    time.sleep(1)
    """
    def __init__(self, title, total, start=0, units="%", size=30):
        self.title = title
        self.total = total
        self.units = units
        self.current = start
        self.size = size
    def __enter__(self):
        # This must return itslf for With statemets
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        percent =  100
        print( self.title + " " + self.get_progress_bar(1) + " 100.0"+ self.units + " DONE!         ")
    def get_progress_bar(self, percent):
        return "[" + ("#" * int(percent * self.size)) + (" " * (self.size -  int(percent * self.size))) + "]"
    def update(self, amount):
        self.current += amount
        percent =  self.current / self.total
        print( self.title + " " + self.get_progress_bar(percent) + " " +"{0:.1f}".format(round(percent * 100,2)) + self.units, end="\r")
     
def timeit(method, showparams = False):
    """
        Define an inner function that invoke the method and measure the
        time that takes to run it.
    """
    def inner(*args, **kw):
        """
            This function will compute the time that takes to invoke
            the function passed by parameters.
            This function will return the same result as the function.
        """
        tstart = time.time()
        result = method(*args, **kw)
        tend = time.time()
        #Print the total amount of time consuming for the curent call
        if (showparams):
            print(('Time: %r (%r, %r) %2.8f sec') % (method.__name__, args, kw, tend-tstart))
        else:
            print(('Time: %r %2.8f sec') % (method.__name__, tend-tstart))
        return result
    # Compute the timing and return the same values of the function
    return inner

