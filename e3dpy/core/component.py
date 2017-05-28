from collections import OrderedDict as dict
from .base import Base
from .catalogue import CatalogueManager

class Component(Base):
    """ Component Class
        This is the base component class that all component show
        inherit from.
    """

    # Slots that will admit the base class of Entity class
    __slots__ = ["name","id", "type", "entity"]

    def __init__(self,  *args, **kwargs):
        """This is the main contructor of the class
            Initially set the dafult valiues
        """
        super().__init__(*args,**kwargs)
        #Add/bind current instance-entity to the catalog manager
        CatalogueManager.instance()[self.type][self.id] = self
        CatalogueManager.instance().bind(self.entity, self.type, self.id)

    def __del__(self):
        """ Destroy current compoennt
        """
        del CatalogueManager.instance()[self.type][self.id]
    
 