


class RenderEngine(object):
    """ Render Engine Class
    
    This class will be the core for rendering the scene. This
    will take the scene and render all the renderable elements elements

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

    def __init__(self):
        """ Initialization of the Render Engine
        """
        pass

    def __del__(self):
        """ Dispose and close the render.
        """

    def init():
        """
        """
        pass

    def render():
        """ Process to render the entire scene
        """
        pass

