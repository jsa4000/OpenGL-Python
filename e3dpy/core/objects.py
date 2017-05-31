from collections import OrderedDict as dict
from .utils import *
from .base import Base
from .catalogue import CatalogueManager

__all__ = ['CatalogueBase', 
           'CatalogueTree',
           'Entity', 
           'Component']

class CatalogueBase(Base):
    """ CatalogueBase class.

   # Subclas of CatalogueBase is needed to bind elementes

    Example:

        class Category1(CatalogueBase):
            pass

        class Category2(CatalogueBase):
            pass

        class Category3(CatalogueBase):
            pass

        class Category4(CatalogueBase):
            pass

        class Category5(CatalogueBase):
            pass

        # Change current index for the Catalog Manager
        Base.DEFAULT_UUID = Base.UUID1
        CatalogueManager.DEFAULT_INDEX = "CatalogueBase"
        # Create several catalogues to be manager to CatalogManager singletone
        catalogue1 = CatalogueBase("catalogue1","catalogue1")
        catalogue2 = CatalogueBase("catalogue2","catalogue2")
        catalogue3 = CatalogueBase("catalogue3","catalogue3")
        catalogue4 = CatalogueBase("catalogue4","catalogue4")
        catalogue5 = CatalogueBase("catalogue5","catalogue5")
        # Create several items for the caralogue to bind
        items1 = [None                    , Category2("item12","12"), None                    , Category4("item14","14"), Category5("item15","15") ]
        items2 = [Category1("item21","21"), None                    , Category3("item23","23"), None                    , None                   ]
        items3 = [Category1("item31","31"), None                    , None                    , None                    , Category5("item35","35") ]
        items4 = [Category1("item41","41"), Category2("item42","42"), None                    , Category5("item44","44"), None                   ]

        # Start adding the items into the catalogs
        print("START ADDING CATALOGUE BY CONSTRUCTOR")
        print("---------------------------------------")
        catalogue1 = CatalogueBase("catalogue1","catalogue1",catalogue=items1)
        print(catalogue1.catalogue.keys())
        # Change name instead the type to create the catalogues
        catalogue1 = CatalogueBase("catalogue1","catalogue1",catalogue=items1, key="name")
        print(catalogue1.catalogue.keys())
        print(CatalogueBase.Catalogue.dataframe.head(10))

        # Add catalogue using indexing. Key is irrelevant
        print("ADDING MULTIPLE CATEGORIES BY INDEXING")
        print("---------------------------------------")
        catalogue2[None] = items2
        print(catalogue2.catalogue.keys())
        print(CatalogueBase.Catalogue.dataframe.head(10))
        # Add another category (single element)
        print("ADDING SINGLE A CATEGORY BY INDEXING")
        print("---------------------------------------")
        catalogue2[None] = Category2("item22",22)
        print(catalogue2.catalogue.keys())
        print(CatalogueBase.Catalogue.dataframe.head(10))
        # Remove categories (and bings)
        print("REMOVE SINGLE A CATEGORY BY INDEXING")
        print("---------------------------------------")
        del catalogue2["21"]
        print(catalogue2.catalogue.keys())
        print(CatalogueBase.Catalogue.dataframe.head(10))
        print("REMOVE SINGLE A CATEGORY BY MULTIPLE  INDEXING")
        print("-----------------------------------------------")
        del catalogue1[("12","14")]
        print(catalogue1.catalogue.keys())
        print(CatalogueBase.Catalogue.dataframe.head(10))

        print("REPORT CATALOGUE")

        print(CatalogueBase.Catalogue)
        print(CatalogueBase.Catalogue.dataframe.head(10))
      
    Output:

        ADDING SINGLE A CATEGORY BY INDEXING
        ---------------------------------------
        odict_keys(['category1', 'category3', 'category2'])
                Category2 Category4 Category5 Category1 Category3
        catalogue1        12        14        15       NaN       NaN
        catalogue2        22       NaN       NaN        21        23
        REMOVE SINGLE A CATEGORY BY INDEXING
        ---------------------------------------
        odict_keys(['category3', 'category2'])
                Category2 Category4 Category5 Category1 Category3
        catalogue1        12        14        15       NaN       NaN
        catalogue2        22       NaN       NaN       NaN        23
        REMOVE SINGLE A CATEGORY BY MULTIPLE  INDEXING
        ---------------------------------------
        odict_keys(['category3', 'category2'])
                Category2 Category4 Category5 Category1 Category3
        catalogue1        12        14        15       NaN       NaN
        catalogue2        22       NaN       NaN       NaN        23
        REMOVE SINGLE A CATEGORY BY MULTIPLE  INDEXING
        -----------------------------------------------
        odict_keys(['item15'])
                Category2 Category4 Category5 Category1 Category3
        catalogue1       NaN       NaN        15       NaN       NaN
        catalogue2        22       NaN       NaN       NaN        23
    """

    Catalogue = CatalogueManager.instance()

    # Default key used in the catalogue
    DEFAULT_KEY = "type"

    # Slots that allows instances of Tree class
    __slots__ = ["name","id","type","catalogue","key"]

    def __init__(self, *args, **kwargs):
        """ Initialize CatalogBase Class
        """
        super(CatalogueBase,self).__init__(*args,**kwargs)
        # Init the catalogue
        catalogue = self.catalogue 
        self.catalogue = dict()
        self.key = self.key or CatalogueBase.DEFAULT_KEY
        # Extract current Catalogue and update
        self._update_catalogue(catalogue)
        # Add current instance to the catalog manager
        CatalogueBase.Catalogue[getattr(self,self.key)][self.id] = self

    def _update_catalogue(self, catalogue):
        """ Update catalogue based on the 
        """
        # Create and ordered dict for the components
        self.catalogue.update(self._get_items(catalogue, default_key=self.key,
                                              format_key="{}.lower()"))
        # Bind components to the current entity                                  
        for item in self.catalogue:
            item = self.catalogue[item]
            # Bind current items that are derived from Base class
            if isinstance(item,(Base)):                        
                CatalogueBase.Catalogue.bind(self.id, getattr(item,item.key), item.id)

    def _substract_catalogue(self, catalogue):
        # Remove given items from catalogue
        catalogue_keys = self._get_keys_from_dict(self.catalogue,catalogue)
        for key in catalogue_keys:
            item = self.catalogue[key]
            # Bind current items that are derived from Base class
            if isinstance(item,(Base)):   
                # unbind current component (Not shared component yet)
                CatalogueBase.Catalogue.unbind(self.id, getattr(item,item.key), item.id)
            # Finally remove the item from the dictionary
            del self.catalogue[key]

    def _get_item(self, value):
        """ Check if the current value is already a Base object.
        If the object is nos an instance of a Base object, then
        it will use the catalog to search the current value in the 
        catalog Manager.
        """
        if value and not isinstance(value,(Base)):
            value = CatalogueBase.Catalogue.get(value)
        return value

    def _get_items(self, values, default_key="id", format_key=None):
        """ This function return a dictionary with the parsed
        base objects. The class will detect if the values
        are a list, objects, ids, etc..

        The returned dictionary will be a key, value using the
        default_key of the Base class and the value with the 
        final item. Typical use is set default_key as: "id", "name" 
        or "type". 

        Also there is an option to change the key formats by
        specifying a eval function in the format_key.
        ex. Following eval function lower the keys:
            format_key="{}.lower()"
        """
        result = dict()
        # Check the values are not None initially
        if values is not None:
            # Check if the values is a collection or single value
            if is_collection(values):
                # Iterate through all the values
                for value in values:
                    if value is None:
                        continue
                    value = self._get_item(value)
                    #key = str(getattr(value,default_key))
                    if isinstance(value,(Base)):
                        key = str(getattr(value,value.key))
                    else:
                        key = str(getattr(value,default_key))
                    if (format_key is None):
                        result[key] = value
                    else:
                        result[eval(format_key.format("key"))] = value
            else:
                value = self._get_item(values)
                #key = str(getattr(value,default_key))
                if isinstance(value,(Base)):
                    key = str(getattr(value,value.key))
                else:
                    key = str(getattr(value,default_key))
                if (format_key is None):
                    result[key] = value
                else:
                    result[eval(format_key.format("key"))] = value
        # Return the result
        return result

    def _get_keys_from_dict(self, dict_orig, items):
        """ This function will return the keys for all the items.
        Items should be a value or a collection with ids for the 
        Base instance to return.
        """
        # Check if the values is a collection or single value
        if is_collection(items):
            return [key for key in dict_orig for item in items if item == dict_orig[key].id]
        else:
            return [key for key in dict_orig if items == dict_orig[key].id]

    def __getattr__(self, key):
        """ This function will be used to return the current attr
        of the class. First it will search for the key inside the
        __slots__ of the object. If it's not inside the slots, then
        it will search inside the catalogue dictionary. This will 
        allows to access inside the catalogue just using the key.
        """
        if key in self.__slots__:
            return getattr(self, key)
        else:
            return self.catalogue[key]

    def __setitem__(self, key, value):
        """ Insert the current current values, ifnoring the key
        """
        self._update_catalogue(value)
 
    def __getitem__(self, key):
        """Retrieve the items with the given key
        """
        return self.catalogue[key]

    def __delitem__(self, key):
        """ Remove the items using keys
        """
        self._substract_catalogue(key)       

    def __contains__(self, key):
        """Returns whether the key is in items or not.
        """
        return key in self.catalogue

    def __iter__(self):
        """Retrieve the items elements using loops
        statements. This usually are more efficent in
        term of memory
        """
        for item in self.catalogue:
            yield item
 
    def __del__(self):
        """ Destroy current class
        All the dictiionaries iterates using the key so they can be deleted
        inside the for loop. This warranty no errors during the deletion.
        """
        # Remove all the components
        for key in self.catalogue.keys():
            item = self.catalogue[key]
            # Bind current items that are derived from Base class
            if isinstance(item,(Base)):   
                # unbind current component (Not shared component yet)
                CatalogueBase.Catalogue.unbind(self.id, getattr(item,item.key), item.id)
            # Finally remove the item from the dictionary
            del self.catalogue[key]
        # Remove also the references to the catalog
        del CatalogueBase.Catalog[getattr(self,self.key)][self.id]
        # Finally del base class
        super(CatalogueBase, self).__del__()

    def __str__(self):
        """Returns the string representation of this instance
        """
        #Create components deserialization
        catalogue = [self.catalogue[item] for item in self.catalogue]
        return "{}({},{},{})".format(self.__class__.__name__,self.name, 
                                        self.id, catalogue)

    def __repr__(self):
        """Returns the string representation of this instance
        """
        #Create components deserialization
        catalogue = [self.catalogue[item].id for item in self.catalogue]
        return "{}('{}','{}',{})".format(self.__class__.__name__,self.name, 
                                        self.id, catalogue)


