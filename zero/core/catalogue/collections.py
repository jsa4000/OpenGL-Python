from collections import OrderedDict as dict
from .catalogue import Catalogue
from ..base.utils import *
from ..base import Base

__all__ = ['CatalogueDict', 
           'CatalogueTree']

class CatalogueDict(Base):
    """ CatalogueDict class.

    Thisclass allows to create elements that will be added to a
    Catalogue automatically.
    
     The catalaogue will be created for instances o the same
     class type. This means the class that will inherit from
     this metaclass all the instances will share the same Catalog.

     This Catalog could be replaced by a Global one in case all the
     instances need to be in the same Catalog to share the instances.
     In order to do this create a cnew Catalogue in the default one.
     The class will check if this golbal variable (per class) is none
     to know if it needed to create a new one.
     To overwrite the Catalogue overwrite the default catalogue:

    # Main Catalogue to add items and bind
    Catalogue = Catalogue("index_name")

    # DEFAULT_KEY is the default key name that will be used to
    create the catalogue. This is the ke name that will be used
    to create the Groups inside the Catalogue. 

    You can use the name, type, or id to group the elements. This 
    can be done globally to all the instances and Subclasses by
    overrriding the variable:

    DEFAULT_KEY = "name"

    Or it could be given at the constructor, so each instances will
    behave different from the main class.

     transform1 = CatalogueDict("tranform1",key="name")


    # Subclasses of CatalogueDict is needed to bind elements 

    Example:

        class Category1(CatalogueDict): pass
        class Category2(CatalogueDict): pass
        class Category3(CatalogueDict): pass
        class Category4(CatalogueDict): pass
        class Category5(CatalogueDict): pass

        # Change current index for the Catalog Manager
        Base.DEFAULT_UUID = Base.UUID1
        CatalogueManager.DEFAULT_INDEX = "CatalogueDict"
        # Create several catalogues to be manager to CatalogManager singletone
        catalogue1 = CatalogueDict("catalogue1","catalogue1")
        catalogue2 = CatalogueDict("catalogue2","catalogue2")
        catalogue3 = CatalogueDict("catalogue3","catalogue3")
        catalogue4 = CatalogueDict("catalogue4","catalogue4")
        catalogue5 = CatalogueDict("catalogue5","catalogue5")
        # Create several items for the caralogue to bind
        items1 = [None                    , Category2("item12","12"), None                    , Category4("item14","14"), Category5("item15","15") ]
        items2 = [Category1("item21","21"), None                    , Category3("item23","23"), None                    , None                   ]
        items3 = [Category1("item31","31"), None                    , None                    , None                    , Category5("item35","35") ]
        items4 = [Category1("item41","41"), Category2("item42","42"), None                    , Category5("item44","44"), None                   ]

        # Start adding the items into the catalogs
        print("START ADDING CATALOGUE BY CONSTRUCTOR")
        print("---------------------------------------")
        catalogue1 = CatalogueDict("catalogue1","catalogue1",catalogue=items1)
        print(catalogue1.catalogue.keys())
        # Change name instead the type to create the catalogues
        catalogue1 = CatalogueDict("catalogue1","catalogue1",catalogue=items1, key="name")
        print(catalogue1.catalogue.keys())
        print(CatalogueDict.Catalogue.dataframe.head(10))

        # Add catalogue using indexing. Key is irrelevant
        print("ADDING MULTIPLE CATEGORIES BY INDEXING")
        print("---------------------------------------")
        catalogue2[None] = items2
        print(catalogue2.catalogue.keys())
        print(CatalogueDict.Catalogue.dataframe.head(10))
        # Add another category (single element)
        print("ADDING SINGLE A CATEGORY BY INDEXING")
        print("---------------------------------------")
        catalogue2[None] = Category2("item22",22)
        print(catalogue2.catalogue.keys())
        print(CatalogueDict.Catalogue.dataframe.head(10))
        # Remove categories (and bings)
        print("REMOVE SINGLE A CATEGORY BY INDEXING")
        print("---------------------------------------")
        del catalogue2["21"]
        print(catalogue2.catalogue.keys())
        print(CatalogueDict.Catalogue.dataframe.head(10))
        print("REMOVE SINGLE A CATEGORY BY MULTIPLE  INDEXING")
        print("-----------------------------------------------")
        del catalogue1[("12","14")]
        print(catalogue1.catalogue.keys())
        print(CatalogueDict.Catalogue.dataframe.head(10))

        print("REPORT CATALOGUE")

        print(CatalogueDict.Catalogue)
        print(CatalogueDict.Catalogue.dataframe.head(10))
      
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

    # Main Catalogue to use when item is added or bind
    Catalogue = None

    # Default key used ti group the items in the Catalogue
    DEFAULT_KEY = "type"

    # Slots that allows instances of Tree class
    __slots__ = ["name","id","type","items","key"]

    def __new__(cls, *args, **kwargs):
        """ Class Constructor
        This function will create a new catalogue for each class type.
        With Catalogue instancce it could be binded items from another
        catalogue to this one and viceversa.
        """
        if cls.Catalogue is None:
            cls.Catalogue = Catalogue(cls.__name__)
        return super(CatalogueDict, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        """ Initialize CatalogBase Class
        """
        super(CatalogueDict,self).__init__(*args,**kwargs)
        # Init the catalogue
        items = self.items
        self.items = dict()
        self.key = self.key or CatalogueDict.DEFAULT_KEY
        # Extract from parameters and update items instance
        self._update_items(items)
         # Add current instance to the catalogue set
        self.Catalogue[getattr(self,self.key)][self.id] = self

    def _update_items(self, catalogue):
        """ Update catalogue based on the 
        """
        # Create and ordered dict for the components
        self.items.update(self._get_items(catalogue, default_key=self.key,
                                                  format_key="{}.lower()"))
        # Bind components to the current entity                                  
        for item in self.items:
            item = self.items[item]
            # Bind current items that are derived from Base class
            if isinstance(item,(Base)):                        
                self.Catalogue.bind(self.id, getattr(item,item.key), item.id)

    def _remove_items(self, catalogue):
        # Remove given items from catalogue
        catalogue_keys = self._get_keys_from_dict(self.items,catalogue)
        for key in catalogue_keys:
            item = self.items[key]
            # Bind current items that are derived from Base class
            if isinstance(item,(Base)):   
                # unbind current component (Not shared component yet)
                self.Catalogue.unbind(self.id, getattr(item,item.key), item.id)
            # Finally remove the item from the dictionary
            del self.items[key]

    def _get_item(self, value):
        """ Check if the current value is already a Base object.
        If the object is not an instance of a Base object, then
        it will use the catalog to search the current value in the 
        catalog Manager.
        """
        if value and not isinstance(value,(Base)):
            value = self.Catalogue.get(value)
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
                    # This is to suport multiple items if not using ids
                    if isinstance(value,(Base)) and default_key != "id":
                        key = str(getattr(value,value.key))
                    else:
                        key = str(getattr(value,default_key))
                    if (format_key is None):
                        result[key] = value
                    else:
                        result[eval(format_key.format("key"))] = value
            else:
                value = self._get_item(values)
                # This is to suport multiple items if not using ids
                if isinstance(value,(Base)) and default_key != "id":
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
            return self.items[key]

    def __setitem__(self, key, value):
        """ Insert the current current values, ignoring the key
        """
        self._update_items(value)
 
    def __getitem__(self, key):
        """Retrieve the items with the given key
        """
        return self.items[key]

    def __delitem__(self, key):
        """ Remove the items using keys
        """
        self._remove_items(key)       

    def __contains__(self, key):
        """Returns whether the key is in items or not.
        """
        return key in self.items

    def __iter__(self):
        """Retrieve the items elements using loops
        statements. This usually are more efficent in
        term of memory
        """
        for item in self.items:
            yield item
 
    def __del__(self):
        """ Destroy current class
        All the dictiionaries iterates using the key so they can be deleted
        inside the for loop. This warranty no errors during the deletion.
        """
        # Remove all the components
        for key in self.items.keys():
            item = self.items[key]
            # Bind current items that are derived from Base class
            if isinstance(item,(Base)):   
                # unbind current component (Not shared component yet)
                self.Catalogue.unbind(self.id, getattr(item,item.key), item.id)
        # Clean all the items
        self.items.clear()
         # Remove also the references from the catalog
        del self.Catalogue[getattr(self,self.key)][self.id]
        # Finally del base class
        super(CatalogueDict, self).__del__()

    def set_items(self,value):
        """ Add/Modify the current current values, ignoring the key
        It's the same as CatalogueList_instance[None] = Element
        """
        self._update_items(value)
    
    def remove_items(self,key):
        """ Remove the item given the key provided
        """
        self._remove_items(key) 
    
    def get_item(self,key):
        """ get the current itel
        """
        return self.items[key]

    def __str__(self):
        """Returns the string representation of this instance
        """
        #Create components deserialization
        catalogue = [self.items[item] for item in self.items]
        return "{}({},{},{})".format(self.__class__.__name__,self.name, 
                                        self.id, catalogue)

    def __repr__(self):
        """Returns the string representation of this instance
        """
        #Create components deserialization
        catalogue = [self.items[item].id for item in self.items]
        return "{}('{}','{}',{})".format(self.__class__.__name__,self.name, 
                                        self.id, catalogue)


class CatalogueTree(CatalogueDict):
    """ CatalogueDict Tree Base class.

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
    __slots__ = ["name","id","type","items","key","parent","children"]

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
            self.parent.set_children(children=self)

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
            parent.remove_children(children=self.id)
        # Finally del base class
        super(CatalogueTree, self).__del__()

    def set_parent(self, value):
        """ This function will set the current value as the parent
        """
        self._set_parent(value)
        return self
    
    def set_children(self, children):
        """Add new children into the Tree.
        """
        self._update_children(children)
        return self

    def remove_children(self, children):
        """ Remove given children from tree
        """
        self._remove_children(children)
        return self

    def get_children(self, key):
        """ Remove given children from tree
        """
        return self.children[key]

    def __str__(self):
        """Returns the string representation of this instance
        """
        #Create components deserialization
        catalogue = " \n    ".join([str(self.items[item]) for item in self.items])
        children =  " \n   ".join([str(self.children[item]) for item in self.children])
        return " {} ( name:{}, id:{} )\n Catalogue: \n    {}\n Children: \n   {}".format(
                                            self.__class__.__name__,self.name, self.id, 
                                            catalogue, children)
