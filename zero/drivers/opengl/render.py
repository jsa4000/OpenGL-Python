import ctypes
import numpy as np
import OpenGL.GL as GL
from ...core.base.utils import *
from ...core import DrawMode
from .wrapper import opengl_drawmode_wrapper
from .wrapper import gldtype

class OpenGLRender(object):
    """
        This Class will render the Buffers stored in GPU
        openGL. It will use OpenGL and a double buffer so
        it can sweep between the buffers per frame.
    """

    # Default Background Color
    defaulBGColor = [0.0, 0.0, 0.0, 1.0]

    def __init__(self, mode=DrawMode.triangles):
        """ Initialize the Render Class
        """
        self.mode = mode

    def init(self):
         """ This function will initialize OpenGL with some functions
         by default. This case depth test is enabled by default initially.
         """
         GL.glEnable(GL.GL_DEPTH_TEST)

    def clear(self, color = defaulBGColor):
        """ This function wll clean the buffers on the GPU
        """
        GL.glClearColor(*color)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    def render(self, buffer):
        """
        """
        # Bind the created Vertex Array Object
        GL.glBindVertexArray(buffer._VAO)
        # Draw the current geoemtry. Check if indices have been added
        if buffer.geometry.indexed:
            GL.glDrawElements(opengl_drawmode_wrapper[self.mode], 3 * 3, 
                              gldtype(buffer.geometry.index_type), ctypes.c_void_p(0))
        else:
            GL.glDrawArrays(opengl_drawmode_wrapper[self.mode], 0, 1)
        # Unbind VAO from GPU
        GL.glBindVertexArray(0)
     

