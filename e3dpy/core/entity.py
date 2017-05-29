from collections import OrderedDict as dict
from utils import *
from cataloguebase import CatalogueBase
from catalogue import CatalogueManager
from component import Component

class Entity(CatalogueBase):
    """ Entity class.

   
    """

    # Slots that allows the instances of Entity class
    __slots__ = ["name","id","catalogue","parent","childs","type"]

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
        self.childs = self.childs or dict()
        # Extract current Componets and childs correctly
        self.add(self.components,self.childs)


   
    def __del__(self):
        """ Destroy current entity
        All the dictiionaries iterates using the key so they can be deleted
        inside the for loop. This warranty no errors during the deletion.
        """
        # Remove all the childs
        for key in self.childs.keys():
            # Finally remove the item from the dictionary (chain?)
            del self.childs[key]

        # Check if has parent to unset this child.
        if self.parent is not None:
            # Remove current entity from the parent childs
            parent.remove(childs=self.id)
      
        # Finally del base class
        super(Entity, self).__del__()

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

 


