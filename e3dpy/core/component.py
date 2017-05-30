from collections import OrderedDict as dict
from .base import Base
from .cataloguebase import CatalogueBase

class Component(CatalogueBase):
    """ Component Class
    This is the base component class that all component must
    inherit from.

    In classes create from this base class propoerties and
    default paramters can be given by the defaults variable

    class Camera(Component):
        defaults = dict({"mode":0,
                         "orbit":False,
                         "view": np.reshape(range(9),(3,3))})
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
        """ Update current properties given in the parameters
        """ 
        for param in properties:
            if force or (not force and param not in self.catalogue):
                 self.catalogue[param] = properties[param] 
       
    
 