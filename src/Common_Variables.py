import pickle
import numpy as np
from Tree import Tree

rng = np.random.default_rng()

C = {
    "WHITE": [255, 255, 255],
    "ON": [255, 255, 255],
    "PURPLE": [0, 255, 255],
    "CYAN": [255, 0, 255],
    "YELLOW": [150, 255, 0],
    "GREEN": [255, 0, 0],
    "RED": [0, 255, 0],
    "ORANGE": [64, 255, 0],
    "BLUE": [0, 0, 255],
    "BLACK": [0, 0, 0],
    "OFF": [0, 0, 0],
    "AQUA": [238, 40, 95]
}

C["COLORS"] = [C["WHITE"], C["PURPLE"], C["CYAN"], C["YELLOW"], C["GREEN"], C["RED"], C["ORANGE"], C["BLUE"], C["AQUA"]]
C["TREECOLORS"] = [C["RED"], C["RED"], C["GREEN"], C["GREEN"], C["YELLOW"], C["BLUE"]]

# Coordinates of LEDs in 3D space
with open("/home/pi/Desktop/TreeLights/Trees/coordinates.list", "rb") as f:
    coordinates = pickle.load(f)
for i in range(200):
    coordinates.append([.7, .7, 1])

# Matt's coordinates
#with open("/home/pi/Desktop/TreeLights/Trees/mattCoordinates.list", "rb") as f:
#    mattCoordinates = pickle.load(f)

tree = 0
def newTree():
    global tree
    tree = Tree(coordinates)
    with open("/home/pi/Desktop/TreeLights/Trees/myTree.tree", "wb") as f:
        pickle.dump(tree, f)
    tree.finishNeighbors()

def savedTree(name):
    global tree
    with open("/home/pi/Desktop/TreeLights/Trees/" + name + ".tree", "rb") as f:
        tree = pickle.load(f)

newTree()
#savedTree("myTree")