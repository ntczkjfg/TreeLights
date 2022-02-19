from Common_Variables import rng, tree, C
import numpy as np
import os
from time import sleep, time
from StaticEffects import *
from Transitions import *

tree.clear()

#Random stripes
#Spinners
#Expanding shapes from center
#Expanding / contracting stripes at random angles
#Letters
#Spinning angled plane
#Small number of points moving around with fading trails
#Sierpinski?
#Snake
#Fire?
#Infectious colors

def hexFill():
    numberOfStripes = 3
    angleDiff = 2 * np.pi / numberOfStripes
    stripeThickness = np.pi/3 # In radians
    stripeThickness /= 2
    zStep = 0.0003
    z = tree.zMin
    while True:
        for angle in np.linspace(0, angleDiff, 40):
            for pixel in tree:
                if abs(abs(abs((pixel.a % angleDiff) - angle) - angleDiff/2) - angleDiff/2) < stripeThickness:
                    pixel.setColor(RED)
                else:
                    if z > tree.zMax or z < tree.zMin:
                        zStep *= -1
                    z += zStep
                    if pixel.z < z:
                        pixel.setColor(C["BLUE"])
                    else:
                        pixel.setColor(C["BLUE"])
            tree.show()

def binary(SLEEP = 1, backwards = False):
    maxLength = len(bin(tree.LED_COUNT - 1)[2:])
    binaryReps = [(maxLength * "0" + bin(i)[2:])[-maxLength:] for i in range(LED_COUNT)]
    if backwards: binaryReps = [rep[::-1] for rep in binaryReps]
    for d in range(maxLength):
        for i in range(LED_COUNT):
            if binaryReps[i][d] == "0":
                tree[i] = C["RED"]
            else:
                tree[i] = C["GREEN"]
        tree.show()
        sleep(SLEEP)
        tree.clear()
        sleep(SLEEP)

def cardinalLightUp(colors = None):
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    while True:
        color = Color()
        tree.clear()
        for i in tree.sortedX:
            tree[i] = color
            tree.show()
        sleep(1)
        color = Color()
        tree.clear()
        for i in tree.sortedY:
            tree[i] = color
            tree.show()
        sleep(1)
        color = Color()
        tree.clear()
        for i in tree.sortedZ:
            tree[i] = color
            tree.show()
        sleep(1)

def cylinder(colors = C["COLORS"]):
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list or len(colors) < 3:
            print("Must supply at least 3 colors for this effect")
            return
        Color = lambda: rng.choice(colors)
    color1 = Color()
    color2 = Color()
    while np.array_equal(color1, color2): color2 = Color()
    tree.fill(color2)
    while np.array_equal(color1, color2): color2 = Color()
    midZ = tree.zRange/2 + tree.zMin
    rRange = 2**.5
    minR = rRange / 4
    sections = 40 # Larger = slower
    while True:
        for z in np.linspace(0, tree.zRange, sections):
            for pixel in tree:
                if pixel.x**2 + pixel.y**2 < minR**2 and abs(pixel.z - midZ) < z:
                    pixel.setColor(color1)
            tree.show()
        for r in np.linspace(minR, rRange, sections):
            for pixel in tree:
                if pixel.x**2 + pixel.y**2 < r**2:
                    pixel.setColor(color1)
            tree.show()
        newColor = Color()
        while np.array_equal(color1, newColor) or np.array_equal(color2, newColor): newColor = Color()
        color2 = newColor
        for r in np.linspace(rRange, minR, sections):
            for pixel in tree:
                if pixel.x**2 + pixel.y**2 > r**2:
                    pixel.setColor(color2)
            tree.show()
        for z in np.linspace(tree.zRange, 0, sections):
            for pixel in tree:
                if abs(pixel.z - midZ) > z:
                    pixel.setColor(color2)
            tree.show()
        sleep(0.2)
        newColor = Color()
        while np.array_equal(color1, newColor) or np.array_equal(color2, newColor): newColor = Color()
        color1 = newColor

def imageSlideshow():
    PAT = "/home/pi/Desktop/Images/"
    imgList = os.listdir(PAT)
    for image in imgList:
        displayImage(image)
        print(image[:-4])
        a = input()
    tree.clear()

