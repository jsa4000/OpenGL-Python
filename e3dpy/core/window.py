from ..core.utils import *

class WindowMode:
    fullscreen  = 0
    resizable   = 1
    noframe     = 2
    doublebuf   = 3
    hwaccel     = 4
    opengl      = 5

class Window(object):
    """ Abstract  Windows class

    """

    def __init__(self, title, width=800, height=600, bpp=16, mode = WindowMode.resizable ):
        """ Initialize all the variables
        """
        self.title = title
        self.width = width
        self.height = height
        self.bpp = bpp # RGBA 8*8*8*8 = 32 bits per pixel
        self.mode = mode

    def __del__(self):
        """ Remove all the memory allocated and close the Window
        """
        pass

    def init(self):
        return self
   
    def update(self):
        """ Update the window
        """
        raise NotImplementedError

    def close(self,dispose=False):
        """ Close the window
        """
        raise NotImplementedError

    def dispose(self):
        """ Dispose manually the window
        """
        raise NotImplementedError