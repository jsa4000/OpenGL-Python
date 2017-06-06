import ctypes
import numpy as np
import OpenGL.GL as GL
from ...core.utils import *
from .wrapper import DrawMode

class OpenGLRender(object):
    """
        This Class will render the Buffers stored in GPU
        openGL. It will use OpenGL and a double buffer so
        it can sweep between the buffers per frame.
    """

    # Default Background Color
    defaulBGColor = [0.0, 0.0, 0.0, 1.0]

    def __init__(self, *args, **kwargs):
        """ Initialize the Render Class
        """
        super().__init__(*args, **kwargs)

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

    def render(self):
        """
        """
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
     

