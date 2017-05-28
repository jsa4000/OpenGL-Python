from collections import OrderedDict as dict
import pandas as pd
import numpy as np

class BaseDict(object):
    """ Subclass used for catalogue

    This catalogue will manage the callback so the catalogue will be able
    to be notify when an element has been added.
    """
    ADDED = 0
    REMOVED = 1
    MODIFIED = 2

    @property
    def items(self):
        return self._items

    @property
    def id(self):
        return self._id

    def __init__(self, id, callback=None):
        """ Initialize all the variables
        """
        self._id = id
        self._items = dict()
        self._callback = callback

    def _notify(self, key, option):
        """Notify when a new element has been added. delegate 
        function to implement has the following arguments:
        >>>  def callback_name(id, key, option):
        Where:
            id: id of the current BaseDict
            key: the item that has been, added, removed or modifed
            option: action performed added, removed or modifed
        """
        if self._callback is not None:
            self._callback(self._id, key, option)

    def __setitem__(self, key, value):
        """Add a new items into the items list.
        """
        if (key in self._items):
            option = BaseDict.MODIFIED
        else:
            option = BaseDict.ADDED
        #Set the current item (added or modified)
        self._items[key] = value
        # Finally callback to the function
        self._notify(key, option)

    def __delitem__(self, key):
         """ Delete current item for the list
         """
         del self._items[key] 
         # Finally notify to the callback
         self._notify(key, BaseDict.REMOVED)

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

    This class will be used to store all the ECS system.

    Catalogue will store:
    - Entities created (depending on the type)
    - Components created (depensding on the type)
    - Systems created ( depending on the type)
    - Mapping between entities, components and Systems
        -> In order to so this Catalogue will check whether an
        element is an Entity or a Component.

    Basic example
    
    >>> ENTITY = "ENTITY"
        >>> COMPONENT_TYPE1 = "COMPONENT_TYPE1"
    >>> COMPONENT_TYPE2 = "COMPONENT_TYPE2"

    >>> db = Catalogue()
    >>> print(db)
    >>> # Don't do anyrhing  > Not allowed
    >>> db[ENTITY] = "pepe"
    >>> print(db)

    >>> # Adding elements
    >>> db[COMPONENT_TYPE1]["comp1"]="Component2"
    >>> db[COMPONENT_TYPE1]["comp2"]="Component2"
    >>> db[ENTITY]["entity"]="Entity2"
    >>> db[COMPONENT_TYPE2]["comp1"]="Component2"
    >>> db[COMPONENT_TYPE2]["comp2"]="Component2"
    >>> db[COMPONENT_TYPE2]["comp3"]="Component3"
    >>> print(db)
    >>> # Modifying elements
    >>> db[COMPONENT_TYPE2]["comp2"]="Component2Mod"
    >>> db[ENTITY]["entity"]="Entity2Mod"
    >>> print(db)
    >>> # Removing elements
    >>> del db[COMPONENT_TYPE2]["comp3"]
    >>> del db[ENTITY]["entity"]
    >>> del db[COMPONENT_TYPE1]["comp2"]
    >>> print(db)

    """
    @property
    def df(self):
        return self._df

    def __init__(self):
        """Initialize  variables and objects
        """
        # Create a catalogue with all the entities and components
        self._items = dict()
        # Create the datafram to map the entity - components
        self._df = pd.DataFrame()
            
    def __setitem__(self, key, value):
        """ Catlogue doesn't allow to create new items manually
        """
        pass

    def __getitem__(self, key):
        """Retrieve the items with the given key
        """
        # Check if the calalogue has been already created.
        if key not in self._items:
            self._items[key] = BaseDict(key, self._callback_items)
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

    def _create_mapping(self, id, key):
        """ This function will create new mapping.
        This function will depend on the id, wheter is an
        element entity or a Component entity.
        """    
        item = self._items[id][key]
        # if isinstance(item, (Entity)):
        #     # Add new row to the dataframe
        #     pass
        # elif isinstance(item, (Component)):
        #     # Add new relation to the dataframe
        #     pass
    
    def _remove_mapping(self, id, key):
        """
        """   
        pass

    def _modify_mapping(self, id, key):
        """
        """  
        pass
    
    def _callback_items(self, id, key, option):
        """ Function call-call back when new element is
        inserted into a list.
        """
        if option == BaseDict.ADDED:
            #print("Element added in {}: {}".format(id,key))
            # Create new mapping based on the added item
            self._create_mapping(id, key)
        elif option == BaseDict.REMOVED:
            #print("Element removed in {}: {}".format(id,key))
            # Create new mapping based on the added item
            self._remove_mapping(id, key)
        else:
            #print("Element modified in {}: {}".format(id,key))
            # Create new mapping based on the added item
            self._modify_mapping(id, key)


class CatalogueManager(object):
    """Create a global instance of a Catalog
    """

    # Singletone instance    
    _catalogue = None
    
    def instance():
        """ Return a singletone instance
        """
        if CatalogueManager._catalogue is None:
            CatalogueManager._catalogue = Catalogue()
        return CatalogueManager._catalogue