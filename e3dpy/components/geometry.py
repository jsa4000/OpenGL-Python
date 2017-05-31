from collections import OrderedDict as dict
from ..core import Component
from ..drivers.geometry import DrawMode, UsageMode

class Geometry(Component):
    """ Geometry Component class
    """

    defaults = dict({"geometry": None,
                     "mode" : DrawMode.triangles, 
                     "usage": UsageMode.static_draw})

    def __init__(self, *args, **kwargs):
        """ Geometry initialization
        """
        super(Geometry,self).__init__(*args, **kwargs)
        
    



