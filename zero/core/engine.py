import time
from .base import Thread
from .controllers import DisplayController, DeviceController
from ..system import InputManager, SceneManager, RenderManager

__all__ = ['CoreEngine']

class CoreEngine(Thread):
    """ Core Engine Class

        This class is the main loop of the process that will manage all
        the scene like inputs, updates, rendering, physics, etc..
    """

    @property
    def display(self):
        """ Return display controller 
        """
        return self._display

    @property
    def device(self):
        """ Return device controller
        """
        return self._device

    @property
    def render(self):
        """ Return render controller 
        """
        return self._render

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
     
    def __init__(self, display, device, render, scene, fps=60):
        """ Contructor for the class

        This class is the main loop for the Engine. In this class all the 
        Managers and workers will be created.

        Devices or controllers that will be used in for the engine. They 
        will take the Scene Graph and perform the work that corresponds 
        i.e. input, update, physics, render etc.

        Controllers are used for the cases where more devices or drivers are
        used, for example in cases of diplays or devices, where it can be used 
        more than one device at the same time. Also it can be used for rendering
        where depending on the type of rendering it could be used one or more
        rendering types, like opengl, directx, ray casting, etc..

        Also the engine will initialize the Display and do the calls to
        the display driver so the Scene could be rendered properly.

        Parameters:

        display: controller that will be used to display- The admited 
        classes will be :DisplayController or Display

        device: controller or device that will be used to interact with the 
        user by the Human User Devices(HUD). The admited classes are :
        DeviceController or any of the devices associated with it that allows
        get_events operation, like KeyboardDevice, MouseDevice, etc..
    
        render: controller that will be used for the engine. The rende controller
        will manage all the interface between the engine and the drivers being
        used.

        scene: This object will contain the whole scene with all the entities
        and componentes. The catalogueManager.Instance() is storing all this
        information in the creation and bindings between entities and components.
        
        fps: frames-per-second the engine will use.

        """
        super(CoreEngine,self).__init__()
        # Initilaize parameters
        self._display = display
        self._device = device
        self._render = render
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
            self._input_manager.run(False)

            # Update Scene, Physics, Logic and solvers
            self._scene_manager.run()

            # Finally render the scene
            self._render_manager.run()

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

