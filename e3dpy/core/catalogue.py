from collections import OrderedDict as dict
import pandas as pd
import numpy as np

class BaseDictionay(object):
    """ BaseDictionay class.
    
    This is the dictionaty used by Catalogue class. The idea is to be able 
    store different type of data inside the main catalogue instance. 
    Since it's a Sorted Dictionary all the data main remain in order 
    and the performances are better than standard lists.

    This catalogue will manage the callbacks so the catalogue will be able
    to know whether an element has been added, removed or modified.

    Each BaseDictionay has a (name) and a function (callback) when action is 
    performed inside the dictionary.

    The function callback need to be implemented as follows:
        def callback_name(id, key, option):
 
    Where:
        name: name of the current BaseDictionay
        key: the item that has been, added, removed or modifed
        option: action performed added, removed or modifed
    """
    ADDED = 0
    REMOVED = 1
    MODIFIED = 2

    @property
    def items(self):
        return self._items

    @property
    def name(self):
        return self._name

    def __init__(self, name, callback=None):
        """ Initialize all the variables
        """
        self._name = name
        self._items = dict()
        self._callback = callback

    def _notify(self, key, option):
        """Notify when a new element has been added.  
        """
        if self._callback is not None:
            self._callback(self._name, key, option)

    def __setitem__(self, key, value):
        """Add a new items into the items list.
        """
        if key in self._items:
            option = BaseDictionay.MODIFIED
        else:
            option = BaseDictionay.ADDED
        #Set the current item (added or modified)
        self._items[key] = value
        # Finally callback to the function
        self._notify(key, option)

    def __delitem__(self, key):
         """ Delete current item for the list
         """
         del self._items[key] 
         # Finally notify to the callback
         self._notify(key, BaseDictionay.REMOVED)

    def __getitem__(self, key):
        """Retrieve the items with the given key
        """
        return self._items[key]

    def __contains__(self, key):
        """Returns whether the key is in items or not.
        """
        return key in self._items

    def __iter__(self):
        """Retrieve the items elements using loops statements. 
        This usually are more efficent in terms of memory
        """
        for item in self._items:
            yield item

    def __str__(self):
        """ Build the default function to represent the catalogue
        user friendly
        """
        result = ""
        for index, item in enumerate(self._items):
            result += "   item {} <{}> : {} \n".format(index, item, str(self._items[item]))
        return result

