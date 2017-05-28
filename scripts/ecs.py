import os
import sys

# Add the currnent parent path so it recognize rendegl package entirely
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from e3dpy.core import Entity, Component, CatalogueManager

class Transform(Component):
    pass

class Camera(Component):
    pass

if __name__ == '__main__':
    # test the current entity

    print("COMP1 #1")
    comp1 = Camera("Camera1")
    print(repr(comp1))

    print("ENTITY #1")
    entity_str = {"name":"Entity01","components":[comp1.id,Transform("Transform1")]}
    entity01 = Entity(**entity_str)
    print(repr(entity01))


    print(CatalogueManager.instance())

    """
        I need to know whether entity and components are aware of each other
        Don't know why Catalog isn't compile when includes are redundant..
        Is good to have a repository where all component and entity are stored inside the
        engine as a Singleton class.

        Try to do it.
    """
    

