import pygame
import threading
from ..graphics import Display, Camera, Shader, Texture, Geometry, DrawMode
from ..geometry.various import Triangle
from .base import Base
from .catalogue import CatalogueManager
from .scene import SceneGraph

class CoreEngine (Base):
    """ Core Engine Class

        This class is the main loop of the process that will manage all
        the scene like inputs, updates, rendering, physics, etc..

    """

    #Set variable multithread
    MULTI_THREAD = True

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
        return self._scene
    
    @property
    def is_running(self):
        return self._is_running

    def __init__(self, width=800, height=600, fps=60, scene=None):
        """ Contructor for the class
        """
        # Initilaize parameters
        self._width = width
        self._height = height
        self._fps = fps
        self._scene = scene
        # Initialize values
        self._display = None
        self._thread = None
        self._is_running = False

    def __del__(self):
        """ Clean up the memory
        """
        # Stop the process if any running
        self._thread_stop()
        # Dipose and close the display
        self._dispose_display()

    def _dispose_display(self):
        """ Close and dipose the diplay
        """
         # Be sure to close and dipose previous display
        if self.display:
            self.display.close()
            self._display.dispose()
            self._display = None

    def _thread_stop(self):
        """ This function will stop and dipose the thread
        """
        # Be sure to wait until the current process stops
        self._is_running = False
        # Wait and set to none
        if self._thread:
            self._thread.join()
            self._thread = None

    def _thread_start(self, process):
        """ This function will start the thread
        """
        # Stop the process if any running
        self._thread_stop()

        # Set started to true
        self._is_running = True
        # Create a new thread and run the process
        self._thread = threading.Thread(target=process)
        self._thread.start()  
   
    def _init_process(self):
        """Main process running the engine

        """
        # Create display
        #########################################################
        # Display must be created in the same context as OpenGL #
        #########################################################
        self.create_display("Core Engine")
        #georaw = cube3D()
        georaw = Triangle()
        # Create a Camera
        camera = Camera([0.0,0.0,-3.0],70.0,800/600,0.01,1000)
        # Create a texture
        texture = Texture("./assets/images/texture.png")
        # Create the default shader
        shader = Shader("default_shader", "./assets/shaders")
        # Create the geometry
        geo = Geometry("geo",shader,mode=DrawMode.triangles)
        #geo.addPoints(georaw[0], 4)
        geo.addPointAttrib("P",georaw[0], 4)
        #geo.addIndices(georaw[1])
        geo.addPointAttrib("Cd",georaw[2], 4)
        geo.addPointAttrib("UV",georaw[3], 2)
        #geo.addPoints(vertices, 4)
        geo.update()

        # Create a counter
        counter = 0
        last_mouse_location = [None, None]

        # Start the Main loop for the program
        while not self.display.isClosed and self._is_running:     
            #Manage the event from the gui
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._is_running = False
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    self._is_running = False
                if event.type == pygame.MOUSEMOTION:
                    # This events wil mange the events done by the mouse
                    button = pygame.mouse.get_pressed()  
                    current_mouse_location = pygame.mouse.get_pos()
                    # Check the current mouse button pressed
                    if button[0]:
                            # Left click to the button
                        if  last_mouse_location[0] is not None:
                            # Get the offset from the last position
                            camera.orbit(current_mouse_location[0] - last_mouse_location[0],
                                            current_mouse_location[1] - last_mouse_location[1])
                        
                    elif button[1]:
                            # Get the offset from the last position
                            camera.pan(current_mouse_location[0] - last_mouse_location[0],
                                        current_mouse_location[1] - last_mouse_location[1])
                    elif button[2]:
                        # Control the zoom
                        camera.zoom(last_mouse_location[1] - current_mouse_location[1] )
                    
                    # Update the mouse location for the next iteration
                    last_mouse_location = current_mouse_location

            # Events when holding 
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
            
            if keys[pygame.K_UP]:
                camera.zoom(1)
            elif keys[pygame.K_DOWN]:
                camera.zoom(-1)
            elif keys[pygame.K_RIGHT]:
                camera.strafe(-1)
            elif keys[pygame.K_LEFT]:
                camera.strafe(1)
            elif keys[pygame.K_y] and keys[pygame.K_LSHIFT]:
                camera.yaw(-0.1)
            elif keys[pygame.K_y]:
                camera.yaw(0.1)
            elif keys[pygame.K_p] and keys[pygame.K_LSHIFT]:
                camera.pitch(-0.1)
            elif keys[pygame.K_p]:
                camera.pitch(0.1)          
            elif keys[pygame.K_r] and keys[pygame.K_LSHIFT]:
                camera.roll(-0.1)
            elif keys[pygame.K_r]:
                camera.roll(0.1)
            elif keys[pygame.K_ESCAPE]:
                display.close()
                        
            # Clear the display
            self.display.clear()
            
            # Render all the elements that share the same shader.
            # Use the current Shader configuration
            shader.use()
            # Use the current texture after the shader
            texture.bind(0)
        
            # # Perform some motion to the object
            # sincount = math.sin(counter)
            # coscount = math.cos(counter)

            # geo.transform.position.x = sincount
            # geo.transform.rotation.z = counter*50
            # geo.transform.scale = [coscount,coscount,coscount]

            # counter += 0.01;

            shader.update("WORLD_MATRIX",geo.transform.model)
            shader.update("VIEW_MATRIX",camera.view_matrix())
            shader.update("PROJECTION_MATRIX",camera.projection_matrix())

            # Render the  geometry
            geo.render()
            # End Use the current Shader configuration
            shader.use(False)

            # Update the display
            self.display.update()

        # Set running to false
        self._is_running = False

    def create_display(self, name="Main Window"):
        """ Function that create the main display
        """
        # Be sure to close and dipose previous display
        self._dispose_display()
        # Create the new display
        self._display = Display(name, self.width, self.height)

    def start(self):
        """This method Starts the engine.
        """
        #Set wether the engin will be launch in a multi-thread context
        if CoreEngine.MULTI_THREAD:
            # Start the engine process (new thread)
            self._thread_start(self._init_process)
        else:
            # Start using the same thread
            self._init_process()

    def stop(self, close_display=False):
        """This method force to Stops the engine and close the window
        """
         # Stop the process if any running
        self._thread_stop()
        # Check if the user want to close the window
        if close_display:
            # close and dipose the display
            self._dispose_display()
  
    def dispose(self):
        """This method Stops the engine and close the window
        """
        # Force to clean the memory
        self.__del__()
