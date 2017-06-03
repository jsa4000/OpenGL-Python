import pygame

class DisplayMode:
    fullscreen  = pygame.FULLSCREEN	# window is fullscreen
    resizable   = pygame.RESIZABLE  # window is resizeable
    noframe     = pygame.NOFRAME	# window has no border or controls
    doublebuf   = pygame.DOUBLEBUF	# use double buffer - recommended for HWSURFACE or OPENGL
    hwaccel     = pygame.HWSURFACE  # window is hardware accelerated, only possible in combination with FULLSCREEN
    opengl      = pygame.OPENGL     # window is renderable by OpenGL

class Display:
    """
        This Class will manager the Display to interact with
        openGL. It will use OpenGL and a double buffer so
        it can sweep between the buffers per frame.

        Also the display is going to manage the interaction
        with the user regarding the events, mouse buttons and
        keypress done.
    """
    
    # Default Display Mode that will be used when crating the window
    # Open GL and Double Buffer are neccesary to display OpenGL
    defaultmode = DisplayMode.opengl|DisplayMode.doublebuf

    def __init__(self, title, width=800, height=600, bpp=16, displaymode = DisplayMode.resizable):
        # Initialize all the variables
        self.title = title
        self.width = width
        self.height = height
        self.bpp = bpp # RGBA 8*8*8*8 = 32 bits per pixel
        self.displaymode = displaymode

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
            screen = pygame.display.set_mode((self.width, self.height), 
                                        Display.defaultmode|self.displaymode,
                                        self.bpp)
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
