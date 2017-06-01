from collections import OrderedDict as dict
from ..core import Component

class RenderComponent(Component):
    """ Render Component class
    """

    # Defaut type/name the component will have
    DEFAULT_TYPE = "render"

    defaults = dict({"mode" : "triangles", 
                     "usage": "static_draw"})

    def __init__(self, *args, **kwargs):
        """ Render initialization
        """
        super(RenderComponent,self).__init__(*args, **kwargs)
        



