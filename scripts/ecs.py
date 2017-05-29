import os
import sys
import numpy as np

# Add the currnent parent path so it recognize rendegl package entirely
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from e3dpy.core import Entity, Component, CatalogueManager

class Transform(Component):
    defaults = dict({"position":[0,1,2,3],
                     "rotation":np.array(range(10))})

class Camera(Component):
    defaults = dict({"mode":0,
                     "orbit":False,
                     "view": np.reshape(range(9),(3,3))})

if __name__ == '__main__':
    # test the current entity

    transform1 = Transform("tranform1",key="name")
    transform2 = Transform("tranform2",key="name")

    camera = Camera("Camera1")
    
    
    print(camera.mode)
    print(camera.orbit)
    print(camera.view)

    entity = Entity("root", catalogue=[transform1,camera])
    entity[None] = transform2.id
    print(repr(entity))

 
    print(CatalogueManager.instance())
    print(CatalogueManager.instance().dataframe.head())


