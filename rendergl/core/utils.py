import numpy as np

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

