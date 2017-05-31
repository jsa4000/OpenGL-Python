from collections import OrderedDict as dict
import numpy as np
import pandas as pd
import uuid
from .utils import *

__all__ = ['Base', 
           'Defaults',
           'DataBase',
           'DefaultBase',
           'ThreadBase']

class Base(object):
    """ This is the default Base Object.

        Base object will only accept the parameters that are set
        in  __slots__ list. If the element is not in the list
        then the code will end up with an error.

        If any value are given without qualified name, then the class
        will use the __slot__ fields by order.

            ex. Base("Javier", 12, type = "Base")
        
            Then:  =>  __slots__ = ["name","id","type"]  

                __slots__[0] = "Javier" => name
                __slots__[1] = 12       => id
                __slots__["type"] = "Base"
        
        To create a new class that inherits from this one you should
        create a new child class and set __slots__ list with the
        desired parameters to be overriding or added:
        
            class CustomBase(Base):
                
                __slots__ = ["name","id","type","children",...]

                def __init__(self, *args, **kwargs):
                    # Create default Database object
                    super(CustomBase, self).__init__(*args, **kwargs)

        IMPORTANT:
            If you set __slots__ you won't be able to set any attribute.
            You have tow options:
                1. Don't include __slots__ so only be considered previous
                slots in inherited classes. Then you could start adding new
                paramters as always. 

                  def __init__(self, *args, **kwargs):
                        # Create default Database object
                        super(CustomBase, self).__init__(*args, **kwargs)
                        # add new parameters
                        self._new_parameter = None
                
                In this case you cannot pass this parameter in the constructor
                since the base class will use them and it will be ignored.

                2. Use Defaults Base class defined at the bottom. Both class 
                could be inherited by using multiple-inheritance. However
                you should call to the constructors independently-

                    class Custom(Base, Defaults):
        
                        defaults = dict( {"job":"driver"})

                        def __init__(self, *args, **kwargs):
                            # Create default Database object
                            Base.__init__(*args, **kwargs)
                            Defaults.__init__(*args, **kwargs)

                    custom = Custom(name = "Javier", job = "Senior Programmer")
                    custom.name
                    custom.job

                3. Add a new value in __slots__ called "attributes" (ex)
                and when the attribute ins called the it will use the override 
                method  __getattr__(self, key) that will take "attributes" 
                if it doesn't found in the inner attribs because the __slots__
                limitation.
                
                    __getattr__(self, key):
                        if key in self.__slots__:
                            return getattr(self, key)
                        else:
                            return self.attributes[key]

        >>> sample = Base("node1", "123", "Geometry",["12","23"])
        >>> sample.name 
        node1
        >>> sample.id
        123
        >>> sample.component 
        Geometry
        >>> sample.children 
        ["12","23"]
        >>> print(repr(sample))
        Base({'id': '123', 'name': 'node1', 'type': 'Geometry', 'children': ["12","23"]})

        >>> base = Base("Node1")
        >>> print(repr(base))
        Base({'id': 'bec10fa6-b9b5-442a-bf00-d9ea5d26dbfa', 'name': 'Node1', 'type': 'Base'})

        When type is not specified the it will use self.__class__.__name__ by default
        Also it will check the DEFAULT_TYPE after the last condition. This is a particular
        case when a derived class want to set by default a "type". 
        
        This could be done also by calling the constructor to the base
        class as follows: 
            
            super(Someclass, self).__init__(*args, **kwargs.update({"type" = "something"}))

        Globally the genreation of the id could be also set globally to
        the python environment. So all the classes create from Base will use the same
        generation unique id.

            Base.DEFAULT_UUID = Base.UUID1

    """

    # Available UUID functions
    UUID1 = uuid.uuid1 # make a UUID based on the host ID and current time
    UUID4 = uuid.uuid4 # make a random UUID
    COUNTER = BasicCounter(1)


    # Default UUID
    DEFAULT_UUID = UUID4

    # Reredefine the type to set into the attribute type. 
    # The default is self.__class__.__name__ by default
    DEFAULT_TYPE = None

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
        self.id = self.id or str(Base.DEFAULT_UUID()) 
        self.type = self.type or self.DEFAULT_TYPE or self.__class__.__name__

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


