import os
import sys


# Add the currnent parent path so it recognize rendegl package entirely
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from e3dpy.core import Engine

if __name__ == '__main__':  
    # Program Start
    print('##############################')
    print('Starting rendergl main')
    print('##############################')


    # The idea is to be able to run the Engine e3dpy and at the same
    # time be able to manipulate the geometry, adding new entitys etc.
    # This should be done by using another thread aor another process
    # that share memory or files to be able to update the scene.

    

    # Create Engine instance and Start
    engine = Engine()
    engine.start()

    # Program Ends   
    print('##############################') 
    print('End program')
    print('##############################')
