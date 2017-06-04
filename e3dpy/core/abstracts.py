from ..core.utils import *
from .constants import *

__all__ = ['Device',
           'Keyboard',
           'Mouse',
           'System',
           'Joy',
           'Display',
           'Render'.
           'Manager']

class Device(object):
    """ Abstract interface for the devices
    init(): initilize the device
    get_events(): get the events of the device for the curren epoch
    dipose(): close and free the device. (for safety reasons)

    """
    def init(self): pass
    def get_events(self): pass
    def close(self): pass

class Keyboard(Device):
    
    def init(self):
        """ Initialize the device
        """
        raise NotImplementedError

    def get_events(self):
        """ This function will return an array of (type, key)
        elements with the inpus received.

        To take into consideration if a key is currently being pressed
        the you have to call get_key_pressed(). Since this events
        wont recognize the pressed action until it will be released again.

        if event.type == EvenType.QUIT:
            display.close()
        if event.type == EvenType.KEYUP and event.key == EvenType.K_ESCAPE:
            display.close()

        Event Type	    Parameters
        -------------------------------------
        KEYDOWN	        unicode, key, mod
        KEYUP	        key, mod
        KEYSPRESSED     Keys
        """
        raise NotImplementedError

    def get_pressed(self):
        """ Return the keys pressed with the key-code 
        The returned array for this function will be:
        [8, 13]

        # In pygame we do the following, because the position will
        give us if that key has been pressed or not
        keys = get_keyboard_input()
        if keys[pygame.K_LEFT] and keys[pygame.K_LSHIFT]:
            pass

        NOTE: To check the specific event that has been triggered
        (KEYUP, KEYDOWN ), use isntead get_events()
        When you keep pressed a button there is no event assigned,
        so we need to check it after.
        """  
        raise NotImplementedError

class Mouse(Device):
    
    def init(self):
        """ Initialize the device
        """
        raise NotImplementedError

    def get_events(self):
        """ This function will return an array of (type, key)
        elements with the inpus received.

        To take into consideration if a key is currently being pressed
        the you have to call get_key_pressed(). Since this events
        wont recognize the pressed action until it will be released again.

        if event.type == EvenType.QUIT:
            display.close()
        if event.type == EvenType.KEYUP and event.key == EvenType.K_ESCAPE:
            display.close()

        Event Type	    Parameters
        -------------------------------------
        MOUSEMOTION	    pos, rel, buttons
        MOUSEBUTTONUP	pos, button
        MOUSEBUTTONDOWN	pos, button
        """
        raise NotImplementedError

    def set_mouse_visible(self, visible):
        """ Set visible the cursor
        """
        raise NotImplementedError

    def set_mouse_position(self, x, y):
        """ Set current position
        """
        raise NotImplementedError

    def get_mouse_offset(self):
        """
        """
       raise NotImplementedError

    def get_mouse_position(self):
        """ This will return the current mouse position
        The output must be a Vector2 with x,y coordinates
        
        Example: [234,234]
        """
        raise NotImplementedError

     def get_pressed(self):
        """ Function to get the buttons currently pressed
        The function will return an array with the mouse 
        buttons pressed. 
        
        For example if the original array is [0,1,0],
        This will return [1] wher the pressed button is the
        index = 1

        Example:
            if mouse[LEFTBUTTON]:
                pass
        """
        raise NotImplementedError

class System(Device):
    
    def init(self):
        """ Initialize the device
        """
        raise NotImplementedError

    def get_events(self):
        """ This function will return an array of (type, key)
        elements with the inpus received.

        To take into consideration if a key is currently being pressed
        the you have to call get_key_pressed(). Since this events
        wont recognize the pressed action until it will be released again.

        if event.type == EvenType.QUIT:
            display.close()
        if event.type == EvenType.KEYUP and event.key == EvenType.K_ESCAPE:
            display.close()

        Event Type	    Parameters
        -------------------------------------
        QUIT	        None
        ACTIVEEVENT	    gain, state
        VIDEORESIZE	    size, w, h
        VIDEOEXPOSE	    None
        USEREVENT	    Code
        """
        #Returne the capture events
        raise NotImplementedError

class Display(object):
    """ Abstract Display class

    """
        
    # Default Display Mode that will be used when crating the window
    # Open GL and Double Buffer are neccesary to display OpenGL
    defaultmode = DisplayMode.opengl|DisplayMode.doublebuf

    def __init__(self, title, width=800, height=600, bpp=16, mode=Display.resizable ):
        """ Initialize all the variables
        """
        self.title = title
        self.width = width
        self.height = height
        self.bpp = bpp # RGBA 8*8*8*8 = 32 bits per pixel
        self.mode = mode

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

class Render(pbject):
    pass

class Manager(object):
    """ Abstract Worker Class
    """
   
    def init(self):
        """ Initialize the Manager
        """
        raise NotImplementedError

    def run(self):
        """ Start the Manager process
        """
        raise NotImplementedError

    def dispose(self):
        """ Dipose the Manager
        """
        raise NotImplementedError
