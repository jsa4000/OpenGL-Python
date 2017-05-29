from collections import OrderedDict as dict
from .base import Base
from .cataloguebase import CatalogueBase

class Component(CatalogueBase):
    """ Component Class
        This is the base component class that all component must
        inherit from.
    """

    # Slots that will admit the base class of Entity class
    __slots__ = ["name","id","type","catalogue","key"]

    # Default dinctionary with properties
    defaults = dict()

    def __init__(self,  *args, **kwargs):
        """This is the main contructor of the class
           Initially set the dafult valiues
        """
        super().__init__(*args,**kwargs)
        # Update the default properties if None
        self._update_properties(Component.defaults, False)
                
    def _update_properties(self, properties, force=True):
        """
        """ 
        # Set defaults if not set in parameters
        for slot in self.__slots__:
            if slot in properties and (force or (not force and getattr(self,slot) is None)):
                setattr(self,slot,properties[slot])
       
    def __del__(self):
        """ Destroy current component
        """
        pass
    
 