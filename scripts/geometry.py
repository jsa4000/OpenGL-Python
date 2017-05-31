import os
import sys
import numpy as np

# Add the currnent parent path so it recognize rendegl package entirely
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from e3dpy.core import Base, DataBase, Defaults

class CustomBase(Base):
    def __init__(self, *args, **kwargs):
        # Create default Database object
        super(CustomBase, self).__init__(*args, **kwargs)

class Custom(Defaults):
    defaults = dict({"name":"Michael Jordan",
                     "age": 20})
    def __init__(self, *args, **kwargs):
        # Create default Database object
        super(Custom, self).__init__(*args, **kwargs)

class Flexible(Base, Defaults):
    
    defaults = dict( {"my_name":"Anything"})

    def __init__(self, *args, **kwargs):
        """
        """
        # Create default Database object
        Base.__init__(*args, **kwargs)
        Defaults.__init__(*args, **kwargs)

class Geometry(DataBase):
    
    # Reset the current type instance
    # <Geometry,Driver>, geo1, 2e17f67e-c2f0-453e-abad-39ce62fcf4d7
    DEFAULT_TYPE = "Driver"

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        """ Only be sure to place setter after the getter so python
        can recognize the attribute to set
        """
        self._active = value
        self.deactive = not self._active

    def __init__(self, *args, **kwargs):
        """ Default initialization for the class that will create
        __slots__ default parameters and let Geometry class create thir owns
        after the super(Geometry, self).__init__(*args, **kwargs)
        """
        # Create default Database object
        super(Geometry, self).__init__(*args, **kwargs)
        # This works great since I'm not passing the variable
        # Through the constructor
        self._active = False
        self.deactive = self.deactive or not self._active


if __name__ == '__main__':
    # This is to test some Geometry creation

    # # Create default Geometry object (empty)
    # geometry = Geometry("geo1")
    # # This will show the current base object with name, id and type
    # print(geometry)
    # print(repr(geometry))


    # print("FIRST SAMPLE")
    # # Add and change new property to the Bata Base object
    # # -> Be sure to place active esetter after the getter !!
    # print(geometry.active)
    # geometry.active = True
    # print(geometry.active)

    # print("SECOND SAMPLE")
    # # Try to configure attributes using the constructor.
    # # No way since there not in the kwargs to add them
    # # It need
    # geometry2 = Geometry("geo1", deactive = True)
    # print(geometry2.deactive)
    # print(geometry2.active)

    # Check Custom when properties set in constructir 
    # or using defaults insted

    flexible = Custom( my_name = "Javier") # Ignore not in default
    flexible = Custom(age = 34)
    print(flexible.name)
    print(flexible.age)
    print(str(flexible))
    print(repr(flexible))

    # Check CustomBase when properties set in constructir or not
    # or using named parameters insted

    flexible = CustomBase()
    flexible = CustomBase("Javier", 12)
    flexible = CustomBase("Javier", type="JavierType")
    flexible = CustomBase(id=23)
    print(flexible.name)
    #print(flexible.age)
    print(str(flexible))
    print(repr(flexible))


