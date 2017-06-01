from ..core import Worker 

class InputsWorker(Worker):
    """ Input Worker Class

    This class will manage all the events sent by the user.
    The class will iterate through all the components and 
    entities that support input components so the will be 
    updated correctly.


    """

    def __init__(self):
        """ Initialization of the Worker
        """
        # initialize the default values
        self._last_mouse_position = [None, None]


    def __del__(self):
        """ Dispose and close the worker.
        """
        pass

    def init(self):
        """
        """
        return self

    def run(self):
        """ Start the worker process
        """
        print("Input Working")


        return self
