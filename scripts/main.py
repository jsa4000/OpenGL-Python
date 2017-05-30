import os
import sys
import time
import math

# Add the currnent parent path so it recognize rendegl package entirely
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from e3dpy.core import CoreEngine, SceneGraph
from e3dpy.core.utils import get_cmd_parameters

if __name__ == '__main__':  
    # Program Start
    print('##############################')
    print('Starting e3dpy main')
    print('##############################')

    # Parameters to be processed at start
    parameters = { "width"  : {"options" : ["width","W"]  , "default": 800 },
                   "height" : {"options" : ["height","H"] , "default": 600 },
                   "fps"    : {"options" : ["fps","F"]    , "default": 60 }}
    # Read the parameters 
    # >>> python main.py -height 800 -width 600 -fps 60
    # >>> python main.py -H 800 -W 600 -F 60
    parameters = get_cmd_parameters(sys.argv, parameters)

    # The idea is to be able to run the Engine e3dpy and at the same
    # time be able to manipulate the geometry, adding new entitys etc.
    # This should be done by using another thread aor another process
    # that share memory or files to be able to update the scene.
    scene = SceneGraph("RootGraph")
  
    engine = CoreEngine(parameters.width, parameters.height, parameters.fps, scene)
    engine.start()


    counter = 0
    # Running in the main Thread
    while engine.is_running:
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
