import numpy as np
from ..base import Datasheet
from ..base.utils import *

class Geometry(Datasheet):
    """ Geometry Class 
    
    This class will create and store all the geometry needed
    to create points, vertices, primitives, etc..

    The way this class works in by inherit from DataBase. This super
    class has two main members:
        - data: dictionary where the geometry types will be stored.
        For each item in data it will be stored one geomtry type:
        points, vertices, prims, etc.. 

        This uses pandas libraries to store all the data, because
        it provides good performances manipulating the data.

        - attributes: This is another dictionary, where all the 
        attrbiutes will be stored. For multivalues attributes
        like vectors, matrizes, etc.. the data will be splitted into
        size parts. Each column's name will be the name of the attributes
        and a siffix (index_cols).

            postion (vector3) -> { "P" : [Px, Py, Pz] }

    """

    # Declare the subindex that will be used for multiple (vector) attribites
    index_cols = ["x","y","z","w"]

    #Defaule type that will be used for indexing using OpenGL elements array buffer
    index_type = np.uint32
    
    # Geometry types supported => Mapping name
    geometry_types = ParseDict({"points":"points",
                                "vertices":"verts",
                                "primitives":"prims"})

    # Some standard attributes to use for manipulating geometry
    point = ParseDict({"position":"P",
                        "normal":"N",
                        "textcoords":"UV",
                        "color":"Cd",
                        "scale":"pscale",
                        "velocity":"V",
                        "life":"life",
                        "acceleration":"accel"})

    # prims attributes
    primitive = ParseDict({"indices":"Id",
                           "normal":"N",
                           "color":"Cd",
                           "material":"M" })

    # defaults allowed in this class for the constructor
    defaults = dict({"vertices":None, 
                     "indices":None, 
                     "normals":None, 
                     "colors":None, 
                     "textcoords":None,
                     "size":None}) # Size will be a 4 vector

    #vertices, indices, normals, colors (alpha), textcoords
    default_sizes = [3,3,3,4,2] 

    # When a group is created it use a prefix to differenciate between normal attribs
    group_preffix = "group_"

    @property
    def indexed(self):
        """ Property to return if the geometry has vertex indexing (faces)
        """
        if self.primitive.indices in self.attributes[self._prims_index]:
            return True
        return False
    
    def __init__(self,*args, **kwargs):
        """This is the main contructor of the class.

        """
        super(Geometry,self).__init__(*args,**kwargs)
        # Get the indexed in the create (simplify the code) 
        self._prims_index = self.geometry_types.primitives
        self._points_index = self.geometry_types.points
        # Extract attributes in defaults
        self._extract_attributes()

    def _extract_attributes(self):
        # Extract all the values from the constructor
  
        # Set the default size if None
        self.size = self.size or self.default_sizes
        #loop over the defaults
        for default in self.defaults:
            if default == "size":
                continue
            # Get the current default value set
            value = getattr(self, default)
            if value is not None:
                #Set the current value
                if default == "vertices":
                    self.add_vertices(value,self.size[0])
                elif default == "indices":
                    self.add_indices(value,self.size[1])
                elif default == "normals":
                    self.add_normals(value,self.size[2])
                elif default == "colors":
                    self.add_colors(value,self.size[3])
                elif default == "textcoords":
                    self.add_textcoords(value,self.size[4])
            # Remove default attribute
            delattr(self, default)

    def get_prim_attrib(self, name):
         return self.get(self._prims_index,name)

    def remove_prim_attrib(self, name):
        self.remove(self._prims_index,name)
        return self

    def add_prim_attrib(self, name, values=None, size=3, default=None, dtype=None):
        # Get the new attribute and dataframe
        self.add(self._prims_index, name, values, size, default, dtype)
        return self

    def add_indices(self, values, size=3, dtype=np.uint32):
        #Add prims Attributes Elements
        self.add_prim_attrib(self.primitive.indices, values, size, dtype=dtype)
        return self
   
    def get_point_attrib(self, name):
        return self.get(self._points_index,name)

    def remove_point_attrib(self, name):
        self.remove(self._points_index,name)
        return self

    def add_point_attrib(self, name, values=None, size=3,  default=None, dtype=None):
         # Get the new attribute and dataframe
        self.add(self._points_index, name, values, size, default, dtype)
        return self

    def add_vertices(self, values, size=3, dtype=np.float32):
        #Add point Attributes Position
        self.add_point_attrib(self.point.position, values, size, dtype)
        return self

    def add_normals(self, values, size=3, dtype=np.float32):
        #Add point Attributes Normals
        self.add_point_attrib(self.point.normal, values, size, dtype)
        return self

    def add_textcoords(self, values, size=3, dtype=np.float32):
            #Add point Attributes Normals
        self.add_point_attrib(self.point.textcoords, values, size, dtype)
        return self
    
    def add_colors(self, values, size=3, dtype=np.float32):
            #Add point Attributes Normals
        self.add_point_attrib(self.point.color, values, size, dtype)
        return self
