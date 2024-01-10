from Tree import Tree
import numpy as np
import pickle
import platform
from time import time
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

# Saves the supplied coordinates to file
def saveCoords(coordinates = None):
    if coordinates is None:
        print("Must supply coordinates to save")
        return
    coordinates = list(coordinates)
    with open(PATH + "coordinates.list", "wb") as f:
        pickle.dump(coordinates, f)
    print("Saved coordinates")

# Makes fake coordinates and builds a tree from them
# Useful for testing before coordinates have been generated
def dummyTree(LEDCount = 800):
    global tree
    coordinates = [[rng.random(), rng.random(), rng.random()] for i in range(LEDCount)]
    newTree(coordinates)

# Builds the tree from scratch, using existing coordinates
# This needs to be done if the Tree class is modified
def buildTree():
    startTime = time()
    global tree
    with open(PATH + "coordinates.list", "rb") as f:
        coordinates = pickle.load(f)
    tree = Tree(coordinates)
    print(f"Built the tree in {round(time() - startTime, 2)} seconds")
    return tree

if __name__ != "__main__":
    buildTree()