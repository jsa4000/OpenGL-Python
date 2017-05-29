import pygame
from ..graphics import Display, Camera, Shader, Texture, Geometry, DrawMode
from ..geometry.various import Triangle
from .catalogue import CatalogueManager

class Engine:
    """Class engine

    """
    
    def __init__(self):
        # Initialize the engine with default variables
        self._init()

    def _init(self):
        # Initialize the engine with default variables
        pass

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
            last_mouse_location = [None, None]
            # Start the Main loop for the program
            while not display.isClosed:     
                #Manage the event from the gui
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        display.close()
                    if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                        display.close()
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
                display.clear()
                
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
                display.update()

    def start(self):
        """This method Starts the engine.
        """
        # Start the engine (new process)
        self._process()

    def end(self):
        """This method Stops the engine
        """
        pass