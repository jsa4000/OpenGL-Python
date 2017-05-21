import numpy as np
import OpenGL.GL as GL

def typeGL(dtype):
    """
        This function will convert the types supported by OpenGL from
        numpy types. 
        If dtype is not founded into the GLtypes the function will
        return GL.GL_FLOAT as default Open GL type
    """
    # Check for some posibilities with the input, np.int32, 'int32','np.int32'
    if isinstance(dtype, (np.dtype)):
        dtype = dtype.name
    elif not isinstance(dtype, (str)):
        dtype = dtype.__name__
    # get the second part in case it can be splitted
    if len(dtype.split(".")) > 1:
        dtype = dtype.split(".")[-1]
    #Check the type of data has to be converted
    datatypes = {
        "int8"     :    GL.GL_BYTE, 			
        "uint8"    :    GL.GL_UNSIGNED_BYTE,	
	    "int16"    :    GL.GL_SHORT,			
	    "uint16"   :    GL.GL_UNSIGNED_SHORT,	
	    "int32"    :    GL.GL_INT,				
	    "uint32"   :    GL.GL_UNSIGNED_INT,		
	    "float16"  :    GL.GL_HALF_FLOAT,		
	    "float32"  :    GL.GL_FLOAT,			
	    "float64"  :    GL.GL_DOUBLE,
        "fixed"    :    GL.GL_FIXED # More compatibility for OS (float32)
    }	
    # Check if the current datatype exists
    if dtype in datatypes:		
        return datatypes[dtype]
    # if the data type does't exit returns default GL type
    return datatypes[np.float32]
