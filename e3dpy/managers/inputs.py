from ..core import Worker 
from ..controllers import Device
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
        
        # Some test
        events = self._device.get_events()
        for event in events:
            if event.type == EventType.QUIT:
                print("QUIT!")
        print(events)

        return self
