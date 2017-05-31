from collections import OrderedDict as dict
from ..core import Component

class Light(Component):
    """ Light Component class
    """

    defaults = dict( {"light": None} )

    def __init__(self, *args, **kwargs):
        """ Light initialization
        """
        super(Light,self).__init__(*args, **kwargs)
        

