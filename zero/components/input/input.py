from collections import OrderedDict as dict
from ...core import Component

class InputComponent(Component):
    """ Input Component class

    Attaching this component to an Entitiy will enable the functionality
    so perform actions by inputs from the user.
    """

    # Defaut type/name the component will have
    DEFAULT_TYPE = "input"

    defaults = dict( {"actions": None} )

    def __init__(self, *args, **kwargs):
        """ Input initialization
        """
        super(InputComponent,self).__init__(*args, **kwargs)
   

