import numpy as np
import threading
from ...core import CatalogueManager
from ...core.base.utils import *
from ...components import ( RenderComponent, MaterialComponent, GeometryComponent,
                           LightComponent, CameraComponent, TransformComponent )
from ...drivers.opengl import OpenGLBuffer, OpenGLShader, OpenGLRender, OpenGLTexture

class RenderManager(object):
    """ Render Manager Class
    
    This class will be the core for rendering the scene. This
    will take the scene and render all the renderable elements elements

    Systems will be used as an interface between the components,
    Geometry definition (vertices, primitives, etc..), shaders, material,
    light, etc.. and the way they are manipulated for the drivers (OpenGL).

    This Systems could be for Rendering, physics, manipulation,
    Solvers, etc..

    Also this class will optimize the scene so only the visible and
    active elements will be renderd. Another aspects that will manage
    is the way the scene will be render. This couls called the "Techinque"
    that will be used for the rendering or the passes that will be applied
    for the scene. Also the technique will manager post-processing aspects
    and filtering.

    The render will take into account components like: 
        - Geometry: geometry that will be rendered
        - Transformations: for the model-view matrix
        - Camera: to get the projection matrix, fov, fustrum, etc..
        - Shaders: shaders being using
        - Materials: material or materials being using for the current geometry
        - Textures: textures that 
        - Draw Mode: if the geometry has to be rendered using lines, triangles, etc.
        - Draw Usage: if the geoemtry is static or dynamic.
        - Lights: lighs that are configured in the scene. (And visible)
                - For each light shadows, reflections, etc.. 
        - Environment: if the scene has Cube map, environment map, hdr, etc..
        - High-dynamic-range rendering

    Future Improvements:
        - Global Illumitation
        - Raytracing
        - VDB and Volume rendering support
        - Sub-surface and translucent materials

    
    """

    def __init__(self, engine):
        """ Initialization of the Manager
        """
        # Create a device controller to get the current inputs
        self._engine = engine
        self._render = engine.render

    def __del__(self):
        """ Dispose and close the worker.
        """
        pass

    def init(self):
        """
        """
        return self

    def search(self, component_types):
        """ This function will search for the component types
        specified
        """
         # Get the current Catalog Manager
        df = CatalogueManager.instance().dataframe

        # Get the current entity-components
        entity_component = df.loc[:,component_types].dropna(axis=0)
        result = []
        # Search for the current active ones
        for index in entity_component.index:
            # Get the entity to get if it's the active one
            entity = CatalogueManager.instance().get(index) 
            if entity.active:
                result.append(entity)
        # Finally return the results founded
        return result

    def run(self):
        """ Start the worker process

        This will manage all the rendering process that
        deal with extracting the component and entities that
        will be render into the scene. 

        Also, it will take another components such as lights,
        materials, textures, etc that will be on scene
        """
     
        # Search for the active camera to render
        cameras = self.search(CameraComponent.DEFAULT_TYPE)
        camera = cameras[0][CameraComponent.DEFAULT_TYPE].camera
       
        # Search for all the lights in the scene
        lights = self.search(LightComponent.DEFAULT_TYPE)

        # Search for all the geometry with transforms, render and
        # geometry components. If no shader or material information, 
        # defaults will be provided
        objects = self.search([GeometryComponent.DEFAULT_TYPE,RenderComponent.DEFAULT_TYPE])
        for obj in objects:
            # Get the transformation
            transform = obj[TransformComponent.DEFAULT_TYPE].transform
            # Get the geometry
            geometry = obj[GeometryComponent.DEFAULT_TYPE].geometry
            # Get the material
            material = obj[MaterialComponent.DEFAULT_TYPE].material
            # Bind the things
            # OpenGLBuffer, OpenGLShader, OpenGLRender, OpenGLTexture
            shader = OpenGLShader("default_shader", "./assets/shaders")
            buffer = OpenGLBuffer(geometry, shader)
            render = OpenGLRender()
            texture = OpenGLTexture("./assets/images/texture.png")
            buffer.update()



            render.clear()
            
            # Render all the elements that share the same shader.
            # Use the current Shader configuration
            shader.use()
            # Use the current texture after the shader
            texture.bind(0)
  
            shader.update("WORLD_MATRIX",transform.model)
            shader.update("VIEW_MATRIX",camera.view_matrix())
            shader.update("PROJECTION_MATRIX",camera.projection_matrix())

            # Render the  geometry
            render.render(buffer)
            # End Use the current Shader configuration
            shader.use(False)


        # In this case I have to go through all the components first
        #That satisfy those conditions

       


    
    # @property
    # def vertices(self):
    #     # Check if geometry has been initialized
    #     if self.geometry:
    #         return self.geometry.get_point_attrib(geometry.point.position)
    #     return None

    # @property
    # def normals(self):
    #     # Check if geometry has been initialized
    #     if self.geometry:
    #         return self.geometry.get_point_attrib(geometry.point.normals)
    #     return None

    # @property
    # def textcoords(self):
    #     # Check if geometry has been initialized
    #     if self.geometry:
    #         return self.geometry.get_point_attrib(geometry.point.textcoords)
    #     return None

    # @property
    # def colors(self):
    #     # Check if geometry has been initialized
    #     if self.geometry:
    #         return self.geometry.get_point_attrib(geometry.point.colors)
    #     return None

    # @property
    # def indices(self):
    #     # Check if geometry has been initialized
    #     if self.geometry:
    #         return self.geometry.get_prim_attrib(geometry.primitives.indices)
    #     return None
    
    # @property
    # def indexed(self):
    #     # Check if geometry has been initialized
    #     if self.geometry:
    #         return self.geometry.indexed
    #     return False