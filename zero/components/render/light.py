from collections import OrderedDict as dict
from ..core import Component

class LightComponent(Component):
    """ Light Component class
    """

    # Defaut type/name the component will have
    DEFAULT_TYPE = "light"

    defaults = dict( {"light": None} )

    def __init__(self, *args, **kwargs):
        """ Light initialization
        """
        super(LightComponent,self).__init__(*args, **kwargs)
        

