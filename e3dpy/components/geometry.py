from collections import OrderedDict as dict
from ..core import Component

class Geometry(Component):
    """ Geometry Component class
    """

    defaults = dict( {"geometry": None} )

    def __init__(self, *args, **kwargs):
        """ Geometry initialization
        """
        super(Geometry,self).__init__(*args, **kwargs)
        



