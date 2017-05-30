import os
import sys
import time
import math

# Add the currnent parent path so it recognize rendegl package entirely
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from e3dpy.core import Engine, SceneGraph
from e3dpy.core.utils import get_cmd_parameters

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

    # Create the main Scene graph
    scene_graph = SceneGraph()

    # Start the Engine in Mult-thread Mode
    Engine.MULTI_THREAD = True
    engine = Engine(parameters.width, parameters.height, parameters.fps, scene_graph)
    engine.start()

    # Do some computation with the scene graph
    counter = 0
    # Running in the main Thread
    while engine.running:
        time.sleep(1/60)
        # print("Waiting for Implementation..")

        # Perform some motion to the object
        sincount = math.sin(counter)
        coscount = math.cos(counter)
        if engine._geo:
            engine._geo.transform.position.x = sincount
            engine._geo.transform.rotation.z = counter*50
            engine._geo.transform.scale = [coscount,coscount,coscount]

        counter += 0.01;

    # End the engine and dispose the memory
    engine.stop(True)
    engine.dispose()

    # Program Ends   
    print('##############################') 
    print('End program')
    print('##############################')
