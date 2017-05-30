from collections import OrderedDict as dict
from .base import Base
from .cataloguebase import CatalogueBase

class Component(CatalogueBase):
    """ Component Class
        This is the base component class that all component must
        inherit from.
    """

    # Default dinctionary with properties
    defaults = dict()

    def __init__(self,  *args, **kwargs):
        """This is the main contructor of the class
           Initially set the dafult valiues
        """
        super().__init__(*args,**kwargs)
        # Update the default properties if None
        self._update_properties(self.defaults, False)
                
    def _update_properties(self, properties, force=True):
        """
        """ 
        # Set defaults if not set in parameters
        # for slot in self.__slots__:
        #     if slot in properties and (force or (not force and getattr(self,slot) is None)):
        #         setattr(self,slot,properties[slot])
        for param in properties:
            if force or (not force and param not in self.catalogue):
                 self.catalogue[param] = properties[param] 
       
    def __del__(self):
        """ Destroy current component
        """
        pass
    
 