# For testing purposes only
def planar():
    sections = 20
    zRange = tree.zRange / sections / 2
    xRange = tree.xRange / sections / 2
    yRange = tree.yRange / sections / 2
    for z in np.linspace(tree.zMin, tree.zMax, sections):
        tree.clear(False)
        for pixel in tree:
            if abs(pixel.z - z) < zRange:
                pixel.setColor(C["WHITE"])
        tree.show()
        print("Showing z from", round(z - zRange, 5), "to", round(z + zRange, 5))
        input()
    for x in np.linspace(tree.xMin, tree.xMax, sections):
        tree.clear(False)
        for pixel in tree:
            if abs(pixel.x - x) < xRange:
                pixel.setColor(C["WHITE"])
        tree.show()
        print("Showing x from", round(x - xRange, 5), "to", round(x + xRange, 5))
        input()
    for y in np.linspace(tree.yMin, tree.yMax, sections):
        tree.clear(False)
        for pixel in tree:
            if abs(pixel.y - y) < yRange:
                pixel.setColor(C["WHITE"])
        tree.show()
        print("Showing y from", round(y - yRange, 5), "to", round(y + yRange, 5))
        input()
    tree.clear()

def pulsatingSphere(colors = C["COLORS"]):
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    color1 = Color()
    color2 = color1
    while np.array_equal(color1, color2): color2 = Color()
    height = 1.3
    minH = 0.6
    maxH = 2
    deltaH = 0.04
    maxR = 1
    r = 0.31
    deltaR = 0.04
    while True:
        if r <= .3:
            deltaR *= -1
            r += deltaR
            color1 = color2
            while np.array_equal(color1, color2): color1 = rng.choice(C["COLORS"])
        elif r > maxR:
            deltaR *= -1
            r += deltaR
        if height <= minH:
            deltaH *= -1
            height += deltaH
        elif height > maxH:
            deltaH *= -1
            height += deltaH
        for pixel in tree:
            if (pixel.x**2 + pixel.y**2 + (pixel.z-height)**2)**0.5 <= r:
                pixel.setColor(color1)
            else:
                pixel.setColor(color2)
        tree.show()
        r += deltaR
        height += deltaH

def rain(colors = [[55, 55, 255]]):
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    tree.clear(False)
    dropCount = 10 # Number of raindrops at any moment
    radius = 0.1 # Size of rain drops (Raindrops are square cylinders)
    newDrop = lambda: [(rng.random() - 0.5) * tree.xRange / 2, (rng.random() - 0.5) * tree.yRange / 2, tree.zMax + rng.random() * 2, Color()]
    raindrops = [newDrop() for i in range(dropCount)]
    while True:
        for i, drop in enumerate(raindrops):
            # Next two lines make drop move away from the trunk, third line makes them move down
            drop[0] *= 1.03
            drop[1] *= 1.03
            drop[2] -= .15
            if drop[2] < tree.zMin or drop[0]**2 + drop[1]**2 > 2**.5:
                # Drop is out of range of any LEDs, delete it and make another
                del raindrops[i]
                raindrops.append(newDrop())
                continue
            for pixel in tree:
                if (pixel.x - drop[0])**2 + (pixel.y - drop[1])**2 < radius**2 and abs(pixel.z - drop[2]) < 2*radius:
                    pixel.setColor(drop[3])
        tree.show()
        tree.fade(0.8)

# Plays at 17 fps
def rainingRainbow():
    sections = 550
    colorDensity = 2.2
    colors = [C["RED"], C["ORANGE"], C["YELLOW"], C["GREEN"], C["CYAN"], C["BLUE"], [0, 128, 255], [0, 255, 96]]
    fuzzFactor = 1 # 0 for a sharp barrier between colors.  Larger it is from there, the fuzzier the barrier becomes.  Starts glitching after 1.  
    #sections = 550 # larger = slower (Adjusted for 30 fps)
    #colorDensity = 2.2 # Number of colors displayed at once
    while True:
        for z in np.linspace(tree.zMax, tree.zMax - len(colors) * tree.zRange / colorDensity, sections):
            for pixel in tree:
                index = int(np.floor((pixel.z - z) / (tree.zRange / colorDensity) + fuzzFactor * rng.random()) % len(colors))
                if pixel.color == colors[(index + 1) % len(colors)]:
                    index = (index + 1) % len(colors)
                pixel.setColor(colors[index])
            tree.show()

