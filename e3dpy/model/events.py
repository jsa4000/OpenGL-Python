

class Event(object):
    """ Generic Event class definition. 
    """
    def __init__(self, *args, **kwargs):
        """Constructor
        """
        try:
            for key in args:
                setattr(self, key, args[key])
        except:
            # None of not a dictionary
            pass
        for key in kwargs:
            setattr(self, key, kwargs[key])
    def __repr__(self):
        """"""
        return "<Event: {}>".format(self.__dict__)

