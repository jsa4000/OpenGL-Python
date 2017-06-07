import ctypes
import numpy as np
import OpenGL.GL as GL
from ...core.base.utils import *
from .wrapper import UsageMode



class OpenGLBuffer(object):
    """
        This element will create and store all the elements needed
        to Render a Geometrt
    """
  
    def __init__(self, usage=UsageMode.static_draw):
        # Initialize all the variables
        self.usage = usage
        # Vertex Array Object for all the Attributtes, elements, etc.
        self._VAO = None
        # Vertex Arrays Buffers for all the Attributes
        self._VAB = {}
        # Element Array Buffers for all the Attrbiutes
        self._EAB = None

    def _dispose(self):
        # Dispose all the objects and memory allocated
        GL.glDeleteVertexArrays(1,self._VAO)

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
  
    def update(self):
        # Depenging on the method to update the vertices using GPU or 
        # inmediate OpenGL the update will be different.
        self._copy_to_buffer()