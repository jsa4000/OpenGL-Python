from collections import OrderedDict as dict
from ..core import Component

class CameraComponent(Component):
    """ Camera Component class
    """

    # Defaut type/name the component will have
    DEFAULT_TYPE = "camera"

    defaults = dict( {"camera": None} )

    def __init__(self, *args, **kwargs):
        """ Camera initialization
        """
        super(CameraComponent,self).__init__(*args, **kwargs)
        



