from Common_Variables import rng, tree, mTree
from StaticEffects import *
from Transitions import *
from Colors import *
from TestingFunctions import *
from HelperFunctions import *
import numpy as np
import os
from time import sleep, time

# Has each light blink out its index number in binary
def binary(SLEEP = 1, backwards = False):
    maxLength = len(bin(tree.LED_COUNT - 1)[2:])
    binaryReps = [(maxLength * "0" + bin(i)[2:])[-maxLength:] for i in range(tree.LED_COUNT)]
    if backwards: binaryReps = [rep[::-1] for rep in binaryReps]
    for d in range(maxLength):
        for i in range(tree.LED_COUNT):
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
    print(totalConnections, "connections among", tree.LED_COUNT, "with", loneLEDs, "neighborless LEDs and", poorlyConnected,
          "poorly connected LEDs, and an average of", totalConnections/tree.LED_COUNT, "connections per LED")
    tree.show()
    input()
    for pixel in tree:
        tree.clear(False)
        pixel.setColor(RED)
        for neighbor in pixel.neighbors:
            neighbor.setColor(GREEN)
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
            if neighbor.z < pixel.z:
                lowest = False
                break
        if lowest:
            pixel.setColor(RED)
    tree.show()

# Lights up thin planar slices of the tree in sorted directions
def sortedPlanarTest(variant = "a"):
    sections = 25
    zRange = tree.zRange / sections
    xRange = tree.xRange / sections
    yRange = tree.yRange / sections
    aRange = 2*np.pi / sections
    if variant == "a":
        for a in np.linspace(0, 2*np.pi, sections + 1):
            tree.clear(False)
            for pixel in tree:
                if pixel.a >= a and pixel.a <= a + aRange:
                    pixel.setColor(WHITE)
            tree.show()
            print("Showing angle from", round(a, 5), "to", round(a + aRange, 5))
            input()
    elif variant == "x":
        for x in np.linspace(tree.xMin, tree.xMax, sections + 1):
            tree.clear(False)
            for pixel in tree:
                if pixel.x >= x and pixel.x <= x + xRange:
                    pixel.setColor(WHITE)
            tree.show()
            print("Showing x from", round(x, 5), "to", round(x + xRange, 5))
            input()
    elif variant == "y":
        for y in np.linspace(tree.yMin, tree.yMax, sections + 1):
            tree.clear(False)
            for pixel in tree:
                if pixel.y >= y and pixel.y <= y + yRange:
                    pixel.setColor(WHITE)
            tree.show()
            print("Showing y from", round(y, 5), "to", round(y + yRange, 5))
            input()
    elif variant == "z":
        for z in np.linspace(tree.zMin, tree.zMax, sections + 1):
            tree.clear(False)
            for pixel in tree:
                if pixel.z >= z and pixel.z <= z + zRange:
                    pixel.setColor(WHITE)
            tree.show()
            print("Showing z from", round(z, 5), "to", round(z + zRange, 5))
            input()
    tree.clear()

# Turns on lights one-by-one in the sorted directions
def sortedTest(colors = None):
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    while True:
        tree.clear()
        color = Color()
        for i in tree.sortedX:
            tree[i].setColor(color)
            tree.show()
        sleep(1)
        tree.clear()
        color = Color()
        for i in tree.sortedY:
            tree[i].setColor(color)
            tree.show()
        sleep(1)
        tree.clear()
        color = Color()
        for i in tree.sortedZ:
            tree[i].setColor(color)
            tree.show()
        sleep(1)
        tree.clear()
        color = Color()
        for i in tree.sortedA:
            tree[i].setColor(color)
            tree.show()
        sleep(1)
        tree.clear()

# Illuminates the interior and surface LEDs on the tree in different colors
def surfaceTest(interior = BLUE, surface = RED):
    setAll(interior)
    for pixel in tree:
        if pixel.surface: pixel.setColor(surface)
    tree.show()