class Defaults(object):
    """ Defaults Class

    This is the base Defaults class that any object should
    inherit from if it's required to have more parameters
    to use without adding them to __slots__. Also this provides
    a way to set a default value to the parameters if
    they are not given in the creaction.

    In classes created from this base class, properties and
    default paramters can be given in the "defaults" variable
    shared for all instances created from current class.

    If parameter not in default, this won't be updated
    or added. In case of accessing to this attribute then
    python give you an error.

        # Supposse "name" is not in "defaults"
        custom = Custom(name="Alex") # This will be ignored
        custom.name # error !!

    Example:

        class Custom(Defaults):
            defaults = dict({"name":"Michael Jordan",
                             "age": 20})
            def __init__(self, *args, **kwargs):
                # Create default Database object
                super(Custom, self).__init__(*args, **kwargs)

        flexible = Custom(age = 34)
        print(flexible.name)
        print(flexible.age)
        print(str(flexible))
        print(repr(flexible))

    Output:

        Michael Jordan
        34
        <Custom> ['name:Michael Jordan', 'age:34']
        Custom(['name:Michael Jordan', 'age:34'])


    Example with multiple inheritance from Base and Defauts
        -> Order is important when multiple inheritance

        class Flexible(Base, Defaults):
            
            defaults = dict( {"my_name":None})

            def __init__(self, *args, **kwargs):
                # Create default objects in order
                Base.__init__(self,*args, **kwargs)
                Defaults.__init__(self,*args, **kwargs)

        flexible = Flexible(name = "Javier", my_name = "Javier")
        print(flexible.name)  # From __slots__
        print(flexible.my_name) # From defaults

        >Javier
        >Javier

        flexible = Flexible()
        print(flexible.name)  # From __slots__
        print(flexible.my_name) # From defaults

        >Flexible
        >None

    """

    # Default dinctionary with properties
    defaults = dict()

    def __init__(self,  *args, **kwargs):
        """This is the main contructor of the class
           Initially set the dafult valiues
        """
        # Update the default properties if None
        self._update_defaults(kwargs, True)
                
    def _update_defaults(self, properties, force=True):
        """ Update current properties given in the parameters
        """ 
        for param in self.defaults:
            if param not in self.__dict__:
                setattr(self, param, self.defaults[param]) 
            if param in properties:
                # Update the value if required
                if force or self.__dict__[param] is None:
                    setattr(self, param, properties[param]) 
      
    def __str__(self):
        """Returns the string representation of this instance
        """
        attribs = self.__dict__
        parameters = ["{}:{}".format(key, attribs[key]) for key in attribs if key in self.defaults]
        return "<{}> {}".format(self.__class__.__name__, parameters)

    def __repr__(self):
        """Returns the string representation of this instance
        """
        attribs = self.__dict__
        parameters = ["{}:{}".format(key, attribs[key]) for key in attribs if key in self.defaults]
        return "{}({})".format(self.__class__.__name__,parameters)


