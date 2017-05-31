from collections import OrderedDict as dict
from ..core import Component

class Camera(Component):
    """ Camera Component class
    """

    defaults = dict( {"camera": None} )

    def __init__(self, *args, **kwargs):
        """ Camera initialization
        """
        super(Camera,self).__init__(*args, **kwargs)
        



