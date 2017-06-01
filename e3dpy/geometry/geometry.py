import numpy as np
from ..core import DataBase
from ..core.utils import *

class Geometry(DataBase):
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
    
    #  Geometry types supported => Mapping name
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
    primitive = ParseDict({"indexes":"Id",
                           "normal":"N",
                           "color":"Cd",
                           "material":"M" })

    # When a group is created it use a prefix to differenciate between normal attribs
    group_preffix = "group_"

    @property
    def indexed(self):
        """ Property to return if the geometry has vertex indexing (faces)
        """
        if self.primitive.indexes in self.attributes[self._prims_index]:
            return True
        return False
  
    def __init__(self,*args, **kwargs):
        """This is the main contructor of the class.

        """
        super(Geometry,self).__init__(*args,**kwargs)
        # Get the indexed in the create (simplify the code) 
        self._prims_index = self.geometry_types.primitives
        self._points_index = self.geometry_types.points
   
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
        self.add_prim_attrib(self.primitive.indexes, values, size, dtype=dtype)
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
