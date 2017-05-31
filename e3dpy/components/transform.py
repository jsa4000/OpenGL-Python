from collections import OrderedDict as dict
from ..core import Component

class Transform(Component):
    """ Transform Component class
    """

    defaults = dict( {"transform": None} )

    def __init__(self, *args, **kwargs):
        """ Transform initialization
        """
        super(Transform,self).__init__(*args, **kwargs)
        