def randomFill(colors = C["COLORS"]):
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            # Assume function was provided a single color, make a list with just that color
            colors = [colors]
        Color = lambda: rng.choice(colors)
    tree.clear()
    on = 0
    while True:
        while on < tree.LED_COUNT:
            i = rng.integers(0, tree.LED_COUNT)
            if tree[i].color == C["OFF"]:
                on += 1
                tree[i] = Color()
                tree.show()
        sleep(1)
        while on > 0:
            i = rng.integers(0, tree.LED_COUNT)
            if not tree[i].color == C["OFF"]:
                on -= 1
                tree[i] = C["OFF"]
                tree.show()
        sleep(1)

def randomPlanes(colors = C["COLORS"]):
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    sections = 50 # Larger = slower
    while True:
        angleZ = rng.random() * 2 * np.pi
        angleX = rng.random() * np.pi
        newCoords = rotate(points = [pixel.coord for pixel in tree], x = angleX, z = angleZ)
        minZ = min(newCoords, key = lambda i: i[2])[2]
        maxZ = max(newCoords, key = lambda i: i[2])[2]
        zStep = (maxZ - minZ) / sections
        factor = 0.8 * rng.random() # Randomized fade speed
        tree.clear(False)
        color = Color()
        for z in np.linspace(minZ, maxZ + 1.5, sections):
            for i in range(len(newCoords)):
                if abs(newCoords[i][2] - z) < zStep:
                    tree[i] = color
            tree.show()
            tree.fade(factor)

# Rotates a given point a certain amount of radians around each axis
# Will rotate first around z, then x, then y.  If you want a different order,
# nest the function.  
def rotate(point = None, points = None, x = 0, y = 0, z = 0):
    if z != 0:
        zMatrix = [[np.cos(z), -np.sin(z), 0], [np.sin(z), np.cos(z), 0], [0, 0, 1]]
        if points is not None:
            points = [p @ zMatrix for p in points]
        else:
            point = point @ zMatrix
    if x != 0:
        xMatrix = [[1, 0, 0], [0, np.cos(x), -np.sin(x)], [0, np.sin(x), np.cos(x)]]
        if points is not None:
            points = [p @ xMatrix for p in points]
        else:
            point = point @ xMatrix
    if y != 0:
        yMatrix = [[np.cos(y), 0, np.sin(y)], [0, 1, 0], [-np.sin(y), 0, np.cos(y)]]
        if points is not None:
            points = [p @ yMatrix for p in points]
        else:
            point = point @ yMatrix
    if points is not None:
        return points
    return point

# Runs about 30 fps
def runFromCSV(name):
    PATH = "/home/pi/Desktop/TreeLights/CSVs/"
    frames = []
    with open(PATH + name + ".csv", "r") as f:
        time0 = time()
        file = f.read().split("\n")
        file.pop(0) # First line is column headers, not used
        file.pop(-1) # File ends on a linebreak so final element is empty
        for frameRaw in file:
            frame = []
            frameRaw = frameRaw.split(",")
            for i in range(1, len(frameRaw), 3): # First element is frame number, not used.
                color = [int(frameRaw[i+1]), # Subsequent elements are R, G, B values for each
                         int(frameRaw[i]), # LED in sequence, which are loaded here in G R B order
                         int(frameRaw[i+2])]
                frame.append(color)
            frames.append(frame)
        print(time() - time0, "seconds to process", len(file), "frames at", len(file) / (time() - time0), "fps.")
    while True:
        time1 = time()
        for frame in frames:
            for i in range(min(tree.LED_COUNT, len(frames))):
                tree[i] = frame[i]
            tree.show()
        print(len(frames), "frames in", round(time()-time1, 3), "seconds")

def seizure():
    while True:
        tree.fill(C["BLUE"])
        tree.show()
        tree.clear()
        tree.fill(C["YELLOW"])
        tree.show()
        tree.clear()