class Catalogue(object):
    """ Catalogue Class

    This class will be used to store all the entities, components
    and any other type of data. The class will manage different
    dictionaries depending on the types to be stored. One of these
    types need to be the index for the main catalogue. The index
    is given in the contructor of the class, where index is the name
    of the dcitionaries that will be used as an index.

    However this Class could be used for any other pourpose
    like managing resources, references or any map-reduce 
    systems that requires a Hastable to store some data
    and make relation between data

    Basically, Catalogue will store:
    - Entities created (depending on the type)
    - Components created (depensding on the type)
    - Systems created ( depending on the type)
    - Mapping between entities, components and Systems
        
    The maping between each data will be performed by
    calling the link function of catalogue. This is to
    link entities and components.

    Basic example

    # Test
    catalogue_index = "Entity"
    catalogue_col1 = "Transform"
    catalogue_col2 = "Position"
    catalogue_col3 = "Health"
    catalogue_col4 = "Renderable"

    entities = ["entity01", "entity02", "entity03", "entity04","entity05"]
    components = [catalogue_col1, catalogue_col2, catalogue_col3,catalogue_col4]
    entity01_comp = ["Transform01", None        , None       ,  "Renderable01" ]
    entity02_comp = ["Transform02", None        , "Health02" ,  "Renderable02" ]
    entity03_comp = ["Transform03", "Position03", None       ,  None           ]
    entity04_comp = ["Transform04", "Position04", "Health04" ,  None           ]
    entity05_comp = ["Transform05", None        , "Health05" ,  "Renderable05" ]

    entities_comp =  [entity01_comp, entity02_comp, entity03_comp, entity04_comp, entity05_comp ]

    # Create the main Catalogue
    catalogue = Catalogue(index = catalogue_index)
    # Add all the entities into the catalogue
    for index, entity in enumerate(entities):
        # Add current entity
        catalogue[catalogue_index][entity] = entity
        # Add component for the current entity
        for cindex, ctype in enumerate(components):
            comp_instance = entities_comp[index][cindex]
            if comp_instance is not None:
                # Add current component to the catalogue
                catalogue[ctype][comp_instance] = comp_instance
                # Bind the current comp with it's entity
                catalogue.bind(entity, ctype, comp_instance)

    print(catalogue)
    print(catalogue.dataframe.head(10))

    Output:

    ITEM Entity:
        item 0 <entity01> : entity01 
        item 1 <entity02> : entity02 
        item 2 <entity03> : entity03 
        item 3 <entity04> : entity04 
        item 4 <entity05> : entity05 
    ITEM Transform:
        item 0 <Transform01> : Transform01 
        item 1 <Transform02> : Transform02 
        ...
        item 1 <Health04> : Health04 
        item 2 <Health05> : Health05 
    ITEM Position:
        item 0 <Position03> : Position03 
        item 1 <Position04> : Position04 

    Dataframe:

                Transform    Renderable    Health    Position
    entity01  Transform01  Renderable01       NaN         NaN
    entity02  Transform02  Renderable02  Health02         NaN
    entity03  Transform03           NaN       NaN  Position03
    entity04  Transform04           NaN  Health04  Position04
    entity05  Transform05  Renderable05  Health05         NaN

    # Delete and index entity
    del catalogue[catalogue_index]["entity01"]
    del catalogue[catalogue_index]["entity04"]
    print(catalogue.dataframe.head(10))
    # Delete components
    del catalogue[catalogue_col1]["Transform02"]
    del catalogue[catalogue_col4]["Renderable05"]
    del catalogue[catalogue_col2]["Position04"]

                Transform Renderable Health    Position
    entity02          NaN        NaN    NaN         NaN
    entity03  Transform03        NaN    NaN  Position03
    entity05          NaN        NaN    NaN         NaN


    """
    @property
    def dataframe(self):
        return self._dataframe

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    def __init__(self, index):
        """Initialize  variables and objects.

        """
        # Create a catalogue with all the entities and components
        self._items = dict()
        self._index = index
        # Create the datafram to map the entity - components
        self._dataframe = pd.DataFrame()
            
    def __setitem__(self, key, value):
        """ Catlogue doesn't allow to create new items manually
        """
        pass

    def __getitem__(self, key):
        """Retrieve the items with the given key
        """
        # Check if the calalogue has been already created.
        if key not in self._items:
            self._items[key] = BaseDictionay(key, self._callback_items)
        return self._items[key]

    def __contains__(self, key):
        """Returns whether the key is in items or not.
        """
        return key in self._items

    def __iter__(self):
        """Retrieve the items elements using loops statements. 
        This usually are more efficent in terms of memory
        """
        for item in self._items:
            yield item

    def __str__(self):
        """ Build the default function to represent the catalogue
        user friendly
        """
        result = ""
        for key, value in self._items.items():
            result += "ITEM {}:\n".format(key)
            result += str(self._items[key])
        return result

    def __repr__(self):
        """ Perpare the catalogue to be represented as object to
        be saved and loaded later on.
        """
        pass

    def _subitem_added(self, key, subitem):
        """ Iten has been added
        """    
        #print("Element added in {}: {}".format(id,key))
        pass
    
    def  _subitem_removed(self, key, subitem):
        """ Item has been removed from the Dict
        """   
        #print("Element removed in {}: {}".format(id,key))
        if key is self._index:
            # Remove the current row
            self._dataframe.drop(subitem, inplace=True)
        else:
            # Remove the element from the curren col
            self.unbind(key, subitem)

    def _subitem_modified(self, key, subitem):
        """ Item has been modified
        """  
        #print("Element modified in {}: {}".format(id,key))
        pass
    
    def _callback_items(self, key, subitem, option):
        """ Function call-call back when new element is
        inserted into a list.
        """
        if option == BaseDictionay.ADDED:
            # Create new mapping based on the added item
            self._subitem_added(key, subitem)
        elif option == BaseDictionay.REMOVED:
            # Create new mapping based on the added item
            self._subitem_removed(key, subitem)
        else:
            # Create new mapping based on the added item
            self._subitem_modified(key, subitem)

    def get(self, subitem):
        """ This function will look for the current value
        inside all the items stored
        """
        for item in self:
            if (subitem in self[item]):
                return self[item][subitem]
            
    def bind(self, index, column, subitem):
        """ This function will map the current subitem with the
        given index and col.
        """
        # Bind the current index, col using dataframe
        if self._dataframe.empty:
            # Add the current data into the attributes frame
            self._dataframe = pd.DataFrame([subitem], index = [index], columns=[column])
        else:
            # Add the current data into the attributes frame
            self._dataframe.loc[index,column] = subitem
    
    def unbind(self, column, subitem):
        """ This function will unbind the current key from the catalogue.
        """
        # Remove the element from the curren col
        self._dataframe[self._dataframe[column]==subitem] = np.NaN
        
class CatalogueManager(object):
    """Create a global instance of a Catalog
    """

    # Singletone instance    
    _catalogue = None

    # Main data index to use within the catalog
    index = "Entity"
    
    def instance():
        """ Return a singletone instance
        """
        if CatalogueManager._catalogue is None:
            CatalogueManager._catalogue = Catalogue(Catalogue.index)
        return CatalogueManager._catalogue

