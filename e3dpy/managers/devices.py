from ..core.utils import *
from ..core import EnumBase
from ..model.events import Event, EventType, Key, KeyModifier, MouseButton

class DeviceManager:
    """  Devices Class
    
    This class will manage the interfaze between the OS
    and the devices connected to. In order to get 
    the events from the devices some packages are going
    to be needed to get all the different events, types and
    parameters. 

    This class will use the request/response pattern design. 
    This means outer classes are going to request the data
    to this class and this class will send the response with 
    the events or the requested functionality.

     Event Type	    Parameters
        -------------------------------------
        QUIT	        None
        ACTIVEEVENT	    gain, state
        KEYDOWN	        unicode, key, mod
        KEYUP	        key, mod
        MOUSEMOTION	    pos, rel, buttons
        MOUSEBUTTONUP	pos, button
        MOUSEBUTTONDOWN	pos, button
        JOYAXISMOTION	joy, axis, value
        JOYBALLMOTION	joy, ball, rel
        JOYHATMOTION	joy, hat, value
        JOYBUTTONUP	    joy, button
        JOYBUTTONDOWN	joy, button
        VIDEORESIZE	    size, w, h
        VIDEOEXPOSE	    None
        USEREVENT	    Code
        -----------------------------------
        KEYSPRESSED     Keys

    """
    def __init__(self, devices):
        """ Initialize the variables.
        """
        pass

    def init(self):
        """ Initialize all the devices to start getting the inputs
        """
        return self

    
     



