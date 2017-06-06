import pygame
from ...core.utils import *
from ...core import DisplayMode, Display

pygame_displaymode_wrapper = {
    DisplayMode.fullscreen  : pygame.FULLSCREEN,	# window is fullscreen
    DisplayMode.resizable   : pygame.RESIZABLE,  # window is resizeable
    DisplayMode.noframe     : pygame.NOFRAME,	# window has no border or controls
    DisplayMode.doublebuf   : pygame.DOUBLEBUF,	# use double buffer - recommended for HWSURFACE or OPENGL
    DisplayMode.hwaccel     : pygame.HWSURFACE, # window is hardware accelerated, only possible in combination with FULLSCREEN
    DisplayMode.opengl      : pygame.OPENGL,     # window is renderable by OpenGL
}

class PygameDisplay(Display):
    """
        This Class will manager the Display to interact with
        openGL. It will use OpenGL and a double buffer so
        it can sweep between the buffers per frame.

        Also the display is going to manage the interaction
        with the user regarding the events, mouse buttons and
        keypress done.
    """

    def __init__(self, *args, **kwargs ):
        """ Initialize the Class the class
        """
        super().__init__(*args, **kwargs)

    def _get_pygame_mode(self):
        """ Return a valid pygame mode that represent all the modes
            modes = modes1|mode2|mode3 
        """
        modes = list(Display.defaultmode)
        modes.append(self.mode)
        result = None
        for mode in modes:
            if result:
                result |= pygame_displaymode_wrapper[mode]
            else:
                result = pygame_displaymode_wrapper[mode]
        return result

    def __del__(self):
        try:
            #Finalize pygame
            pygame.quit()
        except:
            print("ERROR: Error disposing the display.")

    def init(self):
        # Initialize and open the display window
        try:
            # Initialize pygame
            pygame.init()
            # Set title bar caption
            pygame.display.set_caption(self.title)
            # Initialize the display
            screen = pygame.display.set_mode((self.width,self.height), 
                                        self._get_pygame_mode(),self.bpp)
            # Set isclosed to false
            self.isClosed = False
        except:
            print("ERROR: Error creating the display.")
   
    def update(self):
        # With depth buffer flip is the way to update screen
        pygame.display.flip()
        # Check to close the window after update the window
        if self.isClosed:
            self._dispose()

    def close(self, dispose=False):
        """ This function will set close to true. However, this function
        also allows to terminate and close the display manually to
        safety close other processes that can be interacting with it 
        """
        self.isClosed = True
        # Check if the windo must be also diposed
        if dispose:
            self.__del__()

    def dispose(self):
        """ Stop the current task and close the window
        """
        self.__del__()
