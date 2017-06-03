import pygame

class PygameDevice(KeyboardDevice, MouseDevice, UIDevice):
    """ Pygame Class interface
    """
          
    events= {
        pygame.QUIT: 
            lambda event: Event(type=EvenType.QUIT),
        pygame.ACTIVEEVENT: 
            lambda event: Event(type=EvenType.ACTIVEEVENT,gain=event.gain,state=event.state),
        pygame.KEYDOWN: 
            lambda event: Event(type=EvenType.KEYDOWN,key=event.key,mod=event.mod),
        pygame.KEYUP: 
            lambda event: Event(type=EvenType.KEYUP,key=event.key,mod=event.mod),
        pygame.MOUSEMOTION: 
            lambda event: Event(type=EvenType.MOUSEMOTION,pos=event.pos,rel=event.rel,buttons=self.get_buttons_pressed()),
        pygame.MOUSEBUTTONUP: 
            lambda event: Event(type=EvenType.MOUSEBUTTONUP,pos=event.pos,button=event.button),
        pygame.MOUSEBUTTONDOWN: 
            lambda event: Event(type=EvenType.MOUSEBUTTONDOWN,pos=event.pos,button=event.button),
        pygame.JOYAXISMOTION: 
            lambda event: Event(type=EvenType.JOYAXISMOTION,joy=event.joy,axis=event.axis,value=event.value),
        pygame.JOYBALLMOTION: 
            lambda event: Event(type=EvenType.JOYBALLMOTION,joy=event.joy,ball=event.ball,rel=event.rel),
        pygame.JOYHATMOTION: 
            lambda event: Event(type=EvenType.JOYHATMOTION,joy=event.joy,hat=event.hat,value=event.value),
        pygame.JOYBUTTONUP: 
            lambda event: Event(type=EvenType.JOYBUTTONUP,joy=event.joy,button=event.button),
        pygame.JOYBUTTONDOWN: 
            lambda event: Event(type=EvenType.JOYBUTTONDOWN,joy=event.joy,button=event.button),
        pygame.VIDEORESIZE: 
            lambda event: Event(type=EvenType.VIDEORESIZE,size=event.size,w=event.w,h=event.h),
        pygame.VIDEOEXPOSE: 
            lambda event: Event(type=EvenType.VIDEOEXPOSE),
        pygame.USEREVENT: 
            lambda event: Event(type=EvenType.USEREVENT,Code=event.Code),
    }

    def __init__(self):
        pass

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
        events = [PygameWrapper.pygame_events[event.type] for event in pygame.event.get()]
        if empty(events):
             # Check whether buttons or keys are pressed
            keys = self.get_keys_pressed()
            if not empty(keys):
                events.append(ParseDict(type=EventType.KEYSPRESSED, keys=keys))
 
        #Returne the capture events
        return events
