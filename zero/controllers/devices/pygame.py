import pygame
from ...core.utils import *
from ...core import (Event, DeviceEvent, Device, KeyboardDevice, 
                                MouseDevice, SystemDevice, JoyDevice)

pygame_events_wrapper = {
    pygame.QUIT: 
        lambda event, self: Event(type=DeviceEvent.QUIT),
    pygame.ACTIVEEVENT: 
        lambda event, self: Event(type=DeviceEvent.ACTIVEEVENT,gain=event.gain,state=event.state),
    pygame.KEYDOWN: 
        lambda event, self: Event(type=DeviceEvent.KEYDOWN,key=event.key,mod=event.mod),
    pygame.KEYUP: 
        lambda event, self: Event(type=DeviceEvent.KEYUP,key=event.key,mod=event.mod),
    pygame.MOUSEMOTION: 
        lambda event, self: Event(type=DeviceEvent.MOUSEMOTION,pos=event.pos,rel=event.rel,buttons=self.get_buttons_pressed()),
    pygame.MOUSEBUTTONUP: 
        lambda event, self: Event(type=DeviceEvent.MOUSEBUTTONUP,pos=event.pos,button=event.button),
    pygame.MOUSEBUTTONDOWN: 
        lambda event, self: Event(type=DeviceEvent.MOUSEBUTTONDOWN,pos=event.pos,button=event.button),
    pygame.JOYAXISMOTION: 
        lambda event, self: Event(type=DeviceEvent.JOYAXISMOTION,joy=event.joy,axis=event.axis,value=event.value),
    pygame.JOYBALLMOTION: 
        lambda event, self: Event(type=DeviceEvent.JOYBALLMOTION,joy=event.joy,ball=event.ball,rel=event.rel),
    pygame.JOYHATMOTION: 
        lambda event, self: Event(type=DeviceEvent.JOYHATMOTION,joy=event.joy,hat=event.hat,value=event.value),
    pygame.JOYBUTTONUP: 
        lambda event, self: Event(type=DeviceEvent.JOYBUTTONUP,joy=event.joy,button=event.button),
    pygame.JOYBUTTONDOWN: 
        lambda event, self: Event(type=DeviceEvent.JOYBUTTONDOWN,joy=event.joy,button=event.button),
    pygame.VIDEORESIZE: 
        lambda event, self: Event(type=DeviceEvent.VIDEORESIZE,size=event.size,w=event.w,h=event.h),
    pygame.VIDEOEXPOSE: 
        lambda event, self: Event(type=DeviceEvent.VIDEOEXPOSE),
    pygame.USEREVENT: 
        lambda event, self: Event(type=DeviceEvent.USEREVENT,Code=event.Code),
}

class PygameDevice(KeyboardDevice, MouseDevice, JoyDevice, SystemDevice):
    """ Pygame Class interface

    This class will take Keyboard, Mouse, Joy and System Events.
    In order to maintain an interface it will use a wrapper and 
    inheritances to ensure all the devices are using the same
    data across the engine input/output.
    """
 
    def __init__(self, *args, **kwargs):
        """ Initialize the Class
        """
        super().__init__(*args, **kwargs)

    def init(self):
        """ Initialize the device
        """
        # Be sure pygame is already initialized
        pygame.init()
        return self

    def set_mouse_visible(self, visible):
        """ Set visible the cursor
        """
        pygame.mouse.set_visible(visible)
        return self

    def set_mouse_position(self, x, y):
        """ Set current position
        """
        pygame.mouse.set_pos([x,y])
        return self

    def get_mouse_offset(self):
        """
        """
        return pygame.mouse.get_rel()

    def get_mouse_position(self):
        """ This will return the current mouse position
        The output is a Vector2 with x,y coordinates
        
        Example: [234,234]
        """
        return pygame.mouse.get_pos()

    def get_buttons_pressed(self):
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
        #return pygame.mouse.get_pressed()
        return [i for i,value in enumerate(pygame.mouse.get_pressed()) if value]

    def get_keys_pressed(self):
        """ This will return a mask with the keys pressed.
        To check the keys that are currently pressed use the 
        following code:

        (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 
         0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
         0, 0, 0, 0, 0, .. , 0, 0)

        1 in Position 8 => K_BACKSPACE = 8
        1 in postion 13 => K_RETURN	=	13

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
        # Force to update the current events and retrieve the current
        pygame.event.pump()
        # Search for all the postion equal to 1
        return [i for i,value in enumerate(pygame.key.get_pressed()) if value]
       
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
        pygame_events = pygame.event.get()
        events = [pygame_events_wrapper[event.type](event,self) for event in pygame_events]
        # If no KEYDOWN or KEYUP events check if any already pressed
        if pygame.KEYDOWN not in pygame_events and pygame.KEYUP not in pygame_events:
             # Check whether buttons or keys are pressed
            keys = self.get_keys_pressed()
            if not empty(keys):
                # Create new Event for key pressed
                events.append(Event(type=DeviceEvent.KEYSPRESSED, keys=keys))
 
        #Returne the capture events
        return events
