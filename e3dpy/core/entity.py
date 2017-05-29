from collections import OrderedDict as dict
from utils import *
from cataloguebase import CatalogueTree
from catalogue import CatalogueManager
from component import Component

class Entity(CatalogueTree):
    """ Entity class.

   
    """

    # Slots that allows the instances of Entity class
    __slots__ = ["name","id","catalogue","parent","children","type","key"]

    # This default_type is important to maintain the current type as an
    # "Entity", in case the class will be inherited from another sub-class.
    DEFAULT_TYPE = "Entity"

    def __init__(self, *args, **kwargs):
        """This is the main contructor of the class.

        Initially set the dafult items like name, childs, componets
        and parent.

        Components and Childs could be changed from the inputs,
        the way the are going to be represented. Both childs and
        components will be implemented as a dictionary. This way
        there is no option to add the same components or childs to
        the entity.

        The order of the paramters are the same as the __slots__
        oirder.
        """
        super(Entity,self).__init__(*args,**kwargs)
        # Overwrite the type with DEFAULT_TYPE
        # self.type = Entity.DEFAULT_TYPE
        # # Get the parent
        # self.set_parent(self.parent)
        # # Initialize childs and components dictionaries
        # self.childs = self.childs or dict()
        # Extract current Componets and childs correctly
        #self.add(self.components,self.childs)


print(entity)

comp11 = Transform("Transform01")
comp12 = Transform("Transform02")
comp2 = Camera("Camera01")

entity = Entity("Javier", id = 1234, type = Entity.DEFAULT_TYPE, components = comp11 )
print(repr(entity))
print(entity.transform.name)

 


