from collections import OrderedDict as dict
from ..core import Component

class RBOComponent(Component):
    """ Rigid Body Object Component class
    """

    # Defaut type/name the component will have
    DEFAULT_TYPE = "RBO"

    defaults = dict( {"rbo": None} )

    def __init__(self, *args, **kwargs):
        """ Rigid Body Object initialization
        """
        super(RBOComponent,self).__init__(*args, **kwargs)
        



