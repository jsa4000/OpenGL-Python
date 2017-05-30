from .base import Base
from .catalogue import CatalogueManager
from .component import Component
from .entity import Entity

class SceneGraph(Base):
    """ SceneGraph Base class

    This class will containt all the entities and componets.

    """

    @property
    def root(self):
        return self._root

    def __init__(self, *args, **kwargs):
        """ Constructor method for the class
        """
        super(SceneGraph,self).__init__(*args,**kwargs)
        # Create an empty entity
        self._root = Entity("root")

    