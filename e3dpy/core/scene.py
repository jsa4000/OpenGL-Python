from .base import Base
from .catalogue import CatalogueManager
from .component import Component
from .entity import Entity

class SceneGraph(Base):
    """ SceneGraph Base class

    This class will containt all the entities and componets.
    The wat this will work is in a tree base model, where the
    root property will be the main entity and the childs 
    and components will populate the Scene.

    """

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root

    def __init__(self, *args, **kwargs):
        """ Constructor method for the class
        """
        super(SceneGraph,self).__init__(*args,**kwargs)
        # Create an empty Entity initial
        self._root = Entity("root")

    def init(self, file=None):
        """
        """
        pass

   