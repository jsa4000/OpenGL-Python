import numpy as np
from ..core import CatalogueManager
from ..core.controllers import DeviceEvent, Key
from ..components import InputComponent
from ..model import Actions

class InputManager(object):
    """ Input Worker Class

    This class will manage all the events sent by the user.
    The class will iterate through all the components and 
    entities that support input components so the will be 
    updated correctly.

    """
    def __init__(self, engine):
        """ Initialization of the Manager

        Initialize variables to use as cache or storing last
        states for the inptus events, etc.. The manager also
        make use of the device
        """
        # Create a device controller to get the current inputs
        self._engine = engine
        self._device = engine.device 

    def __del__(self):
        """ Dispose and close the worker.
        """
        pass

    def init(self):
        """ Initialize objects and controllers
        """
        self._device.init()
        return self

    def run(self):
        """ Start the worker process
        """
        # To improve performances this can be done during the initializetion
        # This is only when it's in game mode and not in develop mode

        # Get the current Catalog
        df = CatalogueManager.instance().dataframe
        col_input = InputComponent.DEFAULT_TYPE
        # Get the current input actors
        components = df[col_input].dropna(axis=0)

        # Get all the events in the current frame
        events = self._device.get_events()

        # Get the relationship betwen entities and components
        for component in components.index:
            # entity : component (input)
            # print("{}:{}".format(component, components[component]))
            self._process_component_events(components[component],events)

        # End the worker run process
        return self

    def _process_component_events(self, component, events):
        """ Function to process all the events for the current component
        """
        #Get the inputs/actions from the current component
        component =  CatalogueManager.instance().get(component)
        actions = Actions(component.actions)

        # Check if any action satisfy any event
        for action in actions:
            if actions[action].isin(events):
                actions[action].execute(component=component,engine=self._engine)
                
                

      
