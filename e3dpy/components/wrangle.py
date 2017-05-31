from collections import OrderedDict as dict
from ..core import Component

class Wrangle(Component):
    """ Wrangle Component class
    """

    defaults = dict( {"wrangle": None} )

    def __init__(self, *args, **kwargs):
        """ Wrangle initialization
        """
        super(Wrangle,self).__init__(*args, **kwargs)
        


