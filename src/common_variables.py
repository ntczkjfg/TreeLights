from pathlib import Path
from time import time
import json

import numpy as np

from tree import Tree

cwd = Path.cwd()
parent_directory = cwd.parent
trees_path = parent_directory / 'Trees'
rng = np.random.default_rng()
PI = float(np.pi)
TAU = 2*PI
tree = None

# Saves the supplied coordinates to file
def save_coords(coordinates = None):
    if coordinates is None:
        print('Must supply coordinates to save')
        return
    coordinates = [list(coordinate) for coordinate in coordinates]
    with open(trees_path / 'coordinates.list', 'w') as f:
        json.dump(coordinates, f)
    print('Saved coordinates')

# Makes fake coordinates and builds a tree from them
# Useful for testing before coordinates have been generated
# Also useful for testing things on Windows where accurate maps matter much less
def dummy_coordinates(n = 1200):
    coordinates = []
    while len(coordinates) < n:
        point = [rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(0, 4)]
        if point[0]**2 + point[1]**2 <= (1 - point[2]/4)**2:
            coordinates.append(point)
    return coordinates

# Builds the tree, using existing coordinates
def build_tree():
    global tree
    start_time = time()
    try:
        with open(trees_path / 'coordinates.list', 'r') as f:
            coordinates = json.load(f)
    except FileNotFoundError:
        print('Coordinates not found - making dummy coordinates')
        coordinates = dummy_coordinates()
    tree = Tree(coordinates)
    print(f'Built the tree in {round(time() - start_time, 2)} seconds')
    return tree

if __name__ != '__main__':
    tree = build_tree()
    tree.brightness = 0.4
