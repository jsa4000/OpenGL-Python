from collections import OrderedDict as dict
from ..core.utils import *
from .base import Defaults, DBase
from .constants import *

__all__ = ['DeviceManager',
           'Device',
           'KeyboardDevice',
           'MouseDevice',
           'SystemDevice',
           'JoyDevice']

class DeviceManager(dict):
    """ Device Manager Class
    
    This class will store all the devices created. Also it will
    manage the creation of the window, shutdown, etc..
    """

    def __init__(self, devices):
        """ Initialize the constructor
        """
        if not is_collection(devices):
            devices = [devices]
        for device in devices:
            self[device.__class__.__name__] = device
    
    def init(self): 
        """ Init the device
        """
        for device in self:
            self[device].init()
        return self

    def get_events(self): 
        """ Get the events from the devices
        """
        events = []
        for device in self:
            events.extend(self[device].get_events())
        return events

    def send_events(self, event, parameters):
        """ Send the events to the devices
        """
        for device in self:
            self[device].send_events(event,parameters)
        return self    

    def dispose(self): 
        for device in self:
            self[device].dispose()
        return self


class Device(object):
    """ Abstract interface for the devices

    Derived objects from this class are the controllers to
    receiver and send data from the device to the applcation.
    the will act as a Human interface Device (HID) by providing
    Inputs and Outputs (I/O).

    init(): initilize the device
    get_events(): get the events of the device for the curren epoch
    send_events(): send events to the devive
    dipose(): close and free the device. (for safety reasons)

    """
    def init(self): pass
    def get_events(self): pass
    def send_events(self, event, parameters): pass
    def dispose(self): pass

class KeyboardDevice(Device):
    
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

class MouseDevice(Device):
    
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

class SystemDevice(Device):
    """ System Device Class

    System Device class will allow the interaction between the application
    With the OS. This means it will allow to log all the events ocurred
    and allows to get some information and details about the OS, like
    resolution, Cores, Memory, etc. Also it will allow to send some events
    to a handle and performing some other functionality.
    """

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

class JoyDevice(Device):
    """ Joy Device Class
    """

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
        JOYAXISMOTION	joy, axis, value
        JOYBALLMOTION	joy, ball, rel
        JOYHATMOTION	joy, hat, value
        JOYBUTTONUP	    joy, button
        JOYBUTTONDOWN	joy, button
        """
        #Returne the capture events
        raise NotImplementedError

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
