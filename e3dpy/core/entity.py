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
    __slots__ = ["name","id","type","parent","childs","components"]

    # This default_type is important to maintain the current type as an
    # "Entity", in case the class will be inherited from another sub-class.
    DEFAULT_TYPE = "Entity"

    def __init__(self, *args, **kwargs):
        """This is the main contructor of the class.
        Initially set the dafult items like childs and componets.
        Components and Childs could be changed from the inputs,
        the way the are going to be represented. Both childs and
        components will be implemented as a dictionary. This way
        there is no option to add the same components or childs to
        the entity.
        """
        super(Entity,self).__init__(*args,**kwargs)
        # Create a list for the child
        self.childs = self._get_items(self.childs)
        # Create and ordered dict for the components
        self.components = self._get_items(self.components, default_key="type")
        # Overwrite the type with DEFAULT_TYPE
        self.type = Entity.DEFAULT_TYPE
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

    def _get_items(self, values, default_key="id"):
        """ This function return a dictionary with the parsed
        base objects. The class will detect if the values
        are a list, objects, ids, etc..

        The returned dictionary will be a key, value using the
        default_key of the Base class and the value with the 
        final item. Typical use is set default_key as: "id" or
        "type"
        """
        result = dict()
        # Check the values are not None initially
        if values is not None:
            # Check if the values is a collection or single value
            if is_collection(values):
                # Iterate through all the values
                for value in values:
                    value = self._get_item(value)
                    result[getattr(value,default_key)] = value
            else:
                value = self._get_item(values)
                result[getattr(value,default_key)] = value

        # Return the result
        return result

    # def _add_child(self, entity):
    #     """Add a new items into the items list.
    #     """
    #     if not isinstance(entity,(Entity)):
    #         entity = CatalogueManager.instance().get(entity)
    #     # Add to the current entity
    #     self.childs.add(entity)
    #     return self

    # def _add_component(self, component):
    #     """ This function will add new component to the entity.
    #     The parameter could be:
    #     1.  Component of type <Component>
    #     2.  id of the component to add
    #     """
    #     if not isinstance(component,(Component)):
    #         component = CatalogueManager.instance().get(component)
    #     # Directly attach to the current component (id)
    #     self.components[component.type] = component
    #     # Bind current component to the current entity
    #     CatalogueManager.instance().bind(self.id, component.type, component.id)

    def __del__(self):
        """ Destroy current entity
        """
        super(Entity, self).__del__()
        # Check if has parent to unset this child.
        # if (parent is not None):
        #     parent
        # Remove also the references to the catalog
        del CatalogueManager.instance()[self.type][self.id]

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
        del self.components[id]       

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

    # def remove(self, id):
    #     """ This function will remove a child to the entity
    #     """
    #     self.childs = filter(lambda child: child.id == entity, self.childs)
    #     return self

class Transform(Component):
    pass

class Camera(Component):
    pass

entity = Entity("Javier", 1234, Entity.DEFAULT_TYPE )
print(entity)

comp11 = Transform("Transform01")
comp12 = Transform("Transform02")
comp2 = Camera("Camera01")

entity = Entity("Javier", id = 1234, type = Entity.DEFAULT_TYPE, components = comp11 )
print(entity)


