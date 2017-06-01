from .base import ThreadBase 
from ..model import Window
from ..workers import InputsWorker, SceneWorker, RenderWorker

__all__ = ['CoreEngine']

class CoreEngine(ThreadBase):
    """ Core Engine Class

        This class is the main loop of the process that will manage all
        the scene like inputs, updates, rendering, physics, etc..

    """

    @property
    def display(self):
        """ Get current Scene Graph
        """
        return self._display

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
     
    def __init__(self, display, fps=60, scene=None):
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
        self._fps = fps
        # Set the Scene Graph
        self._scene = scene
        # Initialize the variables for the Workers
        self._input_worker = None
        self._scene_worker = None
        self._render_worker = None

    def __del__(self):
        """ Clean up the memory
        """
        # Call threadBase __del__
        super(CoreEngine,self).__del__()

    
    def init(self):
        """ Initialize all the Workers at start
        """
        self._input_worker = InputsWorker().init()
        self._scene_worker = SceneWorker().init()
        self._render_worker = RenderWorker().init()
        return self


    # Override
    def _process(self):
        """Main process running the engine
        Basically the overal loop will be: Input, Update and Render           
        """
        # Display must be created in the same context (thread) as OpenGL
        self._display.init()
       
        # Start the Main loop for the program
        while not self._display.isClosed and self._running:     

            # Process Inputs from the user
            self._input_worker.run()

            # Update Scene, Physics, Logic and solvers
            # Update depend on time, inputs, collisions, logic, etc..
            self._scene_worker.run()

            # Finally render the scene
            self._render_worker.run()

            # Update the display
            self._display.update()

        # Set running to false
        self._running = False

    def stop(self, close=False):
        """This method force to Stops the engine and close the window
        """
        super(CoreEngine,self).stop()

