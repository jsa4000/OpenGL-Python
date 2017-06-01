from .base import ThreadBase 
from ..drivers import Display 

__all__ = ['CoreEngine']

class CoreEngine(ThreadBase):
    """ Core Engine Class

        This class is the main loop of the process that will manage all
        the scene like inputs, updates, rendering, physics, etc..

    """

    @property
    def display(self):
        return self._display

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def fps(self):
        return self._fps

    @property
    def scene(self):
        """ Get current Scene Graph
        """
        return self._scene

    @scene.setter
    def scene(self, value):
        """ This will set the new Scene Graph to render.
        """
        self._scene = value
     
    def __init__(self, width=800, height=600, fps=60, scene=None):
        """ Contructor for the class

        This class is the main loop for the Engine. In this class all the 
        Managers will be created.

        System, or managers, will take the Scene Graph and perfor
        the work that corresponf, i.e. input, update, physics, render etc

        Also the engine will initialize the Display and do the calls to
        the display driver so the Scene could be rendered properly.
        
        """
        super(CoreEngine,self).__init__()
        # Initilaize parameters
        self._width = width
        self._height = height
        self._fps = fps
        # Set the Scene Graph
        self._scene = scene
        # Initialize display
        self._display = None

    def __del__(self):
        """ Clean up the memory
        """
        # Call threadBase __del__
        super(Engine,self).__del__()
        # Dipose and close the display
        self._dispose_display()

    def _close_display(self):
        """ Close and dipose the diplay
        """
        # Be sure to close and dipose previous display
        if self.display:
            self.display.close()
            self._display.dispose()
            self._display = None

    def _create_display(self, name="Main Window"):
        """ Function that create the main display
        """
        # Be sure to close and dipose previous display
        self._close_display()
        # Create the new display
        self._display = Display(name, self.width, self.height)

    # Override
    def _process(self):
        """Main process running the engine
           
        """
        # Display must be created in the same context (thread) as OpenGL
        self._create_display()
       
        # Start the Main loop for the program
        while not self.display.isClosed and self._running:     

            # Input
            # Update

            # Clear the display
            self.display.clear()
            # Render all the elements that share the same shader.
            # Render()
            # Update the display
            self.display.update()

        # Set running to false
        self._running = False

    def stop(self, close=False):
        """This method force to Stops the engine and close the window
        """
        super(CoreEngine,self).stop()
        # Check if the user want to close the window
        if close:
            # close and dipose the display
            self._close_display()
  
 