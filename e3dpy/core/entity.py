from collections import OrderedDict as dict
from .base import Base
from .catalogue import CatalogueManager
from .component import Component

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
        - items. child entities that will inherit the components
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

    # Slots that will admit the base class of Entity class
    __slots__ = ["name","id","type","parent","items","components"]

    def __init__(self, *args, **kwargs):
        """This is the main contructor of the class
            Initially set the dafult items
        """
        super(Entity,self).__init__(*args,**kwargs)
        # Create a list for the child (not sorted)
        self.items = self.items or set()
        # Create and ordered dict for the components
        self._check_components(self.components)
        #Add current instance to the catalog manager
        CatalogueManager.instance()[self.type][self.id] = self
      
    def _check_components(self, components):
        """ This function will add the components into the entity
        The class will detect if the component is already a component
        of just an id.
        """
        self.components = set()
        for component in components:
            self.add(component)

    def add(self, component):
        """ This function will add new component to the entity.
        The parameter could be:
           1.  component of type <Component>
           2.  id of the component to add
        """
        if isinstance(component,(Component)):
            # Add directly to the dictionary
            self.components.add(component.id)
        else:
            # Search for this component in the component list
            if (component in  CatalogueManager.instance()[self.type]):
                # Add directly to the ldictionary
                self.components.add(Component.catalogue[component].id)
        pass
       
    def remove(self, component):
        """ This function will remove a component to the entity
        """
        if component in self.components:
            # If the component is an Id remove directly using key
            del self.components[component]
        else:
            # if it's a name iterate through all the components
            # And remove all the items with the same name
            for component in self.components:
                if component.id == component:
                     del self.components[component]
  
    def __del__(self):
        """ Destroy current entity
        """
        super(Entity, self).__del__()
                # Check if has parent to unset this child.
        # if (parent is not None):
        #     parent
        # Remove also the 
        del CatalogueManager.instance()[self.type][self.id]

    def __setitem__(self, key, value):
        """Add a new items into the items list.
        """
        self.items[key] = value

    def __getitem__(self, key):
        """Retrieve the items with the given key
        """
        return self.items[key]

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
 
    def __repr__(self):
        """Returns the string representation of this instance
        """
        # Create components deserialization
        # item_list = [id for id in self.items]   
        # component_list = [id for id in self.components]
        # return "{}('{}','{}','{}',{},{})".format(self.__class__.__name__, 
        #                                     self.name, self.id, self.parent,
        #                                     item_list, component_list)
        return super(Entity,self).__repr__()


