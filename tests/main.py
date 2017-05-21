import os
import sys


# Add the currnent parent path so it recognize rendegl package entirely
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from rendergl.engine import Engine

if __name__ == '__main__':  
    # Program Start
    print('##############################')
    print('Starting rendergl main')
    print('##############################')
    
    # Create Engine instance and Start
    engine = Engine()
    engine.start()

    # Program Ends   
    print('##############################') 
    print('End program')
    print('##############################')
