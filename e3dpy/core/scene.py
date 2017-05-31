from .objects import Entity, Component
from ..components import Camera, Geometry, Material, Render, Transform, Light

__all__ = ['SceneGraph']

class SceneGraph(object):
    """ SceneGraph Base class

    This class will containt all the entities and componets.
    The wat this will work is in a tree base model, where the
    root property will be the main entity and the childs 
    and components will populate the Scene.

    """

    @property
    def root(self):
        """ Get the new root element
        """
        return self._root

    @root.setter
    def root(self, value):
        """ Set the new root element of the Scene Graph
        """
        self._root

    def __init__(self, root=None):
        """ Constructor method for the class
        """
        # Create an empty Entity initial
        self._root = root or None

    def _create_default_scene(self):
        # Create the main roor for all the sub-entities
        root = Entity("root", catalogue = Transform("transform_component"))
       
        # Create the default camera
        camera_entity = Entity("Camera")
        # Create Transform component
        transform_component = Transform("transform_component")
        # Create Camera Component
        camera_component = Camera("camera_component")
        #Add components to the camera entity
        camera_entity[None] = [transform_component, camera_component]
        
        # Create Geometry component
        geometry_component = Geometry("geometry_component")
        # Create Transform component
        transform_component = Transform("transform_component")
        # Create a default Material (key name material > 1)
        material_component_1 = Material("mat1_component", key="name")
        # Create a default Material (key name material > 1)
        material_component_2 = Material("mat2_component", key="name")
        # Create a render component
        render_component = Render("render_component")
        # Create components array
        components = [geometry_component,transform_component, material_component_1, 
                      material_component_2, render_component]
        # Create a default Geometrty with components 
        geometry_entity = Entity("Geometry", catalogue = components)

        # Create a default lighting
        light_entity = Entity("AmbientLight")
        # Create Transform component
        transform_component = Transform("transform_component")
        # Create Transform component
        light_component = Light("light_component")
        # Add components lo light entity
        light_entity[None] = [transform_component, light_component ]

        # Add entitys to the root object
        childs = [camera_entity, geometry_entity, light_entity ]
        root.add(childs)

        # Finally return the childs
        return root

    def init(self, file=None):
        """ Initialize the current Scene.
        If no file is specified then a Default Scene will be created.
        The default scene will be the basic enities and components, like
        camera, basic geometry (with basic materails), lights, etc..
        """
        if (file):
            pass
        else:
            # Create the root object
            self._root = self._create_default_scene()
