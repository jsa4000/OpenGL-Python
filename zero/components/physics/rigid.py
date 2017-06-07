from collections import OrderedDict as dict
from ...core import Component

class RigidComponent(Component):
    """ Rigid Body Object Component class
    """

    # Defaut type/name the component will have
    DEFAULT_TYPE = "RigidComponent"

    defaults = dict( {"rbo": None} )

    def __init__(self, *args, **kwargs):
        """ Rigid Body Object initialization
        """
        super(RigidComponent,self).__init__(*args, **kwargs)
        



