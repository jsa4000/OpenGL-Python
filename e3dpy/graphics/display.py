import OpenGL.GL as GL
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

    # Default Background Color
    defaulBGColor = [0.0, 0.0, 0.0, 1.0]

    def __init__(self, title, width=800, height=600, bpp=16, displaymode = DisplayMode.resizable):
        # Initialize all the variables
        self.title = title
        self.width = width
        self.height = height
        self.bpp = bpp # RGBA 8*8*8*8 = 32 bits per pixel
        self.displaymode = displaymode
        # Initiali<e variables and Window
        self._initialize()

    def __enter__(self):
        # Enter will always return the object itself. Use with With expressons
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean all the variables and Memory
        self._dispose()

    def _dispose(self):
        try:
            #Finalize pygame
            pygame.quit()
            # SEt is closed to true
            self.isClosed = True
        except:
            print("ERROR: Error disposing the display.")

    def _initialize(self):
        # dispose and close all the windows prior to initialize
        self._dispose()
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
            # Enable Depth test to avoid overlaped areas
            GL.glEnable(GL.GL_DEPTH_TEST)
            # Clear the image
            self.clear()
            # Set isclosed to false
            self.isClosed = False
        except:
            print("ERROR: Error creating the display.")
   
    def close(self):
        # Set close to true
        self.isClosed = True

    def dispose(self):
        """ Stop the current task and close the window
        """
        self._dispose()

    def clear(self, color = defaulBGColor):
        # Clear will clean the windows color.
        GL.glClearColor(*color)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    def update(self):
        # With depth buffer flip is the way to update screen
        pygame.display.flip()
        # Check to close the window after update the window
        if self.isClosed:
            self._dispose()