def sequence(colors = None):
    if colors == None:
        color = rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        color = rng.choice(colors)
    tree.clear()
    for pixel in tree:
        pixel.setColor(color)
        tree.show()

# 23.7 fps
def spirals(colors = [C["BLUE"], C["WHITE"], C["CYAN"], C["WHITE"]], numberOfSpirals = 4, spinCount = 2):
    if len(colors) < numberOfSpirals:
        print("Need to supply at least as many colors as spirals")
        return
    heightSections = 100
    angleStep = 2 * np.pi * spinCount / heightSections
    angle = 0
    offset = 0
    tree.clear(False)
    while True:
        for z in np.linspace(tree.zMin, tree.zMax, heightSections):
            for pixel in tree:
                if z >= pixel.z and z - pixel.z < tree.zRange / (heightSections - 1):
                    if abs(abs(abs(pixel.a + offset*2*np.pi/numberOfSpirals - angle) - np.pi) - np.pi) < (np.pi / numberOfSpirals):
                        pixel.setColor(colors[offset])
            tree.show()
            angle = (angle + angleStep) % (2 * np.pi)
        offset += 1
        if offset == numberOfSpirals:
            for i in range(20):
                tree.show()
            break

def spotlight(colors = [C["WHITE"], C["BLUE"]]):
    if colors == None:
        color1 = rng.integers(0, 256, 3)
        color2 = rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            print("Must supply at least two colors")
            return
        color1, color2 = rng.choice(colors, 2, False)
    radius = .5 # Of the spotlight
    radius *= radius
    z = tree.zMax * rng.random() # Spotlight's z-coordinate
    dz = .2 * rng.random()
    theta = 2 * np.pi * rng.random() # Spotlight's angle around z-axis
    dTheta = .2 * rng.random()
    # m and b used to calculate point on tree's surface from z and theta
    m = tree.xMax / (tree[tree.sortedX[-1]].z - tree[tree.sortedZ[-1]].z)
    b = -m * tree[tree.sortedZ[-2]].z
    while True:
        z += dz
        theta += dTheta
        if z > tree.zMax: dz = -1.3*dz # It tends to get stuck at the top, give it a little push
        if z < 0: dz = -1.05*dz
        point = [(m*z+b)*np.cos(theta), (m*z+b)*np.sin(theta)] + [z] # On or near surface of tree
        for pixel in tree:
            if pixel.surface and (pixel.x - point[0])**2 + (pixel.y - point[1])**2 + (pixel.z - point[2])**2 < radius:
                pixel.setColor(color1)
            else:
                pixel.setColor(color2)
        tree.show()
        dz = min(.1, max(-.1, dz + .06*rng.random() - 0.03))
        dTheta = min(.1, max(-.1, dTheta + .06*rng.random() - 0.03))

def test(color = C["WHITE"]):
    while True:
        tree.fill(color)
        tree.show()

