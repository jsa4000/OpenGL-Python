import numpy as np

def convert(value, dtype=np.float32):
    return np.around(np.array(value,dtype),4)

