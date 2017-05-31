from collections import OrderedDict as dict
from ..core import Component

class Render(Component):
    """ Render Component class
    """

    defaults = dict( {"render": None} )

    def __init__(self, *args, **kwargs):
        """ Render initialization
        """
        super(Render,self).__init__(*args, **kwargs)
        



