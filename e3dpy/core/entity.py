from collections import OrderedDict as dict
from .utils import *
from .cataloguebase import CatalogueTree
from .catalogue import CatalogueManager
from .component import Component

class Entity(CatalogueTree):
    """ Entity class.

    Example:

        class SubEntity(Entity):
            pass

        entity = Entity("Javier")
        print(repr(entity))
        print(entity.type)

        entity = SubEntity("SubJavier")
        print(repr(entity))
        print(entity.type)
   
    Outputs:

        Entity('Javier','6b8f0077-5c4d-45ff-a6b0-a38d746b79aa',[])
        Entity
        SubEntity('SubJavier','e1ff3be1-f1a9-4e71-9c7c-887f00594136',[])
        Entity

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





 


