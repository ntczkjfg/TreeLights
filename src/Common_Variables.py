from Tree import Tree
import numpy as np
import pickle
from time import time
import os

current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
PATH = os.path.join(parent_directory, "Trees")
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
    with open(os.path.join(PATH, "coordinates.list"), "wb") as f:
        pickle.dump(coordinates, f)
    print("Saved coordinates")

# Makes fake coordinates and builds a tree from them
# Useful for testing before coordinates have been generated
# Also useful for testing things on Windows where accurate maps matter much less
def dummyCoordinates(n = 1200):
    coordinates = []
    while len(coordinates) < n:
        point = [rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(0, 4)]
        if point[0]**2 + point[1]**2 <= (1 - point[2]/4)**2:
            coordinates.append(point)
    return coordinates

# Builds the tree, using existing coordinates
def buildTree():
    startTime = time()
    try:
        with open(os.path.join(PATH, "coordinates.list"), "rb") as f:
            coordinates = pickle.load(f)
    except FileNotFoundError:
        try:
            with open("/home/pi/Desktop/TreeLights/Trees/coordinates.list", "rb") as f:
                coordinates = pickle.load(f)
        except FileNotFoundError:
            print("Coordinates not found - making dummy coordinates")
            coordinates = dummyCoordinates()
    tree = Tree(coordinates)
    print(f"Built the tree in {round(time() - startTime, 2)} seconds")
    return tree

if __name__ != "__main__":
    tree = buildTree()