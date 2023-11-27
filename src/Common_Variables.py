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

# Generates a new tree with user-supplied coordinates
def newTree(coordinates = None):
    global tree
    if not coordinates:
        print("Error: Must supply coordinates.")
        return
    with open(PATH + "coordinates.list", "wb") as f:
        pickle.dump(coordinates, f)
    tree = Tree(coordinates)
    with open(PATH + "myTree.tree", "wb") as f:
        pickle.dump(tree, f)
    tree.finishNeighbors()

# Makes fake coordinates and builds a tree from them
# Useful for testing before coordinates have been generated
def dummyTree(LEDCount = 800):
    global tree
    coordinates = [[rng.random(), rng.random(), rng.random()] for i in range(LEDCount)]
    newTree(coordinates)

# Rebuilds the pickled tree from scratch, using existing coordinates, then repickles
# This needs to be done if the Tree class is modified
def rebuildTree(save = True):
    global tree
    with open(PATH + "coordinates.list", "rb") as f:
        coordinates = pickle.load(f)
    tree = Tree(coordinates)
    if save:
        with open(PATH + "myTree.tree", "wb") as f:
            pickle.dump(tree, f)
    tree.finishNeighbors()

# Loads pickled tree - significantly faster than building from scratch
def savedTree(name):
    global tree
    with open(PATH + name + ".tree", "rb") as f:
        tree = pickle.load(f)
    tree.finishNeighbors()

if __name__ != "__main__":
    savedTree("myTree")