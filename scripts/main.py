import os
import sys
import time
import math

# Add the currnent parent path so it recognize rendegl package entirely
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from zero.components import InputComponent
from zero.core import (Base, CoreEngine, SceneGraph, Thread, EntityCatalogue,
                      DeviceController, DisplayController, RenderController)
from zero.core.geometry import Camera, Material, Geometry                 
from zero.core.base.utils import get_cmd_parameters
from zero.drivers import PygameDevice, PygameDisplay, OpenGLRender

def create_scene():
    """ Create initial scene
    """
    # Create the main roor for all the sub-entities
    root = SceneGraph.create_empty("Root",position=[0.0,0.0,0.0])
    
    # Create the default camera
    camera_entity = SceneGraph.create_camera("Camera", 
                                            position=[0.0,0.0,-3.0],
                                            camera=Camera())
    # Add an input to the camera for the viewport
    camera_entity[None] = InputComponent("camera_input",
                                        actions=SceneGraph.DEFAULT_INPUT)
                                            
    # Create a default Geometrty with components 
    geometry_entity = SceneGraph.create_geometry("Geometry", 
                                                position=[0.0,0.0,0.0],
                                                geometry=SceneGraph.DEFAULT_GEOMETRY,
                                                material=SceneGraph.DEFAULT_MATERIAL)
    # Create a default lighting
    light_entity = SceneGraph.create_light(name="Light",
                                            position=[0.0,1.0,0.0])
    
     # Create a default Geometrty with components 
    geometry_entity2 = SceneGraph.create_geometry("Geometry2", 
                                                position=[1.0,0.1,0.0],
                                                geometry=SceneGraph.DEFAULT_GEOMETRY,
                                                material=SceneGraph.DEFAULT_MATERIAL)

    # Create a default Geometrty with components 
    geometry_entity3 = SceneGraph.create_geometry("Geometry3", 
                                                position=[-1.0,0.1,0.0],
                                                geometry=SceneGraph.DEFAULT_GEOMETRY,
                                                material=SceneGraph.DEFAULT_MATERIAL)

    # Add an input to the geometry for the movement of the actor
    geometry_entity3[None] = InputComponent("camera_input2",
                                        actions=SceneGraph.DEFAULT_INPUT)
    
    # Add a hierarchy
    geometry_entity.set_children(children=[geometry_entity2,geometry_entity3])


    # Add entitys to the root object
    root.set_children(children=[camera_entity, geometry_entity, light_entity])

    # Finally return the childs
    return root


if __name__ == '__main__':  
    # Program Start
    print('##############################')
    print('Starting Zero main')
    print('##############################')

    # Parameters to be processed at start    
    # # >>> python main.py -height 800 -width 600 -fps 60
    # >>> python main.py -H 800 -W 600 -F 60
    parameters = { "width"  : {"options" : ["width","W"]  , "default": 800 },
                   "height" : {"options" : ["height","H"] , "default": 600 },
                   "fps"    : {"options" : ["fps","F"]    , "default": 60 }}
    # Read the parameters 
    parameters = get_cmd_parameters(sys.argv, parameters)

    # For testing pourposes create simple uid
    Base.DEFAULT_UUID = Base.COUNTER
    
    # Create the main Scene graph and initialize
    scene_grapgh = SceneGraph(create_scene()).init()

    ###################################################
    #print(scene_grapgh)
    # print(EntityCatalogue.instance())
    print(repr(EntityCatalogue.instance().head(20)))
    ###################################################

    # Start the Engine in Mult-thread Mode
    Thread.MULTI_THREAD = False
    # Create the display (main)
    display_controller = DisplayController(PygameDisplay("Zero Rendering Engine", 
                                           parameters.width, parameters.height))
    # Create the devices
    device_controller = DeviceController(PygameDevice())

    # Create the main Render
    render_controller = RenderController(OpenGLRender())
    # Create the engine and set the display and Devices used
    engine = CoreEngine(display_controller, device_controller, render_controller, 
                        scene_grapgh, fps=parameters.fps, ).init().start()

    # # Running in the main Thread
    # while engine.running:
    #     time.sleep(1/60)
    #     print("Waiting for Implementation..")

    # # End the engine and dispose the memory
    engine.stop(True)
    display_controller.dispose()
    device_controller.dispose()
    render_controller.dispose()

    # Program Ends   
    print('##############################') 
    print('End program')
    print('##############################')
