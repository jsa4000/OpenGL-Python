import numpy as np
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

    #  Geometry types supported.
    geometry_types = ParseDict({"points":"points",
                                "vertices":"verts",
                                "primitives":"prims"])

    # Some standard attributes to use manipulating geometry
    points_attributes = ParseDict({"position":"P",
                                    "normal":"N",
                                    "textcoords":"UV",
                                    "color":"Cd",
                                    "scale":"pscale",
                                    "velocity":"V",
                                    "life":"life",
                                    "acceleration":"accel"})

    # Usually for vertices apply the same attrbiutes since conceptually are very similar
    vertices_attributes = points_attributes

    # prims attributes
    prims_attributes = ParseDict{"indexes":"Id",
                                 "normal":"N",
                                 "color":"Cd",
                                 "material":"M" }

    # When a group is created it use a prefix to differenciate between normal attribs
    group_preffix = "group_"

    def __init__(self,*args, **kwargs):
        """This is the main contructor of the class.

        """
        super(Geometry,self).__init__(*args,**kwargs)
        # SEt the 
        self._iprims = prims_attributes.primitives
        self._ipoints = prims_attributes.points
   
    def has_indices(self):
        if self.prims_attributes.indexes in self.attributes[self._iprims]:
            return True
        return False
  
    def getPrimsAttrib(self, name):
            return self.data[self._iprims][self.attributes[self._iprims][name]]

    def delPrimsAttrib(self, name):
        self.data[self._iprims].drop(self.attributes[self._iprims][name], axis=1, inplace=True)

    def addPrimsAttrib(self, name, values=None, size=3, default=None, dtype=None):
        # Get the new attribute and dataframe
        result = self._createAttribute(self.data[self._iprims],name,size,values,default,dtype)
        if not empty(result):
            # Set the returned dataframe with the new attribute
            self.data[self._iprims] = result[0]
            # Set the columns into the the current Point attribute
            self.attributes[prims_attributes.points][name] = result[1]

    def addIndices(self, values, size=3, dtype=np.uint32):
         #Add prims Attributes Elements
        self.addPrimsAttrib(self.prims_attributes.indexes, values, size, dtype=dtype)
   
    def getPointAttrib(self, name):
        return self.data[self._ipoints][self.attributes[self._ipoints][name]]

    def delPointAttrib(self, name):
        self.data[self._ipoints].drop(self.attributes[self._ipoints][name], axis=1, inplace=True)

    def addPointAttrib(self, name, values=None, size=3,  default=None, dtype=None):
        # Get the new attribute and dataframe
        result = self._createAttribute(self.data[self._ipoints],name,size,values,default,dtype)
        if not empty(result):
            # Set the returned dataframe with the new attribute
            self.data[self._ipoints] = result[0]
            # Set the columns into the the current Point attribute
            self.attributes[self._ipoints][name] = result[1]

    def addPoints(self, values, size=3, dtype=np.float32):
        #Add point Attributes Position
        self.addPointAttrib(self.point_attributes.position, values, size, dtype)

    def addNormals(self, values, size=3, dtype=np.float32):
          #Add point Attributes Normals
        self.addPointAttrib(self.point_attributes.normal, values, size, dtype)
