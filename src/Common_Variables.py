from Tree import Tree
import numpy as np
import pickle
import platform
if platform.system() == "Windows":
    import matplotlib.pyplot as plt
    PATH = "C:/Users/User/My Stuff/GitHub/TreeLights/Trees/"
elif platform.system() == "Linux":
    PATH = "/home/pi/Desktop/TreeLights/Trees/"
else:
    print("Unknown operating system.", platform.system())

if platform.system() == "Windows":
    treeFileName = "winTree.tree"
elif platform.system() == "Linux":
    treeFileName = "myTree.tree"
rng = np.random.default_rng()
PI = float(np.pi)
TAU = 2*PI
tree = None

# Generates a new tree with user-supplied coordinates
def newTree(coordinates = None, sameCoords = False):
    global tree
    if sameCoords:
        with open(PATH + "coordinates.list", "rb") as f:
            coordinates = pickle.load(f)
    if not coordinates:
        print("Error: Must supply coordinates.")
        return
    with open(PATH + "coordinates.list", "wb") as f:
        pickle.dump(coordinates, f)
        print(f"Saved coordinates coordinates.list")
    tree = Tree(coordinates)
    with open(PATH + treeFileName, "wb") as f:
        pickle.dump(tree, f)
        print(f"Saved tree {treeFileName}")

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
        with open(PATH + treeFileName, "wb") as f:
            pickle.dump(tree, f)
            print(f"Saved tree {treeFileName}")

# Loads pickled tree - significantly faster than building from scratch
def savedTree(treeFileName):
    global tree
    with open(PATH + treeFileName, "rb") as f:
        tree = pickle.load(f)
from time import time
startTime = time()
if __name__ != "__main__":
    if platform.system() == "Windows":
        savedTree(treeFileName)
        plt.show(block = False)
    elif platform.system() == "Linux":
        rebuildTree(save = False)
        #savedTree(treeFileName)
finishTime = round(time() - startTime, 2)
print(f"Took {finishTime} seconds")