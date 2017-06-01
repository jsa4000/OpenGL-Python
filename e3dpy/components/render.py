from collections import OrderedDict as dict
from ..core import Component
from ..drivers.geometry import DrawMode, UsageMode

class RenderComponent(Component):
    """ Render Component class
    """

    # Defaut type/name the component will have
    DEFAULT_TYPE = "render"

    defaults = dict({"renderer": None,
                     "mode" : DrawMode.triangles, 
                     "usage": UsageMode.static_draw})

    def __init__(self, *args, **kwargs):
        """ Render initialization
        """
        super(RenderComponent,self).__init__(*args, **kwargs)
        