class CatalogueTree(CatalogueBase):
    """ CatalogueBase Tree Base class.

    This is similar as the Catalogue Base, however this allows the 
    possibility to build more complex Structures. In this Case it's
    a Tree based model.

    Addtional parameters has been added such us: parent and children
   
    Example
    
        # Set childs by add function
        Santiago = CatalogueTree("Santiago")
        Javier = CatalogueTree("Javier")
        Alvaro = CatalogueTree("Alvaro")
        Alberto = CatalogueTree("Alberto")
        # Add childs by using objects and ids
        Santiago.add([Javier,Alvaro])
        Santiago.add(Alberto.id)
        print(repr(Santiago))
        print(Santiago.children)

        # Santiago is the root parent = None
        # Javier, Alvaro and Alberto parent is Santiago
        print(Javier.parent.name)
        print(Alvaro.parent.name)
        print(Alberto.parent.name)
        # TRy to remove the parent and set manually set_parent
        print("REMOVE JAVER FROM CHILDS")
        Santiago.remove(Javier.id)
        print(repr(Santiago))
        print(Santiago.children)
        # print(Javier.parent.name) # ERROR!  No parent anymore
        print("ADD JAVER AGAIN")
        Javier.set_parent(Santiago)
        print(repr(Santiago))
        print(Santiago.children)
        print(Javier.parent.name)

        # Set directly childs into the constructor
        # PPlay adding entitys by object or id
        # By id it will look into the catalog of entities
        Mateo = CatalogueTree("Mateo")
        Ines = CatalogueTree("Ines")
        Alberto = CatalogueTree("Alberto", children = [Mateo, Ines.id])
        print(repr(Alberto))
        print(Alberto.children)

    Outputs:

        Entity('Santiago','61045272-17c8-4f4d-8afd-ade78cca0980',[])
        OrderedDict([('84b3a065-a1ec-4908-802e-b264b6dd6ad3', Entity('Javier','84b3a065-a1ec-4908-802e-b264b6dd6ad3',[])), ('648d82a2-faff-4516-9879-cdf3b289c044', Entity('Alvaro','648d82a2-faff-4516-9879-cdf3b289c044',[])), ('2b37a054-f61a-4942-b66d-583d04dfe20e', Entity('Alberto','2b37a054-f61a-4942-b66d-583d04dfe20e',[]))])
        Santiago
        Santiago
        Santiago
        REMOVE JAVER FROM CHILDS
        Entity('Santiago','61045272-17c8-4f4d-8afd-ade78cca0980',[])
        OrderedDict([('648d82a2-faff-4516-9879-cdf3b289c044', Entity('Alvaro','648d82a2-faff-4516-9879-cdf3b289c044',[])), ('2b37a054-f61a-4942-b66d-583d04dfe20e', Entity('Alberto','2b37a054-f61a-4942-b66d-583d04dfe20e',[]))])
        ADD JAVER AGAIN
        Entity('Santiago','61045272-17c8-4f4d-8afd-ade78cca0980',[])
        OrderedDict([('648d82a2-faff-4516-9879-cdf3b289c044', Entity('Alvaro','648d82a2-faff-4516-9879-cdf3b289c044',[])), ('2b37a054-f61a-4942-b66d-583d04dfe20e', Entity('Alberto','2b37a054-f61a-4942-b66d-583d04dfe20e',[])), ('84b3a065-a1ec-4908-802e-b264b6dd6ad3', Entity('Javier','84b3a065-a1ec-4908-802e-b264b6dd6ad3',[]))])
        Santiago

    """

    # Slots that allows the instances based on Tree class
    __slots__ = ["name","id","type","catalogue","key","parent","children"]

    def __init__(self, *args, **kwargs):
        """This is the main contructor of the class.

        """
        super(CatalogueTree,self).__init__(*args,**kwargs)
        # Get the parent
        self._set_parent(self.parent)
        # Initialize children dictionaries
        children = self.children 
        self.children = dict()
        # Extract current Catalogue and update
        self._update_children(children)

    def _set_parent(self, value):
        """ This function will set the current value as the parent

        """
        #Set current parent
        self.parent = self._get_item(value)
        # Aso add self to the parents childs
        if self.parent:
            self.parent.add(children=self)

    def _update_children(self, children):
        """Update children or child into the Tree
        """
        # Create a list for the child
        children = self._get_items(children)
        # Set the parent for the new childs
        for child in children:
            child = children[child]
            # Set the parent if None or not the same
            if child.parent is None or child.parent.id != self.id:
                child.set_parent(self)
        # Finally udate children dictionary
        self.children.update(children)
   
    def _remove_children(self, children):
        # Remove given childs
        child_keys = self._get_keys_from_dict(self.children,children)
        for key in child_keys:
            # Remove parent from the childs since no inheritance anymore
            self.children[key].set_parent(None)
            # Remove current child from the component
            del self.children[key]

    def __del__(self):
        """ Destroy current entity
        All the dictiionaries iterates using the key so they can be deleted
        inside the for loop. This warranty no errors during the deletion.
        """
        # Remove all the childs
        for key in self.children.keys():
            # Finally remove the item from the dictionary (chain?)
            del self.children[key]
        # Check if has parent to unset this child.
        if self.parent is not None:
            # Remove current entity from the parent childs
            parent.remove(children=self.id)
        # Finally del base class
        super(CatalogueTree, self).__del__()

    def set_parent(self, value):
        """ This function will set the current value as the parent
        """
        self._set_parent(value)
        return self
    
    def add(self, children):
        """Add new children into the Tree.
        """
        self._update_children(children)
        return self

    def remove(self, children):
        """ Remove given children from tree
        """
        self._remove_children(children)
        return self

    def __str__(self):
        """Returns the string representation of this instance
        """
        #Create components deserialization
        catalogue = " \n    ".join([str(self.catalogue[item]) for item in self.catalogue])
        children =  " \n   ".join([str(self.children[item]) for item in self.children])
        return " {} ( name:{}, id:{} )\n Catalogue: \n    {}\n Children: \n   {}".format(
                                            self.__class__.__name__,self.name, self.id, 
                                            catalogue, children)

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

    # This default type, it's important to maintain the current type as an
    # "Entity". In case this class will be inherited from another sub-class,
    # this type will be maintained. This si like using __new__ to create
    # Singletone instances.
    DEFAULT_TYPE = "Entity"

    @property
    def active(self):
        """ Get wether the entity is active or not
        """
        return self._active

    @active.setter
    def active(self,value):
        """ Set wether the entity is active or not
        """
        self._active = value

    def __init__(self, *args, **kwargs):
        """This is the main contructor of the class.

        Initially set the dafult items like name, childs, componets
        (as catalogue) and parent. Additionally Entities have
        another paramter such as active or functions to initialize,
        update or destroy all the collecions.

        """
        super(Entity,self).__init__(*args,**kwargs)
        # Set default variables
        self._active = True

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
       