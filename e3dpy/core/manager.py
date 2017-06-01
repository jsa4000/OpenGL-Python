from .object import Entity, Component
from .transform import Transform
from ..components import *
from ..model import (Settings, Geometry, Camera, Material, Input)

__all__ = ['SceneManager']

class SceneManager(object):
    """ SceneManager Base class

    This class will containt all the entities and componets.
    The wat this will work is in a tree base model, where the
    root property will be the main entity and the childs 
    and components will populate the Scene.

    In Scene graph the default scenario is created as follows:

         # Create the main roor for all the sub-entities
        root = Entity("root", catalogue = Transform("transform_component"))
       
        # Create the default camera
        camera_entity = Entity("Camera")
        # Create Transform component
        transform_component = Transform("transform_component")
        # Create Camera Component
        camera_component = Camera("camera_component")
     
        ...

        # Add components lo light entity
        light_entity[None] = [transform_component, light_component ]

        # Add entitys to the root object
        childs = [camera_entity, geometry_entity, light_entity ]
        root.add(childs)

    Output:

        ---------------------------------------------------------------------
        Entity ( name:root, id:3 )
        Components: 
            Transform ( name:transform_component, id:2 )
        Children: 
        ---------------------------------------------------------------------
            Entity ( name:Camera, id:4 )
            Components: 
                Transform ( name:transform_component, id:5 )
                Camera ( name:camera_component, id:6 )
            Children: 
        ---------------------------------------------------------------------
            Entity ( name:Geometry, id:12 )
            Components: 
                Geometry ( name:geometry_component, id:7 )
                Transform ( name:transform_component, id:8 )
                Material ( name:mat1_component, id:9 )
                Material ( name:mat2_component, id:10 )
                Render ( name:render_component, id:11 )
            Children: 
        ---------------------------------------------------------------------
            Entity ( name:AmbientLight, id:13 )
            Components: 
                Transform ( name:transform_component, id:14 )
                Light ( name:light_component, id:15 )
            Children: 

    """

    # Set the dafult geometry in scene manger to add
    DEFAULT_GEOMETRY = Settings.default_geometry
    DEFAULT_MATERIAL = Settings.default_material
    DEFAULT_INPUT = Settings.default_input

    @property
    def root(self):
        """ Get the new root element
        """
        return self._root

    @root.setter
    def root(self, value):
        """ Set the new root element of the Scene Graph
        """
        self._root = value
        return self

    @property
    def camera(self):
        """ Default active Camera component
        """
        return self._camera

    @camera.setter
    def camera(self, value):
        """ Default active Camera component
        """
        self._camera = None

    def __init__(self, root=None):
        """ Constructor method for the class
        """
        # Create an empty Entity initial
        self._root = root or None
        self._camera = None

    def __del__(self):
        """ Destroy all the variables
        """
        pass

    def _create_default_scene(self):
        # Create the main roor for all the sub-entities
        root = SceneManager.create_empty("Root",position=[0.0,0.0,0.0])
       
        # Create the default camera
        camera_entity = SceneManager.create_camera("Camera", 
                                                position=[0.0,0.0,-3.0],
                                                camera=Camera())
        # Add an input to the camera for the viewport
        camera_entity[None] = InputComponent("camera_input",
                                            input=SceneManager.DEFAULT_INPUT)
                                                
        # Create a default Geometrty with components 
        geometry_entity = SceneManager.create_geometry("Geometry", 
                                                    position=[0.0,0.0,0.0],
                                                    geometry=SceneManager.DEFAULT_GEOMETRY,
                                                    material=SceneManager.DEFAULT_MATERIAL)
        # Create a default lighting
        light_entity = SceneManager.create_light(name="Light",
                                               position=[0.0,1.0,0.0])
      
        # Add entitys to the root object
        root.add(children=[camera_entity, geometry_entity, light_entity])

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
            #Reset current scene and create the default root object
            self._root = self._create_default_scene()
        return self

    def create_empty(name="Empty", position=None, active=True):  
        """ Create an empty object with only transformation
        """
        return Entity(name, active=active,catalogue=TransformComponent("transform_component",
                                                        transform=Transform(position)))

    def create_geometry(name="Geometry", position=None, geometry=None, material=None, active=True):
        """ Create a default geometry
        """
        # Create Geometry component (triangle by default)
        geometry_component = GeometryComponent("geometry_component",geometry=geometry)
        # Create Transform component
        transform_component = TransformComponent("transform_component",
                                                transform=Transform(position))
       # Create a default Material (key name material > 1)
        material_component = MaterialComponent("material_component",material=material)
        # Create a render component
        render_component = RenderComponent("render_component")
        # Create components array
        components = [geometry_component,transform_component, 
                      material_component,render_component]
        # Create a default Geometrty with components 
        geometry_entity = Entity(name,catalogue=components,active=active)
        return geometry_entity

    def create_camera(name="Camera", position=None, camera=None, active=True):
        """ Create a default camera
        """
         # Create the default camera
        camera_entity = Entity("Camera",active=active)
        # Create Transform component
        transform_component = TransformComponent("transform_component",
                                                transform=Transform(position))
        # Create Camera Component
        camera_component = CameraComponent("camera_component", camera=camera)
        #Add components to the camera entity
        camera_entity[None] = [transform_component, camera_component]
        return camera_entity

    def create_light(name="Light", position=None, light=None, active=True):
        """ Create a default light
        """
          # Create a default lighting
        light_entity = Entity(name,active=active)
        # Create Transform component
        transform_component = TransformComponent("transform_component",
                                                transform=Transform(position))
        # Create Transform component
        light_component = LightComponent("light_component", light=light)
        # Add components lo light entity
        light_entity[None] = [transform_component, light_component]
        return light_entity

    def _repr(self, node, level):
       """ This function will print the scene entirely
       """
       zeros = " " * (level * 3)
       result = "---------------------------------------------------------------------\n"
       result += zeros + " {} ( name:{}, id:{} )\n".format(node.type,
                                                        node.name, node.id)
       #result += "----------------------------------------------------------------------\n"
       result +=  zeros + "  Components: \n"
       for item in node.catalogue:
            item = node.catalogue[item]
            result +=  zeros + "      {} ( name:{}, id:{} )\n".format(item.type,
                                                                   item.name, item.id)
       #result += "---------------------------------------------------------------------\n"
       result +=  zeros + "  Children: \n"     
       for child in node.children:
            result += self._repr(node.children[child], level+1)
      
       return result 

    def __repr__(self):
        """ Get current representation of the scene graph
        """
        return self._repr(self._root,0)