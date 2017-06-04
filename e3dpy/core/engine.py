import time
from .base import Thread
from .controllers import DisplayManager, DeviceManager
from ..managers import InputManager, SceneManager, RenderManager

__all__ = ['CoreEngine']

class CoreEngine(Thread):
    """ Core Engine Class

        This class is the main loop of the process that will manage all
        the scene like inputs, updates, rendering, physics, etc..
    """

    @property
    def display(self):
        """ Return display manager 
        """
        return self._display

    @property
    def device(self):
        """ Return device manager
        """
        return self._device

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
     
    def __init__(self, display, device, scene, fps=60):
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
        self._display = display
        self._device = device
        self._scene = scene
        self._fps = fps
        # Initialize the variables for the Managers
        self._input_manager = None
        self._scene_manager = None
        self._render_manager = None

    def __del__(self):
        """ Clean up the memory
        """
        # Call threadBase __del__
        super(CoreEngine,self).__del__()
    
    def init(self):
        """ Initialize all the Managers at start
        """
        self._input_manager = InputManager(self).init()
        self._scene_manager = SceneManager(self).init()
        self._render_manager = RenderManager(self).init()
        # Return itself for Cascade
        return self

    # Override
    def _process(self):
        """ Main process running the engine

        Basically the overal loop will be: Input, Update and Render           
        """
        # Display must be created in the same context (thread) as OpenGL
        self.display.init()
       
        # Start the Main loop for the program
        while self.running:     

            # Process Inputs from the user
            self._input_manager.run()

            # Update Scene, Physics, Logic and solvers
            # Update depend on time, inputs, collisions, logic, etc..
            #  self._scene_manager.run()

            # Finally render the scene
            # self._render_manager.run()

            time.sleep(1/60)

            # Update the display
            self.display.update()

        # Set running to false
        self._running = False

    def stop(self, close=False):
        """This method force to Stops the engine and close the window
        """
        super(CoreEngine,self).stop()
        # Close All the windows and dipose
        self.display.close(True)

