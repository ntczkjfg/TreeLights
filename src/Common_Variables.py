import pickle
import numpy as np
from Tree import Tree

rng = np.random.default_rng()
np.tau = 2*np.pi

tree = None
def newTree():
    global tree
    coordinates = None
    with open("/home/pi/Desktop/TreeLights/Trees/coordinates.list", "wb") as f:
        pickle.dump(coordinates, f)
    tree = Tree(coordinates)
    with open("/home/pi/Desktop/TreeLights/Trees/myTree.tree", "wb") as f:
        pickle.dump(tree, f)

def rebuildTree(save = False):
    global tree
    with open("/home/pi/Desktop/TreeLights/Trees/coordinates.list", "rb") as f:
        coordinates = pickle.load(f)
    tree = Tree(coordinates)
    if save:
        with open("/home/pi/Desktop/TreeLights/Trees/myTree.tree", "wb") as f:
            pickle.dump(tree, f)

def savedTree(name):
    global tree
    with open("/home/pi/Desktop/TreeLights/Trees/" + name + ".tree", "rb") as f:
        tree = pickle.load(f)

# Generates a new tree, using manually-input new coordinates
#newTree()

# Rebuilds the same tree, using existing coordinates
# Must be used if Tree class is modified
#rebuildTree(save = True)

# Loads pickled Tree - significantly faster than building from scratch
savedTree("myTree")

# Pickling fails if this is done before pickling, due to recursion errors
# Converts pixel neighbors to proper format
tree.finishNeighbors()
