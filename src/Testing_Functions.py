from Common_Variables import rng, tree, PI, TAU, newTree
from Colors import *
from Simple_Effects import *
from Helper_Functions import *
import numpy as np
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
        tree.clear(UPDATE = False)
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

def lightSlice(n, dim, width = 0.015):
    for pixel in tree:
        if abs(pixel.coord[dim] - tree[n].coord[dim]) < width:
            pixel.setColor(WHITE)
        else:
            pixel.setColor(OFF)
    tree[n].setColor(GREEN)
    tree.show()

def adjustLight(n, dim):
    dims = ["x", "y", "z"]
    if dim not in dims:
        print("""Must specify "x", "y", or "z" dimension""")
        return
    dim = dims.index(dim)
    if n < 0 or n >= tree.LED_COUNT:
        print("Given n is outside of acceptable range.")
        return
    while True:
        lightSlice(n, dim)
        print("Current " + str(dims[dim]) + "-coord: " + str(tree[n].coord[dim]))
        delta = input("Increase (+) or decrease (-)? ")
        if delta == "":
            break
        elif delta == "+":
            delta = .02
        elif delta == "-":
            delta = -.02
        else:
            continue
        tree[n].coord[dim] += delta
    save = input("Save (y/n)? ")
    if save not in ["y", "Y"]:
        return
    coordinates = []
    for pixel in tree:
        coordinates.append(pixel.coord)
    newTree(coordinates)
    print("Saved")

# Lights up thin planar slices of the tree in sorted directions
def planeTest(variant = "z"):
    sections = 20
    propertyIndex = ["x", "y", "z", "a"].index(variant)
    minVal = [-1, -1, 0, 0][propertyIndex]
    increment = [2/sections, 2/sections, tree.zMax/sections, TAU / sections][propertyIndex]
    try:
        if variant == "a":
            for a in np.linspace(0, TAU, sections + 1):
                tree.clear(UPDATE = False)
                for pixel in tree:
                    if pixel.a >= a and pixel.a <= a + increment:
                        pixel.setColor(WHITE)
                tree.show()
                print("Showing angle from", round(a, 5), "to", round(a + increment, 5))
                input()
        else:
            for i in range(sections):
                cMin = i*increment + minVal
                cMax = cMin + increment
                tree.clear(UPDATE = False)
                for pixel in tree:
                    if pixel.coord[propertyIndex] >= cMin and pixel.coord[propertyIndex] <= cMax:
                        pixel.setColor(WHITE)
                tree.show()
                print("Showing", variant, "from", round(cMin, 5), "to", round(cMax, 5))
                input()
    except KeyboardInterrupt:
        binary(SLEEP = 0.2)
        x = input()
        x = "0b" + x
        x = int(x, 2)
        adjustLight(x, variant)
    tree.clear()

# Lights up thin planar slices of the tree in sorted directions
def planeTest2(sections = 12, variant = "x"):
    propertyIndex = ["x", "y", "z"].index(variant)
    minVal = [-1, -1, 0][propertyIndex]
    increment = [2/sections, 2/sections, tree.zMax/sections][propertyIndex]
    tree.clear(UPDATE = False)
    color = GREEN
    text = "Boundaries: -1"
    for i in range(sections):
        if color == RED:
            color = GREEN
        elif color == GREEN:
            color = BLUE
        else:
            color = RED
        cMin = i*increment + minVal
        cMax = cMin + increment
        text += ", " + str(cMax)
        for pixel in tree:
            if cMin <= pixel.coord[propertyIndex] and pixel.coord[propertyIndex] <= cMax:
                pixel.setColor(color)
    tree.show()
    print(text)
    x = input()
    if x == "":
        return
    binary(SLEEP = 0.2)
    x = input()
    x = "0b" + x
    x = int(x, 2)
    adjustLight(x, variant)
    planeTest2(sections, variant)

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

def coordinateChange(index, coord, value):
    if coord == 0:
        tree[index].x = value
    elif coord == 1:
        tree[index].y = value
    elif coord == 2:
        tree[index].z = value
    else:
        print("Invalid coord")
        return
    tree[index].coordinate[coord] = value
    tree.coordinates[index][coord] = value
    with open("/home/pi/Desktop/TreeLights/Trees/coordinates.list", "wb") as f:
        pickle.dump(tree.coordinates, f)
    rebuildTree(save = True)
