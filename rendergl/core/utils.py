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

