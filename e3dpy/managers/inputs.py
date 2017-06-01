import numpy as np
from ..core import Worker 
from ..components import InputComponent
from ..controllers import Device
from ..core import CatalogueManager
from ..model import Input, Preset, Mouse, Keys, EventType

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

        # Get the relationship betwen entities and components
        for component in components.index:
            # entity : component (input)
            # print("{}:{}".format(component, components[component]))
            pass

        # For each component get the 
        # events = self._device.get_events()
        # for event in events:
        #     if event.type == EventType.QUIT:
        #         print("QUIT!")
        # print(events)

        return self