class DefaultBase(Base, Defaults):
    """ DefaultBase Class

        This class is a subclass of Base and Defaults. This provide
        multi-inheritance functionality to allow to set more attributes
        to Base and also set default values to the attributes.

        Example

            class Flexible(DefaultBase):
                defaults = dict( {"nick":None})

                def __init__(self, *args, **kwargs):
                    # Create default objects in order
                    super.__init__(*args, **kwargs)

            (Or simply)
            class Flexible(DefaultBase):
                 defaults = dict( {"nick": "Awesome"})

            flexible = Flexible()
            flexible = Flexible("Javier", 12)
            flexible = Flexible("Javier", type="JavierType", nick="jsa000")

            # Following is allowed by Base class, but you always need to 
            # include nick in the creation since it can not be created inside 
            # the class. See the init function at the top for CustomBase
            #flexible = CustomBase("Javier", type="JavierType", nick="jsa000")

            #flexible = Flexible(id=23)
            print(flexible.name)
            print(flexible.nick)
            print(str(flexible))
            print(repr(flexible))

            <FlexibleDB> 
            FlexibleDB(OrderedDict([('name', 'Javier'), ('id', '5f212236-8214-4ae7-bc86-eca5aae8b3a5'),
                                 ('type', 'JavierType')])) 
            FlexibleDB(['nick:jsa000'])
            FlexibleDB(FlexibleDB(OrderedDict([('name', 'Javier'), ('id', '5f212236-8214-4ae7-bc86-eca5aae8b3a5'), 
                            ('type', 'JavierType')])) FlexibleDB(['nick:jsa000']))

    """
    defaults = dict()

    def __init__(self, *args, **kwargs):
        """
        """
        # Create default DefaultBase object
        #    Note: "self"" it's required
        Base.__init__(self,*args, **kwargs)
        Defaults.__init__(self,*args, **kwargs)

    def __str__(self):
        """Returns the string representation of this instance
        """
        return "<{}> \n {} \n {}".format(self.__class__.__name__, 
                                        Base.__repr__(self),Defaults.__repr__(self))

    def __repr__(self):
        """Returns the string representation of this instance
        """
        return "{}({} {})".format(self.__class__.__name__, 
                                        Base.__repr__(self),Defaults.__repr__(self))


class DataBase(DefaultBase):
    """ Data Base Class

        This element will create and store all the elements in
        small dataframes. Data frames can be accessed by a 
        Key methods sinde the are going to e stored in a dict.

        Parameters:
            name, id and type wil be inherited from Base

            data: Dictionary with the data that will be stored
                  In case we want to store "People", "Product"
                  we will have two items. Inside each item wwill 
                  store a data frame with the attributes.
                  data.keys() = ["People","Product"]

            attributes: Attrbiutes will be stored per data index.
                 In previous example we will have different attributes
                 for "Person" and different attribs for "Product". 
                 In case "Person" has an attribute with posistion ("P") 
                 we will have the following structure:

                 atttributes["Person"]["P"] = ["Px","Py","Pz"]

                 This means attributes that more size tham 1, will
                 be divided into multiple indexes, x, y and z.
                 See multiple_index = ["x","y","z","w"]

                 How ever to access to this attribute, it's only needed
                 the first part atttributes["Person"]["P"], since the
                 class know what columns to take for each multiple
                 attribute.

    """

    # Slots to fix Memory allocation and ensure integrity in the data
    __slots__ = ["name","id","type","data","attributes"] 

    # Declare the subindex that will be used for multiple (vector) attribites
    multiple_index = ["x","y","z","w"]

    def __init__(self, *args, **kwargs):
        """This is the main contructor of the class.

        """
        super(DataBase,self).__init__(*args,**kwargs)
        # Initialize data variable where dataframe will be stored
        self.data = dict()
        # Initialize groups for attribute in Data frames
        self.attributes = dict()
   
    def __del__(self):
        # Dispose all the objects and memory allocated
        pass
    
    def _createAttribute(self, df, name, size=3, values=None, default=None, dtype=None):
        """ This will create a n Attribute inside the current df.
        
        Parameters:
            df: dataframe where the attribute will be created
            name: name for the new attribute to create.
            size: if value has 3 elements (vector) or scalar 1
                -> if size > 1 the attrribute will be splitted in
                  different columns inside the data. The new columns
                  will depend on the multiple_index
            values: The values that will be set by default if any.
            default: value that will be set if no values are defined.
                -> If no values and not default the function will return
                  without performing any operation.
            dtype: type of the data that will be inserted. For example,
            np.float32, np.int32, etc...

        """
        #Check the data type if any
        if dtype is None:
            if empty(values):
                # Assign a default value
                dtype = np.float32
            else:
                # Get the type from the values
                if not isinstance(values,(np.ndarray)):
                    # If not numpy then get the numppy array 
                    values = np.array(values)
                #Finally get the type from the numpy array
                dtype = values.dtype 
        # Check any values or default values has been provided
        if empty(values) and empty(default):
            if df is None or df.empty:
                # If nothing to add exit the function
                return None
            else:
                # Create a default value (float)
                default = np.zeros((size), dtype=dtype)
        # Check the index value depending on the size
        if size > 1:
            columns = [name + self.multiple_index[i] for i in range(size)]
        else:
            columns = [name]
        # Check if values has been already defined
        if empty(values) and (df is not None and not df.empty):
            # create an array with the same number of rows as the current
            values = np.tile(default,(len(df.index)))
        # Reshape the values [ Maybe should be normalized and flatten]
        values = np.array(np.reshape(values, (-1, size)) ,dtype=dtype)
        # Check if the DataFrame is empty
        if df is None or df.empty:
            # Add the current data into the attributes frame
            df = pd.DataFrame(values, columns=columns)
        else:
            # Add the current data into the attributes frame
            dfvalues = pd.DataFrame(values, columns=columns)
            # Append both dataframes
            df = pd.merge(df, dfvalues, how='inner', left_index=True, right_index=True)
        # Set the columns into the the current Point attribute
        return (df, columns)

    def getAttrib(self, index, name):
            return self.data[index][self.attributes[index][name]]

    def delAttrib(self, index, name):
        self.data[index].drop( self.attributes[index][name], axis=1, inplace=True)

    def addAttrib(self, index, name, values=None, size=3, default=None, dtype=None):
        # Check if current data frame is not create
        if (index not in self.data):
            self.data[index] = pd.DataFrame()
            self.attributes[index] = dict()
        # Get the new attribute and dataframe
        result = self._createAttribute(self.data[index],name,size,values,default,dtype)
        if not empty(result):
            # Set the returned dataframe with the new attribute
            self.data[index] = result[0]
            # Set the columns into the the current attribute
            self.attributes[index][name] = result[1]

    def __str__(self):
        """Returns the string representation of this instance
        """
        # Get parents string represenation
        #base = super(DataBase, self).__str__()
        current = ""
        for item in self.data:
            # Get the list of attributes
            current += "-----------------------------------------------------------\n"
            current += " {}\n".format(item)
            current += "-----------------------------------------------------------\n"
            current += str(self.attributes[item]) + "\n"
            current += "-----------------------------------------------------------\n"
            current += self.data[item].head().to_string()  + "\n"
            current += "-----------------------------------------------------------\n"

        # Returns the base and 
        return current

    def __repr__(self):
        """Returns the string representation of this instance
        """
        return super(DataBase, self).__repr__()


