from collections import OrderedDict as dict
from utils import *
from base import Base
from catalogue import CatalogueManager
from component import Component

class Entity(Base):
    """ Entity class.

    This class should be used for all the entities that will be
    created in the engine. Each entity could have child entities and
    components. Each of these entities will store it parent, so all
    the transformation or updates performed on the parent will also
    affect to its childs.Entities don't have to know anything about 
    its components or it's behaviour.

    The main goal of the entities it's to put together all the functionality
    that the entity we have. The functionality will be instances of
    componentes with particular values for this entity that will change
    depending on the environment or other entities and components. Each
    system created will take into consideration all the components that
    need are needed for the system. ej.

        Entity1 (position1, health1)
        Entity2 (position2, health2)  

        Entities -> Entity1, Entity2
        Components:
         list <position> -> position1 (entity1), position2 (entity2)
         list <heakth>   -> health1  (entity1), health2 (entity2)

         CombatSystem <system> (position, health)

            >>>system.update(timestamp)
            
            -> The combat system will perform the following steps:
            1. Take all entities with both position and health components.
            2. Compare each position (zip) between all entity considering
            a distance between them.
            3. If distance between entities  in length(x-y) < 1 and p(x) > 0.3
            
            >>>entity1.health (entity1) -= 10
            
            -> Do this for all the entities.
 
    For the constructor each entity will have two main parameters, one of them
    will be the name of the entity and an id that will be used to perform
    hash search or anything we want to perform later.
    Also the entity will have two dictionary of elements.
        - components. Componets that will be setup for this enity
        - childs. child entities that will inherit the components
        of this entity and so on.

    Default creation process of an entity:

    >>> print(' This will create a new entity with sub-childs')
    >>> person = Entity("entity01", 0)

    However there is another way to create an Entity by using 
    dictionaries so it can be loaded dinamically inside the engine.

    Following is to create an entity from 0. There is no configuratino already set to this
    entity yet. If there are components or childs already created then they should be
    added also into the configuration.

    To load the components we could have the following scenarios to simplify the things.
    components:[Transform(),Renderable())]  # This will add the following components
    components:["12","3"]  # This will use the componets by id

    There is no multiple inheritance or anything. This is to simplyfy the things

    >>> entity = { name:"Javier", id:"0", components:[Tansform(),Renderable()}

    # If already created components, childs and is child of another entity.
    >>> entity = {name:"Javier", id:"1", parent:"0", components:["12","3"], items:["2","3"]}

    For this reaon entity will have a static dictionary with all the class that will be created.
    Also for the components. Components are given by a name wo they can be loaded dinamically. 

    Finally the entities will be stored using the Scene Manager
    """

    # Slots that allows the instances of Entity class
    __slots__ = ["name","id","components","parent","childs","type"]

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
        self.type = Entity.DEFAULT_TYPE
        # Get the parent
        self.set_parent(self.parent)
        # Initialize childs and components dictionaries
        self.components = self.components or dict()
        self.childs = self.childs or dict()
        # Extract current Componets and childs correctly
        self.add(self.components,self.childs)
        # Add current instance to the catalog manager
        CatalogueManager.instance()[self.type][self.id] = self

    def _get_item(self, value):
        """ Check if the current value is already a Base object.
        If the object is nos an instance of a Base object, then
        it will use the catalog to search the current value in the 
        catalog Manager.
        """
        if not isinstance(value,(Base)):
            value = CatalogueManager.instance().get(value)
        return value

    def _get_items(self, values, default_key="id", format_key=None):
        """ This function return a dictionary with the parsed
        base objects. The class will detect if the values
        are a list, objects, ids, etc..

        The returned dictionary will be a key, value using the
        default_key of the Base class and the value with the 
        final item. Typical use is set default_key as: "id" or
        "type". 

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
                    value = self._get_item(value)
                    key = str(getattr(value,default_key))
                    if (format_key is None):
                        result[key] = value
                    else:
                        result[eval(format_key.format("key"))] = value
            else:
                value = self._get_item(values)
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

    def __del__(self):
        """ Destroy current entity
        All the dictiionaries iterates using the key so they can be deleted
        inside the for loop. This warranty no errors during the deletion.
        """
        # Remove all the components
        for key in self.components.keys():
            component = self.components[key]
            # unbind current component (Not shared component yet)
            CatalogueManager.instance().unbind(component.type, component.id)
            # Finally remove the item from the dictionary
            del self.components[key]
            
        # Remove all the childs
        for key in self.childs.keys():
            # Finally remove the item from the dictionary (chain?)
            del self.childs[key]

        # Check if has parent to unset this child.
        if self.parent is not None:
            # Remove current entity from the parent childs
            parent.remove(childs=self.id)
        # Remove also the references to the catalog
        del CatalogueManager.instance()[self.type][self.id]
        # Finally del base class
        super(Entity, self).__del__()

    def __getattr__(self, key):
        """ This function will be used to return the current attr
        of the entity. First it will search for the key inside the
        __slots__ of the object. If it's not inside the slots, then
        it will search inside the component dictionary. This will 
        allows to access inside the components just using the key.
        """
        if key in self.__slots__:
            return getattr(self, key)
        else:
            return self.components[key]

    def __setitem__(self, key, value):
        """ Not allowed insert component this way
        """
        pass
 
    def __getitem__(self, key):
        """Retrieve the items with the given key
        """
        return self.components[key]

    def __delitem__(self, key):
        """ Remove the component with given id from the entity
        """
        del self.components[key]       

    def __contains__(self, key):
        """Returns whether the key is in items or not.
        """
        return key in self.components

    def __iter__(self):
        """Retrieve the items elements using loops
        statements. This usually are more efficent in
        term of memory
        """
        for component in self.components:
            yield component
 
    def __repr__(self):
        """Returns the string representation of this instance
        """
        #Create components deserialization
        child_list = [child for child in self.childs]   
        component_list = [self.components[component].id for component in self.components]
        return "{}('{}','{}','{}',{},{})".format(self.__class__.__name__, 
                                            self.name, self.id, self.parent,
                                            child_list, component_list)

    def set_parent(self, value):
        """ This function will set the current value as the parent

        """
        #Set current parent
        self.parent = self._get_item(value)
        # Aso add self to the parents childs
        if self.parent:
            self.parent.add(childs=self)
        return self
    
    def add(self, components=None, childs=None):
        """Add new components or childs into the entity.
        """
        if components:
            # Create and ordered dict for the components
            self.components.update(self._get_items(components, default_key="type",
                                                    format_key="{}.lower()"))
            # Bind components to the current entity                                  
            for component in self.components:
                component = self.components[component]                                  
                CatalogueManager.instance().bind(self.id, component.type, component.id)

        if childs:
            # Create a list for the child
            childs = self._get_items(childs)
            # Set the parent for the new childs
            for child in childs:
                child = childs[child]
                # Set the parent if None or not the same
                if child.parent is None or child.parent.id != self.id:
                    child.set_parent(self)
            self.childs.update(childs)

        return self

    def remove(self, components=None, childs=None):
        # Remove given components
        if components:
            components_keys = self._get_keys_from_dict(self.components,components)
            for key in components_keys:
                component = self.components[key]
                # unbind current component (Not shared component yet)
                CatalogueManager.instance().unbind(component.type, component.id)
                # Finally remove the item from the dictionary
                del self.components[key]
        if childs:
            # Remove given childs
            child_keys = self._get_keys_from_dict(self.childs,childs)
            for key in child_keys:
                # Remove parent from the childs since no inheritance anymore
                self.childs[key].set_parent(None)
                # Remove current child from the component
                del self.childs[key]

        return self


class Transform(Component):
    pass

class Camera(Component):
    pass

class Position(Component):
    pass

# Set childs by add function
Santiago = Entity("Santiago")
Javier = Entity("Javier")
Alvaro = Entity("Alvaro")
Alberto = Entity("Alberto")
# Add childs by using objects and ids
Santiago.add(childs=[Javier,Alvaro])
Santiago.add(childs=Alberto.id)
print(repr(Santiago))
print(Santiago.childs)

# Santiago is the root parent = None
# Javier, Alvaro and Alberto parent is Santiago
print(Javier.parent.name)
print(Alvaro.parent.name)
print(Alberto.parent.name)
# TRy to remove the parent and set manually set_parent
print("REMOVE JAVER FROM CHILDS")
Santiago.remove(childs=Javier.id)
print(repr(Santiago))
print(Santiago.childs)
# print(Javier.parent.name) # ERROR!  No parent anymore
print("ADD JAVER AGAIN")
Javier.set_parent(Santiago)
print(repr(Santiago))
print(Santiago.childs)
print(Javier.parent.name)

# Set directly childs into the constructor
# PPlay adding entitys by object or id
# By id it will look into the catalog of entities
Mateo = Entity("Mateo")
Ines = Entity("Ines")
Alberto = Entity("Alberto", childs = [Mateo, Ines.id])
print(repr(Alberto))
print(Albert.childs)





Santiago




print(entity)

comp11 = Transform("Transform01")
comp12 = Transform("Transform02")
comp2 = Camera("Camera01")

entity = Entity("Javier", id = 1234, type = Entity.DEFAULT_TYPE, components = comp11 )
print(repr(entity))
print(entity.transform.name)

 


