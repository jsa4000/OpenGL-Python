from collections import OrderedDict as dict
from ..core import Component

class GeometryComponent(Component):
    """ Geometry Component class
    """

    defaults = dict({"geometry": None})

    def __init__(self, *args, **kwargs):
        """ Geometry initialization
        """
        super(GeometryComponent,self).__init__(*args, **kwargs)
        
    



