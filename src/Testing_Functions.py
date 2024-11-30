from time import sleep, time

import numpy as np

from Common_Variables import rng, tree, PI, TAU, saveCoords, buildTree
from Colors import *
from Simple_Effects import *
from Helper_Functions import *

# Has each light blink out its index number in binary
def binary(SLEEP = .5, backwards = False):
    maxLength = len(bin(tree.n - 1)[2:])
    binaryReps = [(maxLength * "0" + bin(i)[2:])[-maxLength:] for i in range(tree.n)]
    if backwards: binaryReps = [rep[::-1] for rep in binaryReps]
    for d in range(maxLength):
        for i in range(tree.n):
            if binaryReps[i][d] == "0":
                tree[i] = RED
            else:
                tree[i] = GREEN
        tree.show()
        sleep(SLEEP)
        tree.clear()
        sleep(SLEEP)

# Sequentially shows all LEDs and their "connected" neighbors
def connectivityTest():
    totalConnections = 0
    loneLEDs = 0
    poorlyConnected = 0
    for pixel in tree:
        connections = len(pixel.neighbors)
        totalConnections += connections
        pixel.setColor(GREEN)
        if connections < 4:
            poorlyConnected += 1
            pixel.setColor(YELLOW)
        if connections == 2:
            loneLEDs += 1
            pixel.setColor(RED)
    print(totalConnections, "connections among", tree.n, "with", loneLEDs, "neighborless LEDs and", poorlyConnected,
          "poorly connected LEDs, and an average of", totalConnections/tree.n, "connections per LED")
    tree.show()
    input()
    for pixel in tree:
        tree.clear(UPDATE = False)
        pixel.setColor(RED)
        for neighbor in pixel.neighbors:
            tree[neighbor].setColor(GREEN)
        tree.show()
        input()
    tree.clear()

# Continuously updates all LEDs with a color - useful when stringing the tree
def continuousUpdate(color = WHITE):
    if color is not None: tree.fill(color)
    while True:
        tree.show()
        sleep(0.5)

# Lights up all pixels that are locally the lowest
def findFloor():
    tree.clear()
    for pixel in tree:
        lowest = True
        for neighbor in pixel.neighbors:
            if tree[neighbor].z < pixel.z:
                lowest = False
                break
        if lowest:
            pixel.setColor(RED)
    tree.show()

# Used by adjustLight below
# Lights up all LEDs with a similar coordinate to the indicated LED
def lightSlice(n, dim, width = 0.015):
    for pixel in tree:
        if abs(pixel.coordinate[dim] - tree[n].coordinate[dim]) < width:
            pixel.setColor(WHITE)
        else:
            pixel.setColor(OFF)
    tree[n].setColor(GREEN)
    tree.show()

# Used to adjust a specific coordinate for a specific light
def adjustLight(n, dim):
    global tree
    dims = ["x", "y", "z"]
    if dim not in dims:
        print("""Must specify "x", "y", or "z" dimension""")
        return
    dim = dims.index(dim)
    if n < 0 or n >= tree.n:
        print("Given n is outside of acceptable range.")
        return
    while True:
        lightSlice(n, dim)
        print("Current " + str(dims[dim]) + "-coord: " + str(tree[n].coordinate[dim]))
        delta = input("Increase (+) or decrease (-)? ")
        if delta == "":
            break
        elif delta == "+":
            delta = .02
        elif delta == "-":
            delta = -.02
        else:
            continue
        tree[n].coordinate[dim] += delta
    save = input("Save (y/n)? ")
    if save not in ["y", "Y"]:
        return
    coordinates = []
    for pixel in tree:
        coordinates.append(pixel.coordinate)
    saveCoords(coordinates)
    tree = buildTree()

# Help determine the maximum theoretical framerate of the tree under various circumstances
def maxFramerate(duration = 10, variant = 0):
    startTime = time()
    tree.frames = 0
    while time() - startTime < duration:
        if variant == 0: # tree.setColors
            colors = rng.integers(0, 256, 3*tree.n)
            tree.setColors(colors)
        elif variant == 1: # pixel.setColor
            colors = rng.integers(0, 256, 3*tree.n)
            colors = colors.reshape(tree.n, 3)
            for i, pixel in enumerate(tree):
                pixel.setColor(colors[i])
        elif variant == 2: # No color changing
            pass
        tree.show()
    duration = time() - startTime
    print(f"maxFramerate: {tree.frames} frames in {round(duration, 2)} seconds for {round(tree.frames/duration, 2)} fps")

# Divide the tree into halves to detect (and fix) misplaced lights
def planeTest(sections = 20, variant = "y", startAt = 1):
    propertyIndex = ["x", "y", "z"].index(variant)
    minVal = [-1, -1, 0][propertyIndex]
    increment = [2/sections, 2/sections, tree.zMax/sections][propertyIndex]
    for boundary in range(startAt, sections + 1):
        tree.clear(UPDATE = False)
        boundaryVal = boundary*increment
        for pixel in tree:
            if pixel.coordinate[propertyIndex] <= minVal + boundaryVal:
                pixel.setColor(RED)
            else:
                pixel.setColor(GREEN)
        tree.show()
        if boundary == sections: continue
        x = input("Enter to continue, anything else to flash binary and fix")
        if x == "":
            continue
        binary(SLEEP = 0.25)
        x = input()
        x = int(x, 2)
        adjustLight(x, variant)
        planeTest(sections, variant, startAt = boundary)
        return
    tree.clear()

# Turns on lights one-by-one in the sorted directions
def sortedTest(colors = None, speed = 1, variant = "z"):
    Color = color_builder(colors)
    index = ["i", "x", "y", "z", "r", "a"].index(variant)
    order = tree.indices[index]
    color = Color()
    for count, i in enumerate(order, start = 1):
        tree[i].setColor(color)
        if count % speed == 0 or count == tree.n:
            tree.show()

# Illuminates the interior and surface LEDs on the tree in different colors
def surfaceTest(interior = BLUE, surface = RED):
    for pixel in tree:
        if pixel.surface:
            pixel.setColor(surface)
        else:
            pixel.setColor(interior)
    tree.show()
