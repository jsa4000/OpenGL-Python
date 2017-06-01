import pygame

class Device:
    """  Device Class
       
    This class will manager the interfaze between the OS
    ans python. In order to get the inputs we are going to 
    use pygame. This is the package used for creating the
    display.

    """
 
    def __init__(self):
        """This class won't do anything.
        It's supposed to be alreaddy initialized pygame.
        """
        pass

    def init(self):
        """
        """
        #pygame.init()
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

    def get_mouse_motion(self):
        """
        """
        return pygame.mouse.get_rel()

    def get_mouse_position(self):
        """ This will return the current mouse position
        The output is a Vector2 with the two coordinates
        """
        return pygame.mouse.get_pos()
  
    def get_events(self):
        """ This functiin will return an array of (type, key)
        elements with the inpus received.

        To take into consideration if a key is currently being pressed
        the you have to call get_key_pressed(). Since this events
        wont recognize the pressed action until it will be released again.

        if event.type == pygame.QUIT:
            display.close()
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            display.close()
        """
        return pygame.event.get()

    def get_mouse_pressed(self):
        """ Function to get the buttons currently pressed
        The function will return an array with the mouse 
        buttons pressed. [0,1,0]
        
        Example:
            if mouse[LEFTBUTTON]:
                pass
        """
        return pygame.mouse.get_pos()

    def get_key_pressed(self):
        """ This will return a mask with the keys pressed.
        To check the keys that are currently pressed use the 
        following code:

        keys = get_keyboard_input()
        if keys[pygame.K_LEFT] and keys[pygame.K_LSHIFT]:
            pass

        NOTE: To check the specific event that has been triggered
        (KEYUP, KEYDOWN ), use isntead get_events()
        """  
        # Force to update the current events and retrieve the current
        pygame.event.pump()
        return pygame.key.get_pressed() 