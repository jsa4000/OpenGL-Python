from collections import OrderedDict as dict

class CatalogDict(object):
    """ Subclass used for catalogue
    """

    @property
    def items(self):
        return self._items

    def __init__(self, catalogue):
        self._catalogue = catalogue
        self._items = dict()

    def __setitem__(self, key, value):
        """Add a new items into the items list.
        """
        self._items[key] = value

    def __getitem__(self, key):
        """Retrieve the items with the given key
        """
        return self._items[key]

    def __contains__(self, key):
        """Returns whether the key is in items or not.
        """
        return key in self._items

    def __iter__(self):
        """Retrieve the items elements using loops
        statements. This usually are more efficent in
        term of memory
        """
        for item in self._items:
            yield item

class Catalogue(object):
    """ Catalogue Class

    This class will be used to store all the ECS system.

    Catalogue will store:
    - Entities created
    - Components created
    - Systems created
    - Mapping between entities, components and Systems

    """
    ENTITY = 0
    COMPONENT = 1
    SYSTEM = 2

    # Catalogues that will be created
    catalogues = [ENTITY, COMPONENT, SYSTEM]

    def __init__(self):
        # Initialize  variables and objects
        self._items = dict()
        for item in Catalogue.catalogues:
            self._items[item] = CatalogDict(self)
    
    def __setitem__(self, key, value):
        """Not alowed to add more items into the catalogue
        """
        pass

    def __getitem__(self, key):
        """Retrieve the items with the given key
        """
        return self._items[key]

    def __contains__(self, key):
        """Returns whether the key is in items or not.
        """
        return key in self._items

    def __iter__(self):
        """Retrieve the items elements using loops
        statements. This usually are more efficent in
        term of memory
        """
        for item in self._items:
            yield item


db = Catalogue()
print(db._items)
db["hola"] = "pepe"
print(db._items)

db[Catalogue.ENTITY]["hola"]="1"
print (db[Catalogue.ENTITY].items)



print(db[Catalogue.COMPONENT])
print(db[Catalogue.SYSTEM])