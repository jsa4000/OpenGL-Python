from collections import OrderedDict as dict
from ..core import Component

class GeometryComponent(Component):
    """ Geometry Component class
    """

    # Defaut type/name the component will have
    DEFAULT_TYPE = "geometry"

    # Default paramters of the component
    defaults = dict({"geometry": None})

    def __init__(self, *args, **kwargs):
        """ Geometry initialization
        """
        super(GeometryComponent,self).__init__(*args, **kwargs)
        
