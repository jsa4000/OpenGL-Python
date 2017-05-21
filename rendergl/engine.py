import math
import pygame
from .graphics import Display, Camera, Shader, Texture, Geometry, DrawMode
from .geometry.create.various import Triangle

class Engine:
    """Class engine


    """

    def __init__(self):
        # Initialize the engine with default variables
        self._init()

    def start(self):
        """This method Starts the engine.
        """
        # Start the engine (new process)
        self._process()

    def end(self):
        """This method Stops the engine
        """
        pass

    def _init(self):
        """Initialize engine
        """

    def _process(self):
        """Main process running the engine
        """
         # Create the Display with the main window
        with  Display("Main Window",800,600) as display:
        
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
            # Start the Main loop for the program
            while not display.isClosed:     
                # Manage the event from the gui
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        display.close()
                    if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                        display.close()
                    if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                        camera.position.y += 0.1
                    if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                        camera.position.y -= 0.1
                    if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                        camera.position.x += 0.1
                    if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                        camera.position.x -= 0.1
                            
                # Clear the display
                display.clear()
                
                # Render all the elements that share the same shader.
                # Use the current Shader configuration
                shader.use()
                # Use the current texture after the shader
                texture.bind(0)
            
                # Perform some motion to the object
                sincount = math.sin(counter)
                coscount = math.cos(counter)

                geo.transform.position.x = sincount
                geo.transform.rotation.z = counter*50
                geo.transform.scale = [coscount,coscount,coscount]

                counter += 0.01;

                shader.update("WORLD_MATRIX",geo.transform.model)
                shader.update("VIEW_MATRIX",camera.view)
                shader.update("PROJECTION_MATRIX",camera.projection)

                # Render the  geometry
                geo.render()
                # End Use the current Shader configuration
                shader.use(False)

                # Update the display
                display.update()
