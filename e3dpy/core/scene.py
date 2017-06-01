from .objects import Entity, Component
from ..components import *
from ..geometry import Triangle, Geometry

__all__ = ['SceneGraph']

class SceneGraph(object):
    """ SceneGraph Base class

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

    def __del__(self):
        """ Destroy all the variables
        """
        pass

    def _create_default_scene(self):
        # Create the main roor for all the sub-entities
        root = Entity("root", catalogue = TransformComponent("transform_component"))
       
        # Create the default camera
        camera_entity = Entity("Camera")
        # Create Transform component
        transform_component = TransformComponent("transform_component")
        # Create Camera Component
        camera_component = CameraComponent("camera_component")
        #Add components to the camera entity
        camera_entity[None] = [transform_component, camera_component]
        
        # Create Geometry component
        geometry_component = GeometryComponent("geometry_component")
        
        
        triangle = Triangle()
        #return {"vertices":triangle[0], "indices":triangle[1], "colors":triangle[2], "textcoords":triangle[3], size=[4,3,4,2]}
        # geometry = Geometry()
        # geometry.add_vertices(triangle[0], 4)
        # geometry.add_indices(triangle[1], 3)
        # geometry.add_colors(triangle[2], 4)
        # geometry.add_textcoords(triangle[3], 2)
        geometry = Geometry(vertices=triangle.vertices, 
                            indices=triangle.indices, 
                            colors=triangle.colors, 
                            textcoords=triangle.textcoords, 
                            size=triangle.size)

        print(str(geometry))



        # Create Transform component
        transform_component = TransformComponent("transform_component")
        # Create a default Material (key name material > 1)
        material_component_1 = MaterialComponent("mat1_component", key="name")
        # Create a default Material (key name material > 1)
        material_component_2 = MaterialComponent("mat2_component", key="name")
        # Create a render component
        render_component = RenderComponent("render_component")
        # Create components array
        components = [geometry_component,transform_component, material_component_1, 
                      material_component_2, render_component]
        # Create a default Geometrty with components 
        geometry_entity = Entity("Geometry", catalogue = components)

        # Create a default lighting
        light_entity = Entity("AmbientLight")
        # Create Transform component
        transform_component = TransformComponent("transform_component")
        # Create Transform component
        light_component = LightComponent("light_component")
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