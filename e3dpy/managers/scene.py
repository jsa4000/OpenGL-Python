from ..core import Worker

class SceneManager(Worker):
    """ Input Worker Class
    """

    def __init__(self):
        """ Initialization of the Worker
        """
        pass

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
        print("Scene Working")
        return self
