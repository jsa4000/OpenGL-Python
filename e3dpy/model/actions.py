from ..core.utils import *
from ..model.events import Event, EventType, Key, KeyModifier, MouseButton

class Actions(list):
    """ Actions Class Definition

    This class will map the inputs from devices such as
    key board, clicks, etc.. to apply a certaion action.

    The idea is to have mapped all the possible inputs from
    the keyboard into actions. Actions could be from simple
    actions like invoking simple functions to be able to
    write some scripts to specify more advanced and complex actions.abs

    This input will model this configuration for files or any key, value
    structutre like dictionary
    """

    def __init__(self, actions):
        # List that will store all the input-action for this instance
        for action in actions:
            action = ParseDict(action)
            self.append(Action(action.name, action.type,
                               action.parameters, action.action))

class Action(object):
    """ Class to represent the input/action behaviour
    """
    def __init__(self, name, type, parameters, action):
        """Set the basic structure of an input/action
        """
        self.name = name
        self.type = eval(type)
        self.parameters = [eval(parameter) for parameter in parameters]
        self.action = action
