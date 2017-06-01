from collections import OrderedDict as dict
from ..core import Component

class GeometryComponent(Component):
    """ Geometry Component class

        This component will be used as an interface between 
        the Geometry definition (vertices, primitives, etc..)
        and the systems that will use Geometry for some pourpose.

        This Systems could be for Rendering, physics, manipulation,
        Solvers, etc..

    """

    # Defaut type/name the component will have
    DEFAULT_TYPE = "geometry"

    # Default paramters of the component
    defaults = dict({"geometry": None})

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

    def __init__(self, *args, **kwargs):
        """ Geometry initialization
        """
        super(GeometryComponent,self).__init__(*args, **kwargs)
        
