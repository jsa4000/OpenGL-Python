import numpy as np
from ..core import Worker 
from ..components import InputComponent
from ..controllers import Device
from ..core import CatalogueManager, Globals
from ..model import Actions, Action, Mouse, Keys, EventType

class InputsManager(Worker):
    """ Input Worker Class

    This class will manage all the events sent by the user.
    The class will iterate through all the components and 
    entities that support input components so the will be 
    updated correctly.

    """
    def __init__(self):
        """ Initialization of the Worker

        Initialize variables to use as cache or storing last
        states for the inptus events, etc.. The manager also
        make use of the device
        """
        # Create a device controller to get the current inputs
        self._device = Device()

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

        # Get all the events in the current frame for globals¡ events
        for event in events:
            if event.type == EventType.QUIT or \
              (event.type == EventType.KEYUP and event.key == Keys.K_ESCAPE):
                Globals.display.close()
                break
        # End the worker run process
        return self

    def _process_component_events(self, component, events):
        """ Function to process all the events for the current component
        """
        #Get the inputs/actions from the current component
        component =  CatalogueManager.instance().get(component)
        actions = component.actions
        actions = [ {"name": "Camera Orbit",
                    "type":"EventType.MOUSEMOTION",
                     "parameters":["Mouse.LEFTBUTTON"],
                     "action":"entity.camera.orbit(event.rel[0],event.rel[1])"},
                    {"name": "Camera Pan",
                     "type":"EventType.MOUSEMOTION",
                     "parameters":"[Mouse.MIDDLEBUTTON]",
                     "action":"entity.camera.pan(event.rel[0],event.rel[1])"}]
        actions = Actions(actions)
        print(inputs)
                       