class ThreadBase(object):
    """ ThreadBase Engine Class

        This class is the main loop of the process that will manage 
        the threads in the engine. If threads are not supported
        set global variable MULTI_THREAD to false at start

        ThreadBase.MULTI_THREAD = False

    """

    #Set variable multithread globally
    MULTI_THREAD = True

    @property
    def running(self):
        return self._running

    def __init__(self):
        """ Contructor for the class
        """
        # Initilaize parameters
        self._thread = None
        self._running = False

    def __del__(self):
        """ Clean up the memory
        """
        # Stop the process if any running
        self._thread_stop()
   
    def _thread_stop(self):
        """ This function will stop and dipose the thread
        """
        # Be sure to wait until the current process stops
        self._running = False
        # Wait and set to none
        if self._thread:
            self._thread.join()
            self._thread = None

    def _thread_start(self, process):
        """ This function will start the thread
        """
        # Stop the process if any running
        self._thread_stop()
        # Set started to true
        self._running = True
        # Create a new thread and run the process
        self._thread = threading.Thread(target=process)
        self._thread.start()  
   
    def _process(self):
       """ Process to implement
       """
       pass

    def start(self):
        """This method Starts the thread.
        """
        if ThreadBase.MULTI_THREAD:
            # Start the engine process (new thread)
            self._thread_start(self._process)
        else:
            # Set started to true (possible while in process)
            self._running = True
            # Start using the same thread
            self._process()
            # Since it'not multithread set again to false
            self._running = False
 
    def stop(self):
        """This method force to Stops the thread
        """
        self._thread_stop()
        
