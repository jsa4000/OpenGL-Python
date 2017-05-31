import os
import sys
import numpy as np

# Add the currnent parent path so it recognize rendegl package entirely
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from e3dpy.core import Base, DataBase, Defaults, DefaultBase

class Geometry(DataBase):
    
    # Reset the current type instance
    # <Geometry,Driver>, geo1, 2e17f67e-c2f0-453e-abad-39ce62fcf4d7
    DEFAULT_TYPE = "Driver"

    defaults = dict( {"deactive":False })

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

class CustomBase(Base):
    def __init__(self, *args, **kwargs):
        # Create default Database object
        super(CustomBase, self).__init__(*args, **kwargs)
        # Not allowed.
        #self.nick = self.nick or None

class Custom(Defaults):
    defaults = dict({"name":"Michael Jordan",
                     "age": 20})
    def __init__(self, *args, **kwargs):
        # Create default Database object
        super(Custom, self).__init__(*args, **kwargs)

class Flexible(Base, Defaults):
    
    defaults = dict( {"nick": "Awesome"})

    def __init__(self, *args, **kwargs):
        """
        """
        # Create default Database object
        #    Note: "self"" it's required
        Base.__init__(self,*args, **kwargs)
        Defaults.__init__(self,*args, **kwargs)

    def __str__(self):
        """Returns the string representation of this instance
        """
        return "<{}> \n {} \n {}".format(self.__class__.__name__, Base.__repr__(self),Defaults.__repr__(self))

    def __repr__(self):
        """Returns the string representation of this instance
        """
        return "{}({} {})".format(self.__class__.__name__, Base.__repr__(self),Defaults.__repr__(self))


class FlexibleDB(DefaultBase):
    defaults = dict( {"nick": "Awesome"})


def check_base_objects():

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

    # Now check the mixed class with base and default

    flexible = Flexible()
    flexible = Flexible("Javier", 12)
    flexible = Flexible("Javier", type="JavierType", nick="jsa000")

    # Flollowing is allowd but you need to include  nick in the constructor
    # since it can not be created inside the class. See the init function
    # at the top for CustomBase
    #flexible = CustomBase("Javier", type="JavierType", nick="jsa000")

    #flexible = Flexible(id=23)
    print(flexible.name)
    print(flexible.nick)
    print(str(flexible))
    print(repr(flexible))

    # From Base packadge use inherited function to simplify
    # it's creation from the multiple-inheritance.

    flexible = FlexibleDB()
    flexible = FlexibleDB("Javier", 12)
    #flexible = FlexibleDB("Javier", type="JavierType", nick="jsa000")

    # Flollowing is allowd but you need to include  nick in the constructor
    # since it can not be created inside the class. See the init function
    # at the top for CustomBase
    #flexible = CustomBase("Javier", type="JavierType", nick="jsa000")

    #flexible = Flexible(id=23)
    print(flexible.name)
    print(flexible.nick)
    print(str(flexible))
    print(repr(flexible))


def Triangle():
     #Create default vertices 4f
    vertices = [ -0.5, -0.5, 0.0, 1.0,
                  0.0,  0.5, 0.0, 1.0,
                  0.5, -0.5, 0.0, 1.0]
    indices = [ 0, 1, 2 ]
    color = [ 1.0, 0.0, 0.0, 1.0,
              0.0, 1.0, 0.0, 1.0,
              0.0, 0.0, 1.0, 1.0]
    uvs = [0.0, 0.0,
           0.5, 1.0,
           1.0, 0.0 ]
    return [vertices, indices, color, uvs]

def check_geometry_objects():

    # Create default Geometry object (empty)
    geometry = Geometry("geo1")
    # This will show the current base object with name, id and type
    print(geometry)
    print(repr(geometry))

    print("FIRST SAMPLE")
    # Add and change new property to the Bata Base object
    # -> Be sure to place active esetter after the getter !!
    print(geometry.active)
    geometry.active = True
    print(geometry.active)

    print("SECOND SAMPLE")
    # Try to configure attributes using the constructor.
    # No way since there not in the kwargs to add them
    # It need
    geometry2 = Geometry("geo1", deactive = True)
    print(geometry2.deactive)
    print(geometry2.active)

    georaw = Triangle()
    # Create the geometry
    geometry = Geometry("geo")
    geometry.addAttrib("Points","P",georaw[0], 4)
    geometry.addAttrib("Prims","I",georaw[1], 3)
    geometry.addAttrib("Points","Cd",georaw[2], 4)
    geometry.addAttrib("Points","UV",georaw[3], 2)

    print(geometry)
    #print(repr(geometry))



if __name__ == '__main__':
    
    # Check base objects function
    #check_base_objects()

    # This is to test some Geometry creation
    check_geometry_objects()




