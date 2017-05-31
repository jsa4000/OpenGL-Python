from collections import OrderedDict as dict
from ..core import Component

class Material(Component):
    """ Material Component class
    """

    defaults = dict( {"material": None} )

    def __init__(self, *args, **kwargs):
        """ Material initialization
        """
        super(Material,self).__init__(*args, **kwargs)
        


