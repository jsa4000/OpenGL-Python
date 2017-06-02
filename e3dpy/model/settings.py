from ..core.utils import *
from .samples import *

class Settings:
    """ Material Class Definition
    """

    @property
    def default_actions():
        return None

    @property
    def default_material():
        return samples.basic_material()

    @property
    def default_geometry():
        return samples.basic_material()

    def __init__(self, texture):
        pass
    


 

    

  