import os
import sys
import numpy as np

# Add the currnent parent path so it recognize rendegl package entirely
PACKAGE_PARENT = '../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from zero.core import ( Entity, Component, Base,
                        Catalogue, CatalogueGroup,
                        CatalogueDict, CatalogueTree)

class Transform(Component):
    defaults = dict({"position":[0,1,2,3],
                     "rotation":np.array(range(10))})

class Camera(Component):
    defaults = dict({"mode":0,
                     "orbit":False,
                     "view": np.reshape(range(9),(3,3))})

def test_ecs():
    transform1 = Transform("tranform1",key="name")
    transform2 = Transform("tranform2",key="name")

    camera = Camera("Camera1")
    
    print(camera.mode)
    print(camera.orbit)
    print(camera.view)

    entity = Entity("root", items=[transform1,camera])
    #entity[None] = transform2.id
    entity.set_items(transform2.id)
    print(repr(entity))

    print(entity.Catalogue)
    print(entity.Catalogue.dataframe.head())


def test_catalogue():
    # Test
    catalogue_index = "Entity"
    catalogue_col1 = "Transform"
    catalogue_col2 = "Position"
    catalogue_col3 = "Health"
    catalogue_col4 = "Renderable"

    entities = ["entity01", "entity02", "entity03", "entity04","entity05"]
    components = [catalogue_col1, catalogue_col2, catalogue_col3,catalogue_col4]
    entity01_comp = ["Transform01", None        , None       ,  "Renderable01" ]
    entity02_comp = ["Transform02", None        , "Health02" ,  "Renderable02" ]
    entity03_comp = ["Transform03", "Position03", None       ,  None           ]
    entity04_comp = ["Transform04", "Position04", "Health04" ,  None           ]
    entity05_comp = ["Transform05", None        , "Health05" ,  "Renderable05" ]

    entities_comp =  [entity01_comp, entity02_comp, entity03_comp, entity04_comp, entity05_comp ]

    # Create the main Catalogue
    catalogue = Catalogue(index = catalogue_index)
    # Add all the entities into the catalogue
    for index, entity in enumerate(entities):
        # Add current entity
        catalogue[catalogue_index][entity] = entity
        # Add component for the current entity
        for cindex, ctype in enumerate(components):
            comp_instance = entities_comp[index][cindex]
            if comp_instance is not None:
                # Add current component to the catalogue
                catalogue[ctype][comp_instance] = comp_instance
                # Bind the current comp with it's entity
                catalogue.bind(entity, ctype, comp_instance)

    print(catalogue)
    print(catalogue.dataframe.head(10))

def test_collection_list():
    class Category1(CatalogueDict): pass
    class Category2(CatalogueDict): pass
    class Category3(CatalogueDict): pass
    class Category4(CatalogueDict): pass
    class Category5(CatalogueDict): pass

    # Change current index for the Catalog Manager
    Base.DEFAULT_UUID = Base.UUID1
    #CatalogueManager.DEFAULT_INDEX = "CatalogueDict"
    # Create several catalogues to be manager to CatalogManager singletone
    catalogue1 = CatalogueDict("catalogue1","catalogue1")
    catalogue2 = CatalogueDict("catalogue2","catalogue2")
    catalogue3 = CatalogueDict("catalogue3","catalogue3")
    catalogue4 = CatalogueDict("catalogue4","catalogue4")
    catalogue5 = CatalogueDict("catalogue5","catalogue5")
    # Create several items for the caralogue to bind
    items1 = [None                    , Category2("item12","12"), None                    , Category4("item14","14"), Category5("item15","15") ]
    items2 = [Category1("item21","21"), None                    , Category3("item23","23"), None                    , None                   ]
    items3 = [Category1("item31","31"), None                    , None                    , None                    , Category5("item35","35") ]
    items4 = [Category1("item41","41"), Category2("item42","42"), None                    , Category5("item44","44"), None                   ]

    # Start adding the items into the catalogs
    print("START ADDING CATALOGUE BY CONSTRUCTOR")
    print("---------------------------------------")
    # catalogue1 = CatalogueDict("catalogue1","catalogue1",items=items1)
    # print(catalogue1.items.keys())
    # Change name instead the type to create the catalogues
    catalogue1 = CatalogueDict("catalogue1","catalogue1",items=items1, key="name")
    print(catalogue1.items.keys())
    print(CatalogueDict.Catalogue.dataframe.head(10))

    # Add catalogue using indexing. Key is irrelevant
    print("ADDING MULTIPLE CATEGORIES BY INDEXING")
    print("---------------------------------------")
    catalogue2[None] = items2
    print(catalogue2.items.keys())
    print(CatalogueDict.Catalogue.dataframe.head(10))
    # Add another category (single element)
    print("ADDING SINGLE A CATEGORY BY INDEXING")
    print("---------------------------------------")
    catalogue2[None] = Category2("item22",22)
    print(catalogue2.items.keys())
    print(CatalogueDict.Catalogue.dataframe.head(10))
    # Remove categories (and bings)
    print("REMOVE SINGLE A CATEGORY BY INDEXING")
    print("---------------------------------------")
    del catalogue2["21"]
    print(catalogue2.items.keys())
    print(CatalogueDict.Catalogue.dataframe.head(10))
    print("REMOVE SINGLE A CATEGORY BY MULTIPLE  INDEXING")
    print("-----------------------------------------------")
    del catalogue1[("12","14")]
    print(catalogue1.items.keys())
    print(CatalogueDict.Catalogue.dataframe.head(10))

    print("REPORT CATALOGUE")

    print(CatalogueDict.Catalogue)
    print(CatalogueDict.Catalogue.dataframe.head(10))


def test_collection_tree():
        
    # Set childs by add function
    Santiago = CatalogueTree("Santiago")
    Javier = CatalogueTree("Javier")
    Alvaro = CatalogueTree("Alvaro")
    Alberto = CatalogueTree("Alberto")
    # Add childs by using objects and ids
    Santiago.set_children([Javier,Alvaro])
    Santiago.set_children(Alberto.id)
    print(repr(Santiago))
    print(Santiago.children)

    # Santiago is the root parent = None
    # Javier, Alvaro and Alberto parent is Santiago
    print(Javier.parent.name)
    print(Alvaro.parent.name)
    print(Alberto.parent.name)
    # TRy to remove the parent and set manually set_parent
    print("REMOVE JAVER FROM CHILDS")
    Santiago.remove_children(Javier.id)
    print(repr(Santiago))
    print(Santiago.children)
    # print(Javier.parent.name) # ERROR!  No parent anymore
    print("ADD JAVER AGAIN")
    Javier.set_parent(Santiago)
    print(repr(Santiago))
    print(Santiago.children)
    print(Javier.parent.name)

    # Set directly childs into the constructor
    # PPlay adding entitys by object or id
    # By id it will look into the catalog of entities
    Mateo = CatalogueTree("Mateo")
    Ines = CatalogueTree("Ines")
    Alberto = CatalogueTree("Alberto", children = [Mateo, Ines.id])
    print(repr(Alberto))
    print(Alberto.children)

if __name__ == '__main__':
    # test the current entity
    test_ecs()
    #test_catalogue()
    #test_collection_list()
    #test_collection_tree()

