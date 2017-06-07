import numpy as np
import threading
from ...core import CatalogueManager, Actions
from ...core.utils import *
from ...components import InputComponent

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

    def run(self, multithread=False):
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

        # Check whether is going to be multithread
        if multithread:
            threads = []
            # Get the relationship betwen entities and components
            for entity in components.index:
                thread = threading.Thread(target=self._process_component_events, 
                                          args=(entity,components[entity],events))
                thread.start()
                threads.append(thread)
                # Wain unitl all the component ahave finished
            for thread in threads:
                thread.join()
        else:
            # Get the relationship betwen entities and components
            for entity in components.index:
                # entity : component (input)
                # print("{}:{}".format(entity, components[entity]))
                self._process_component_events(entity, components[entity], events)

      
    def _process_component_events(self, entity, component, events):
        """ Function to process all the events for the current component
        """
        #Get the inputs/actions from the current component
        component =  CatalogueManager.instance().get(component)
        entity = CatalogueManager.instance().get(entity)
        actions = component.actions

        # Check if any action satisfy any event
        for action in actions:
            if actions[action].isin(events) and actions[action].evaluate(events):
                # If events and condition then execute the action
                actions[action].execute(entity=entity,component=component,engine=self._engine)
 
      
