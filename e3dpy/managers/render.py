

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
        """ Initialization of the Worker
        """
        pass

    def __del__(self):
        """ Dispose and close the worker.
        """
        pass

    def init(self):
        """
        """
        return self

    def run(self):
        """ Start the worker process
        """
        print("Render Working")
        return self



    
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