from collections import OrderedDict as dict
from ..core import Component

class MaterialComponent(Component):
    """ Material Component class
    """

    # Defaut type/name the component will have
    DEFAULT_TYPE = "material"

    defaults = dict( {"material": None} )

    def __init__(self, *args, **kwargs):
        """ Material initialization
        """
        super(MaterialComponent,self).__init__(*args, **kwargs)
        


