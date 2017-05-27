from collections import OrderedDict as dict
from .base import Base

class Component(Base):
    """ Component Class
        This is the base component class that all component show
        inherit from.
    """
    # Global variable to store all the componets created
    catalogue = dict()

    # Slots that will admit the base class of Entity class
    __slots__ = ["name","id", "type", "entity"]

    def __init__(self,  *args, **kwargs):
        """This is the main contructor of the class
            Initially set the dafult valiues
        """
        super().__init__(*args,**kwargs)
        # Add current entity into the main catalogue with components
        Component.catalogue[self.id] = self

    def __del__(self):
        """ Destroy current compoennt
        """
        # Remove current component from the static list
        del Component.catalogue[self.id]
    
 