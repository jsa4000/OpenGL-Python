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

    Example 2: Entities and Components

        transform = Transform("tranform1")
        print(transform.catalogue)
        print(transform.position)

        camera = Camera("Camera1")
        print(camera.mode)
        print(camera.orbit)
        print(camera.view)

        entity = Entity("root", catalogue=[transform,camera])
        print(repr(entity))

        entity = Entity("root")
        entity[None] = Transform("tranform1")
        entity[None] = camera.id
        print(repr(entity))

        print(CatalogueManager.instance())
        print(CatalogueManager.instance().dataframe.head())

    Output:

        OrderedDict([('position', [0, 1, 2, 3]), ('rotation', array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))])
        [0, 1, 2, 3]
        0
        False
        [[0 1 2]
        [3 4 5]
        [6 7 8]]
        Entity('root','4b7b2568-6001-4a5d-8ac6-14be43214e16',['00471c63-0f1d-44a5-a5fe-8159606a6589', 'b5037de0-95cb-48a0-9e2f-e0b887af7a47'])
        Entity('root','d476e541-f1a6-432f-b385-b424045285b3',['174e81bb-330f-4f7c-95f3-e75cb89524ab', 'b5037de0-95cb-48a0-9e2f-e0b887af7a47'])
        ITEM Transform:
        item 0 <00471c63-0f1d-44a5-a5fe-8159606a6589> : <Transform,Transform>, tranform1, 00471c63-0f1d-44a5-a5fe-8159606a6589 
        item 1 <174e81bb-330f-4f7c-95f3-e75cb89524ab> : <Transform,Transform>, tranform1, 174e81bb-330f-4f7c-95f3-e75cb89524ab 
        ITEM Camera:
        item 0 <b5037de0-95cb-48a0-9e2f-e0b887af7a47> : <Camera,Camera>, Camera1, b5037de0-95cb-48a0-9e2f-e0b887af7a47 
        ITEM Entity:
        item 0 <4b7b2568-6001-4a5d-8ac6-14be43214e16> : <Entity,Entity>, root, 4b7b2568-6001-4a5d-8ac6-14be43214e16 
        item 1 <d476e541-f1a6-432f-b385-b424045285b3> : <Entity,Entity>, root, d476e541-f1a6-432f-b385-b424045285b3 
                                                                        Transform  \
        4b7b2568-6001-4a5d-8ac6-14be43214e16  00471c63-0f1d-44a5-a5fe-8159606a6589   
        d476e541-f1a6-432f-b385-b424045285b3  174e81bb-330f-4f7c-95f3-e75cb89524ab   
                                                                            Camera  
        4b7b2568-6001-4a5d-8ac6-14be43214e16  b5037de0-95cb-48a0-9e2f-e0b887af7a47  
        d476e541-f1a6-432f-b385-b424045285b3  b5037de0-95cb-48a0-9e2f-e0b887af7a47 

    
    Instead using key = "type", catalogue support to add more than one category by changeing the key
    in the contructor. This wat the Component will be binded by name instead.

    Example

        transform1 = Transform("tranform1",key="name")
        transform2 = Transform("tranform2",key="name")

        camera = Camera("Camera1")

        entity = Entity("root", catalogue=[transform1,camera])
        entity[None] = transform2.id
        print(repr(entity))

    
        print(CatalogueManager.instance())
        print(CatalogueManager.instance().dataframe.head())

    Output

        ITEM tranform1:
        item 0 <4aebc2f4-b54a-4364-b633-16f9ed8fad9c> : <Transform,Transform>, tranform1, 4aebc2f4-b54a-4364-b633-16f9ed8fad9c 
        ITEM tranform2:
        item 0 <ff89bc9b-cd91-4ac9-ac7c-ff355576add0> : <Transform,Transform>, tranform2, ff89bc9b-cd91-4ac9-ac7c-ff355576add0 
        ITEM Camera:
        item 0 <790a1400-f794-4316-ab8e-ad43c276059d> : <Camera,Camera>, Camera1, 790a1400-f794-4316-ab8e-ad43c276059d 
        ITEM Entity:
        item 0 <815d3b9c-a111-414d-9650-c21e67b37729> : <Entity,Entity>, root, 815d3b9c-a111-414d-9650-c21e67b37729 

                                                                        tranform1  \
        815d3b9c-a111-414d-9650-c21e67b37729  4aebc2f4-b54a-4364-b633-16f9ed8fad9c   
                                                                            Camera  \
        815d3b9c-a111-414d-9650-c21e67b37729  790a1400-f794-4316-ab8e-ad43c276059d   
                                                                        tranform2  
        815d3b9c-a111-414d-9650-c21e67b37729  ff89bc9b-cd91-4ac9-ac7c-ff355576add0  

    """

    # This default_type is important to maintain the current type as an
    # "Entity", in case the class will be inherited from another sub-class.
    DEFAULT_TYPE = "Entity"

    def active(self):
        return self._active

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
        # Set default variables
        self._active = True





 


