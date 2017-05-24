import ctypes
import numpy as np
import pandas as pd
import OpenGL.GL as GL
from ..core.transform import Transform
from ..core.utils import *


class DrawMode:
    triangles    = GL.GL_TRIANGLES	
    points       = GL.GL_POINTS
    lines        = GL.GL_LINES 
    quads        = GL.GL_QUADS
    tfan         = GL.GL_TRIANGLE_FAN
    lstrip       = GL.GL_LINE_STRIP
    tstrip       = GL.GL_TRIANGLE_STRIP

class UsageMode:
    stream_draw  = GL.GL_STREAM_DRAW
    stream_read  = GL.GL_STREAM_READ
    stream_copy  = GL.GL_STREAM_COPY
    static_draw  = GL.GL_STATIC_DRAW
    static_read  = GL.GL_STATIC_READ
    static_copy  = GL.GL_STATIC_COPY
    dynamic_draw = GL.GL_DYNAMIC_DRAW
    dynamic_read = GL.GL_DYNAMIC_READ
    dynamic_copy = GL.GL_DYNAMIC_COPY 

class Geometry:
    """
        This element will create and store all the elements needed
        to Render a Geometrt
    """

    # Declare the subindex that will be used for multiple (vector) attribites
    index_cols = ["x","y","z","w"]
    #Defaule type that will be used for indexing using OpenGL elements array buffer
    index_type = np.uint32

    def __init__(self, name=None, shader=None, mode=DrawMode.triangles, usage=UsageMode.static_draw):
        # Initialize all the variables
        self.name = name
        self.shader = shader
        self.mode = mode
        self.usage = usage
        # Create new properties
        self.transform = Transform()
        # Attributes dictionary to store the columns for each component
        self._pointAttribCols = {}
        self._primAttribCols = {}
        # Point Attributes and elements Data frames
        self._dfPoints = pd.DataFrame()
        self._dfPrims = pd.DataFrame()
        # Vertex Array Object for all the Attributtes, elements, etc.
        self._VAO = None
        # Vertex Arrays Buffers for all the Attributes
        self._VAB = {}
        # Element Array Buffers for all the Attrbiutes
        self._EAB = None

        # Initiali<e variables and Window
        self._initialize()

    def __enter__(self):
        # Enter will always return the object itself. Use with With expressons
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean all the memery stored
        self._dispose()

    def _dispose(self):
        # Dispose all the objects and memory allocated
        GL.glDeleteVertexArrays(1,self._VAO)

    def _has_indices(self):
        if "Id" in self._primAttribCols:
            return True
        return False

    def _create_vertex_buffer_array(self, name, attribute_name = None):
        """
            This function only make sense to do when working with
            points (vertex) attributes.S
            The function  will return the bind attribute attached
            to the shader. This could be stored into a list to 
            detach later when copy all the buffers and after unbind
            VAO object.
        """
        # Check if not attribute name has been mapped for the bidinng
        if attribute_name is None:
            attribute_name = name
        # Get the current vertices (flatten is not needed)
        vertices = self._dfPoints[self._pointAttribCols[name]].values
        # Create the vertex array buffer and send the positions into the GPU buffers
        self._VAB[name] = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._VAB[name] )
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, self.usage)

        # Bind Attribute to the current shader. 
        return self.shader.bind(attribute_name, len(vertices[0]), vertices.dtype)

    def _copy_to_buffer(self):
        # Bind the shaders attributes for the current geometry
        if self.shader is None:
            print("ERROR: No shader specified")
      
        # Create a list with the attributes created and binded
        shader_attributes = []

        # Create a new VAO (Vertex Array Object). Only (1) VAO.
        #   Note. Using bpp > 16bits doesn't work. This depend on the Graphic Card.
        self._VAO = GL.glGenVertexArrays(1)
        # Every time we want to use VAO we just have to bind it
        GL.glBindVertexArray(self._VAO)

        # Create the first attribute "position" (location = 0) (Mandatory)
        shader_attributes.append(self._create_vertex_buffer_array("P","position"))
        
        # Check wether the geometry has indexes
        if self._has_indices():
            # Get the current indices (flatten)
            indices = self._dfPrims[self._primAttribCols["Id"]].values
            # Create the element array buffer and send the positions into the GPU buffers
            self._EAB = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER,  self._EAB);
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, self.usage);
        
        # Create and bind other Attributes
        for attrib in self._pointAttribCols.keys():
            if attrib != "P":
                shader_attributes.append(self._create_vertex_buffer_array(attrib))

        # Unbind VAO from OpenGL. Set to None = 0
        GL.glBindVertexArray(0)
        # Remove and unbind buffers
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        # Unbind all the Attributes "position" + Additionals
        for attribute in shader_attributes:
            self.shader.unbind(attribute)

    def _initialize(self):
        pass
        
    def update(self):
        # Depenging on the method to update the vertices using GPU or 
        # inmediate OpenGL the update will be different.
        self._copy_to_buffer()
    
    def _createAttribute(self, df, name, size=3, values=None, default=None, dtype=None):
        #Check the data type if any
        if dtype is None:
            if empty(values):
                # Assign a default value
                dtype = np.float32
            else:
                # Get the type from the values
                if not isinstance(values,(np.ndarray)):
                    # If not numpy then get the numppy array 
                    values = np.array(values)
                #Finally get the type from the numpy array
                dtype = values.dtype 
        # Check any values or default values has been provided
        if empty(values) and empty(default):
            if df.empty:
                # If nothing to add exit the function
                return None
            else:
                # Create a default value (float)
                default = np.zeros((size), dtype=dtype)
        # Check the index value depending on the size
        if size > 1:
            columns = [name + Geometry.index_cols[i] for i in range(size)]
        else:
            columns = [name]
        # Check if values has been already defined
        if (empty(values) and not df.empty):
            # create an array with the same number of rows as the current
            values = np.tile(default,(len(df.index)))
        # Reshape the values [ Maybe should be normalized and flatten]
        values = np.array(np.reshape(values, (-1, size)) ,dtype=dtype)
        # Check if the DataFrame is empty
        if df.empty:
            # Add the current data into the attributes frame
            df = pd.DataFrame(values, columns=columns)
        else:
            # Add the current data into the attributes frame
            dfvalues = pd.DataFrame(values, columns=columns)
            # Append both dataframes
            df = pd.merge(df, dfvalues, how='inner', left_index=True, right_index=True)
        # Set the columns into the the current Point attribute
        return (df, columns)

    def getPrimsAttrib(self, name):
            return self._dfPrims[self._primAttribCols[name]]

    def delPrimsAttrib(self, name):
        self._dfPrims.drop(self._primAttribCols[name], axis=1, inplace=True)

    def addPrimsAttrib(self, name, values=None, size=3, default=None, dtype=None):
        # Get the new attribute and dataframe
        result = self._createAttribute(self._dfPrims,name,size,values,default,dtype)
        if not empty(result):
            # Set the returned dataframe with the new attribute
            self._dfPrims = result[0]
            # Set the columns into the the current Point attribute
            self._primAttribCols[name] = result[1]

    def addIndices(self, values, size=3, dtype=np.uint32):
         #Add prims Attributes Elements
        self.addPrimsAttrib("Id", values, size, dtype=dtype)
   
    def getPointAttrib(self, name):
        return self._dfPoints[self._pointAttribCols[name]]

    def delPointAttrib(self, name):
        self._dfPoints.drop(self._pointAttribCols[name], axis=1, inplace=True)

    def addPointAttrib(self, name, values=None, size=3,  default=None, dtype=None):
        # Get the new attribute and dataframe
        result = self._createAttribute(self._dfPoints,name,size,values,default,dtype)
        if not empty(result):
            # Set the returned dataframe with the new attribute
            self._dfPoints = result[0]
            # Set the columns into the the current Point attribute
            self._pointAttribCols[name] = result[1]

    def addPoints(self, values, size=3, dtype=np.float32):
        #Add point Attributes Position
        self.addPointAttrib("P", values, size, dtype)

    def addNormals(self, values, size=3, dtype=np.float32):
          #Add point Attributes Normals
        self.addPointAttrib("N", values, size, dtype)

    def render(self):
        # Bind the created Vertex Array Object
        GL.glBindVertexArray(self._VAO)
        # Draw the current geoemtry. Check if indices have been added
        if self._has_indices():
            GL.glDrawElements(self.mode, len(self._dfPrims.index) * 3, 
                              typeGL(Geometry.index_type), ctypes.c_void_p(0))
        else:
            GL.glDrawArrays(self.mode, 0, len(self._dfPoints.index))
        # Unbind VAO from GPU
        GL.glBindVertexArray(0)