import os
import sys
import time
import math

# Add the currnent parent path so it recognize rendegl package entirely
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from e3dpy.core import Base, CoreEngine, SceneGraph, ThreadBase, CatalogueManager
from e3dpy.model import Camera
from e3dpy.components import InputComponent
from e3dpy.core.utils import get_cmd_parameters
from e3dpy.drivers import Display, Devices


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
    geometry_entity.add(children=[geometry_entity2,geometry_entity3])


    # Add entitys to the root object
    root.add(children=[camera_entity, geometry_entity, light_entity])

    # Finally return the childs
    return root


if __name__ == '__main__':  
    # Program Start
    print('##############################')
    print('Starting e3dpy main')
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
    scene = SceneGraph(create_scene()).init()

    ###################################################
    #print(scene)
    print(CatalogueManager.instance())
    # print(repr(CatalogueManager.instance().head()))
    ###################################################

    # Start the Engine in Mult-thread Mode
    ThreadBase.MULTI_THREAD = False
    # Create the display
    display = Display("e3dpy render engine", parameters.width, parameters.height)   
    # Create the devices
    devices = Devices() 
    # Create the engine and set the display used
    engine = CoreEngine(display, devices, fps=parameters.fps,scene=scene).init().start()

    # Running in the main Thread
    while engine.running:
        time.sleep(1/60)
        print("Waiting for Implementation..")

    # End the engine and dispose the memory
    engine.stop(True)
    display.dispose()

    # Program Ends   
    print('##############################') 
    print('End program')
    print('##############################')
