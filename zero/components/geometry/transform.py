from collections import OrderedDict as dict
from ...core import Component

class TransformComponent(Component):
    """ Transform Component class
    """

    # Defaut type/name the component will have
    DEFAULT_TYPE = "transform"

    defaults = dict( {"transform": None} )

    def __init__(self, *args, **kwargs):
        """ Transform initialization
        """
        super(TransformComponent,self).__init__(*args, **kwargs)
        



