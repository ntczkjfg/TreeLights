import pickle
import numpy as np
from Tree import Tree

rng = np.random.default_rng()

tree = 0
def newTree():
    global tree
    # Coordinates of LEDs in 3D space
    with open("/home/pi/Desktop/TreeLights/Trees/coordinates.list", "rb") as f:
        coordinates = pickle.load(f)
    tree = Tree(coordinates)
    with open("/home/pi/Desktop/TreeLights/Trees/myTree.tree", "wb") as f:
        pickle.dump(tree, f)

def savedTree(name):
    global tree
    with open("/home/pi/Desktop/TreeLights/Trees/" + name + ".tree", "rb") as f:
        tree = pickle.load(f)

#newTree()
savedTree("myTree")
tree.finishNeighbors()

#with open("/home/pi/Desktop/TreeLights/Trees/mCoordinates.list", "rb") as f:
#    mCoordinates = pickle.load(f)
#mTree = Tree(mCoordinates)
#with open("/home/pi/Desktop/TreeLights/Trees/mTree.tree", "wb") as f:
#    pickle.dump(mTree, f)
with open("/home/pi/Desktop/TreeLights/Trees/mTree.tree", "rb") as f:
    mTree = pickle.load(f)
mTree.finishNeighbors()