def tinkerbell(colors = [C["WHITE"], C["OFF"]]):
    if colors == None:
        color1 = rng.integers(0, 256, 3)
        color2 = rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            print("Must supply at least two colors")
            return
        color1, color2 = colors[0], colors[1]
    radius = .2 # Of the spotlight
    t = 0
    dt = .08
    tailWidth = 2 # Factor of head radius
    tailLength = 12 # Factor of head radius
    # m and b used to calculate point on tree's surface from z and t
    m = tree.xMax / (tree[tree.sortedX[-1]].z - tree[tree.sortedZ[-1]].z)
    b = (-m * tree[tree.sortedZ[-2]].z)*0.85
    tree.clear(False)
    p = lambda t: ([(m*z+b)*np.cos(t), (m*z+b)*np.sin(t)] + [z])
    def helper(pixel):
        if pixel.flag[1] > 0:
            pixel.flag[1] -= 1
            return
        if pixel.flag[0] > 0:
            if True or np.floor(pixel.flag[0]/10) % 2 == 0:
                y = np.ceil(pixel.flag[0]/10)
                x = pixel.flag[0] % 10
                if y >= 3: f = .06
                if y == 2: f = .2
                if y == 1: f = 1
                if x == 9:
                    pixel.setColor(0.5 * f * np.array([C["WHITE"], [255, 255, 100]][rng.integers(0, 2)]))
                elif x == 8:
                    pixel.setColor(0.8 * f * np.array(pixel.color)/0.5)
                elif x == 7:
                    pixel.setColor(1.0 * f * np.array(pixel.color)/0.8)
                elif pixel.flag[0] % 10 > 4:
                    pass
                else:
                    pixel.setColor(0.8 * np.array(pixel.color))
            pixel.flag[0] -= 1
        else:
            pixel.flag = 0
    while True:
        z = 0.75#0.5*tree.zRange + .6*np.sin(1.44*(t+1)) + 0.5*np.sin(0.83*(t-1)) + 0.4*np.sin(2*(t-2)) - 0.2*np.sin(1.5*(t+2))
        point = p(t) # On or near surface of tree
        for pixel in tree:
            d = (pixel.x - point[0])**2 + (pixel.y - point[1])**2 + (pixel.z - point[2])**2
            if d < (tailWidth * radius)**2 and (pixel.flag == 0 or pixel.flag[2] > d):
                pixel.flag = [29, np.floor(0*d/radius) + np.floor(6*rng.random()) - 3, d]
            if d < 1.1*radius**2:
                pixel.flag = [69, np.floor(15*d/radius), d]
                pixel.setColor(C["WHITE"])
            if pixel.flag != 0:
                helper(pixel)
        tree.show()
        tree.fade(.8)
        t += dt

def wander(colors = None):
    white = False
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    elif colors == C["WHITE"] or colors == [C["WHITE"]]:
        Color = lambda: rng.integers(80, 231) * np.array([1, 1, 1])
        white = True
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    wander = 20
    for pixel in tree:
        pixel.setColor(Color())
    while True:
        for pixel in tree:
            drift = rng.integers(-wander, wander + 1)
            pixel.setColor([max((0, 30)[white], min(255, pixel.color[0] + (rng.integers(-wander, wander + 1), drift)[white])),
                            max((0, 30)[white], min(255, pixel.color[1] + (rng.integers(-wander, wander + 1), drift)[white])),
                            max((0, 30)[white], min(255, pixel.color[2] + (rng.integers(-wander, wander + 1), drift)[white]))])
        tree.show()

def twinkle(variant = 0):
    if variant == 0:
        setAll([50, 50, 50])
    elif variant == 1:
        setAllRandom(C["TREECOLORS"])
    else:
        setAllRandom(C["COLORS"])
    while True:
        for pixel in tree:
            if pixel.flag == 0 and rng.random() < 0.03:
                pixel.flag = 5
            if pixel.flag > 0:
                if pixel.flag >= 3:
                    f = (1 + (pixel.flag - 3)/(3*4))
                else:
                    f = 1/(1 + abs(pixel.flag - 3)/(3*4))
                c = np.array(pixel.color) * f
                c[0] = min(255, max(0, c[0]))
                c[1] = min(255, max(0, c[1]))
                c[2] = min(255, max(0, c[2]))
                pixel.setColor(c)
                pixel.flag -= 1
        tree.show()

def testConnectivity():
    totalConnections = 0
    loneLEDs = 0
    poorlyConnected = 0
    for pixel in tree:
        connections = len(pixel.neighbors)
        totalConnections += connections
        pixel.setColor(C["GREEN"])
        if connections < 4:
            poorlyConnected += 1
            pixel.setColor(C["YELLOW"])
        if connections == 2:
            loneLEDs += 1
            pixel.setColor(C["RED"])
    print(totalConnections, "connections among", tree.LED_COUNT, "with", loneLEDs, "neighborless LEDs and", poorlyConnected,
          "poorly connected LEDs, and an average of", totalConnections/tree.LED_COUNT, "connections per LED")
    tree.show()
    input()
    while True:
        for pixel in tree:
            tree.clear(False)
            pixel.setColor(C["RED"])
            for neighbor in pixel.neighbors:
                neighbor.setColor(C["GREEN"])
            tree.show()
            #sleep(0.1)
            input()
