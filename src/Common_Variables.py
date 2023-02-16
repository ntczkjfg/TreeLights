from Tree import Tree
import numpy as np
import pickle
import platform
if platform.system() == "Windows":
    PATH = "C:/Users/User/My Stuff/GitHub/TreeLights/Trees/"
elif platform.system() == "Linux":
    PATH = "/home/pi/Desktop/TreeLights/Trees/"
else:
    print("Unknown operating system.", platform.system())

rng = np.random.default_rng()
PI = float(np.pi)
TAU = 2*PI

tree = None
def newTree():
    global tree
    coordinates = None
    with open(PATH + "coordinates.list", "wb") as f:
        pickle.dump(coordinates, f)
    tree = Tree(coordinates)
    with open(PATH + "myTree.tree", "wb") as f:
        pickle.dump(tree, f)

def rebuildTree(save = False):
    global tree
    with open(PATH + "coordinates.list", "rb") as f:
        coordinates = pickle.load(f)
    tree = Tree(coordinates)
    if save:
        with open(PATH + "myTree.tree", "wb") as f:
            pickle.dump(tree, f)

def savedTree(name):
    global tree
    with open(PATH + name + ".tree", "rb") as f:
        tree = pickle.load(f)

# Generates a new tree, using manually-input new coordinates
#newTree()

# Rebuilds the same tree, using existing coordinates
# Must be used if Tree class is modified
rebuildTree(save = False)

# Loads pickled Tree - significantly faster than building from scratch
#savedTree("myTree")

# Pickling fails if this is done before pickling, due to recursion errors
# Converts pixel neighbors to proper format
tree.finishNeighbors()
