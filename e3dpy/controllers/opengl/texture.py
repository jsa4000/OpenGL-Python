import ctypes
import numpy as np
import OpenGL.GL as GL

class OpenGLTexture:
    """
        This class will create and store all the elements needed
        to create the texture.
        The module needed to load the images is Pillow
            from PIL import Image
    """
    # Maximun number of textures
    max_textures = 32

    def __init__(self, filename):
        # Initialize all the variables
        self.filename = filename
        # Create a texture variable with the pointer to the buffer
        self._texture = None
        # Initiali<e variables and Window
        self._initialize()

    def __enter__(self):
        # Enter will always return the object itself. Use with With expressons
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean all the memery stored
        self._dispose()

    def _dispose(self):
        pass

    def _initialize(self):
        # Create the texture and copy into OpenGL
        self._texture = self._load_Texture(self.filename)

    def _load_Texture(self,filename):
        # Check if the file exists
        if file_exists(filename):
            # Load the image using the path configured
            img_data, size = load_image(filename)
            width, height = size
            # Generate texture buffer to load into GPU
            texture = GL.glGenTextures(1)
            # Set initial parameters needed prior send the image to OpenGL
            GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
            # Bind current texture buffer to load the data
            GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
            # Set parameters to tell OpenGL how to draw the image
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, width, height, 0,
                            GL.GL_RGB, gldtype(img_data.dtype), img_data)
            # Create different Mipmaps for the current texure
            GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
            return texture
        # If not exist return None
        return None
    
    def bind(self, count):
        """
            This method will bind the current texture to be used to the graphic card
            Parameter:
                count: this is used to assign a free slot to the texture into OpenGL
                    [   Some graphic cards could have a limitation in the number of   ]
                    [   textures that can store, depending on the memory.             ]
        """
        if self._texture and (count > 0 and count < Texture.max_textures + 1 ):
            # Following we will activate the texture in a slot 
            GL.glActiveTexture(GL.GL_TEXTURE0 + count)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)