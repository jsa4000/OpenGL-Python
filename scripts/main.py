import os
import sys
import time
import math

# Add the currnent parent path so it recognize rendegl package entirely
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from e3dpy.core import Base, CoreEngine, SceneGraph, ThreadBase, CatalogueManager
from e3dpy.core.utils import get_cmd_parameters
from e3dpy.controllers import Display

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
    scene = SceneGraph().init()

    ###################################################
    print(scene)
    print(CatalogueManager.instance())
    print(repr(CatalogueManager.instance().head()))
    ###################################################

    # Start the Engine in Mult-thread Mode
    ThreadBase.MULTI_THREAD = False
    # Create the display
    display = Display("e3dpy render engine", parameters.width, parameters.height)    
    # Create the engine and set the display used
    engine = CoreEngine(display,fps=parameters.fps,scene=scene).init().start()

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
