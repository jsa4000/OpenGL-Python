from collections import OrderedDict as dict
from ..base.utils import *
from .constants import *

class RenderController(list):
    """ Render Controller Class

    This class will store all the renders created. Also it will
    manage the creation of the window, shutdown, etc..

    """
    def __init__(self, render):
        """ Initialize the constructor
        """
        if not is_collection(render):
            render = [render]
        self.extend(render)


    def init(self):
        """ Initialize the creation of the render
        """
        for render in self:
            render.init()
        return self

    def render(self):
        """ Render
        """
        for render in self:
            render.render()
        return self

    def dispose(self):
        """ Dispose manually the render
        """
        for render in self:
            render.dispose()
        return self