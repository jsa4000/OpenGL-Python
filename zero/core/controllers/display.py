from collections import OrderedDict as dict
from ..base.utils import *
from ..base import Defaults, DBase
from .constants import *

__all__ = ['DisplayManager',
           'Display']

class DisplayManager(list):
    """ Display Manager Class

    This class will store all the displays created. Also it will
    manage the creation of the window, shutdown, etc..

    """
    def __init__(self, displays):
        """ Initialize the constructor
        """
        if not is_collection(displays):
            displays = [displays]
        self.extend(displays)

    def init(self):
        """ Initialize the creation of the windows
        """
        for display in self:
            display.init()
        return self

    def __setattr__(self, value):
        pass

    def update(self):
        """ Update the windows
        """
        for display in self:
            display.update()
        return self

    def close(self,dispose=False):
        """ Close the window
        """
        for display in self:
            display.close(dispose)
        return self

    def dispose(self):
        """ Dispose manually the window
        """
        for display in self:
            display.dispose()
        return self
            
class Display(Defaults):
    """ Abstract Display class

    """
        
    # Default Display Mode that will be used when crating the window
    # Open GL and Double Buffer are neccesary to display OpenGL
    defaultmode = [DisplayMode.opengl, DisplayMode.doublebuf]

    defaults = dict([("title","Display Window"), 
                     ("width",800), 
                     ("height",600), 
                     ("bpp",16), 
                     ("mode",DisplayMode.resizable)])

    def __init__(self, *args, **kwargs ):
        """ Initialize all the variables
        """
        super().__init__(*args,**kwargs)
        keys = list(Display.defaults.keys())
        for index, arg in enumerate(args):
            setattr(self, keys[index], arg)
  
    def init(self):
        """ Initialize the creation of the window
        """
        raise NotImplementedError
   
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

