from ..core.utils import *

class WindowMode:
    fullscreen  = 0
    resizable   = 1
    noframe     = 2
    doublebuf   = 3
    hwaccel     = 4
    opengl      = 5

class Window:
    """ Windows class

    This is a wrapper for the engine to encalsulate the basic logic of a 
    Display to use for the render.
    """

    def __init__(self, display):
        # Initialize all the variables
        self._display = display
        #Inititlize the variables
        self.title = self._display.title
        self.width = self._display.width
        self.height = self._display.height
        # RGBA 8*8*8*8 = 32 bits per pixel
        self.bpp = self._display.bpp
        self.displaymode = self._display.displaymode

    def __del__(self):
        """ Remove all the memory allocated and close the Window
        """
        self._display.__del__()

    def init(self):
        self._display.init()
   
    def update(self):
        """ Update the window
        """
        self._display.update()

    def close(self,dispose=False):
        """ Close the window
        """
        self._display.close(force)

    def dispose(self):
        """ Dispose manuallt the window
        """
        self._display.dispose()