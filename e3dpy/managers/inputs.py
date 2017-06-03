import numpy as np
from ..core import WorkerBase
from ..components import InputComponent
from ..controllers import Device
from ..core import CatalogueManager, Globals
from ..model import Actions, Action, MouseButton, Key, EventType

class InputsManager(WorkerBase):
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
              (event.type == EventType.KEYUP and event.key == Key.K_ESCAPE):
                Globals.display.close()
                break
        # End the worker run process
        return self

    def _process_component_events(self, component, events):
        """ Function to process all the events for the current component
        """
        #Get the inputs/actions from the current component
        component =  CatalogueManager.instance().get(component)
        actions = Actions(component.actions)
        packed = {}
        for event in events:
            packed[event.type] = []
        for event in events:
            if event.type in [EventType.KEYDOWN, EventType.KEYUP]:
                packed[event.type].append(event.key)
            elif event.type in [EventType.KEYSPRESSED]:
                packed[event.type].extend(event.keys)
            elif event.type in [EventType.MOUSEBUTTONUP, EventType.MOUSEBUTTONDOWN]:
                packed[event.type].append(event.button)
            elif event.type in [EventType.MOUSEMOTION]:
                packed[event.type].extend(event.buttons)
        #print("My actions: ")
        for action in actions:
            #print("type = {self.type}, parameters = {self.parameters}".format(self=action))  
            if action.type.value in packed:
                if packed[action.type.value] == action.parameters:
                    print("This is OK")
      
