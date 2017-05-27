import uuid

class Base(object):
    """ This is the default Base Object.

        Base object will only accept the parameters that are set
        in  __slots__ list. If the element is not in the list
        then the code will end up with an error.

        If any value are given without qualified name, then the class
        will use the __slot__ fields by order.
        
        To create a new class that will inherit from this one you should
        create a new child class and set __slots__ list with the
        desired parameters:

        >>> __slots__ = ["name","id","c","childs",...] 

        >>> sample = Base("node1", "123", "Geometry",["12","23"])
        >>> sample.name 
        node1
        >>> sample.id
        123
        >>> sample.component 
        Geometry
        >>> sample.childs 
        ["12","23"]
        >>> print(repr(sample))
        Base({'id': '123', 'name': 'node1', 'type': 'Geometry', 'childs': ["12","23"]})

        >>> base = Base("Node1")
        >>> print(repr(base))
        Base({'id': 'bec10fa6-b9b5-442a-bf00-d9ea5d26dbfa', 'name': 'Node1', 'type': 'Base'})
    """
    # Slots to fix Memory allocation and ensure integrity in the data
    __slots__ = ["name","id","type"] 

    def __init__(self, *args, **kwargs):
        """ Create the base Object
        """ 
        # Create all slot attributes with empty values
        for slot in self.__slots__:
            setattr(self, slot, None)
        # Set individual elements in args
        for index, value in enumerate(args):
            if index >= len(self.__slots__):
                break
            setattr(self, self.__slots__[index], value)
        # Finally set dictionary values in kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
        # Initialize custom paremters if none
        self.name = self.name or self.__class__.__name__
        self.id = self.id or str(uuid.uuid4()) 
        self.type = self.type or self.__class__.__name__

    def __del__(self):
        """  Destroy current object
        """
        pass

    def __str__(self):
        """Returns the string representation of this instance
        """
        return "<{},{}>, {}, {}".format(self.__class__.__name__, self.type, self.name, self.id)

    def __repr__(self):
        """Returns the string representation of this instance
        """
        attribs = dict()
        for attrib in self.__slots__:
            attribs[attrib] = getattr(self,attrib)
        return "{}({})".format(self.__class__.__name__,str(attribs))

