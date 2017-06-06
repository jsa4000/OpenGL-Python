import numpy as np
import OpenGL.GL as GL
from ...core import UsageMode, DrawMode

opengl_usagemode_wrapper = {
    UsageMode.stream_draw  : GL.GL_STREAM_DRAW,
    UsageMode.stream_read  : GL.GL_STREAM_READ,
    UsageMode.stream_copy  : GL.GL_STREAM_COPY,
    UsageMode.static_draw  : GL.GL_STATIC_DRAW,
    UsageMode.static_read  : GL.GL_STATIC_READ,
    UsageMode.static_copy  : GL.GL_STATIC_COPY,
    UsageMode.dynamic_draw : GL.GL_DYNAMIC_DRAW,
    UsageMode.dynamic_read : GL.GL_DYNAMIC_READ,
    UsageMode.dynamic_copy : GL.GL_DYNAMIC_COPY 
}

opengl_drawmode_wrapper = {
    DrawMode.triangles    : GL.GL_TRIANGLES,
    DrawMode.points       : GL.GL_POINTS,
    DrawMode.lines        : GL.GL_LINES, 
    DrawMode.quads        : GL.GL_QUADS,
    DrawMode.tfan         : GL.GL_TRIANGLE_FAN,
    DrawMode.lstrip       : GL.GL_LINE_STRIP,
    DrawMode. tstrip      : GL.GL_TRIANGLE_STRIP,
}

def gldtype(dtype):
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


