from Common_Variables import rng, tree, mTree
from StaticEffects import *
from Transitions import *
from Colors import *
import numpy as np
import os
from time import sleep, time

tree.clear()
tree.clear()

# Random stripes
# Falling Matrix trails
# Expanding shapes from center
# Expanding / contracting stripes at random angles
# Letters
# Small number of points moving around with fading trails
# Sierpinski?
# Fire?
# Tartan
# Accumulating snow
# Clock
# Breakout
# Look like a traffic cone, wizard hat, pizza slice
# Quicker rain from cloud
# Barbershop poll
# Falling leaves
# Jack-o-lantern?

# Thanks Arby
def pulsatingRainbow():
    radius = .8
    dR = 0.01
    minR = 0.4
    maxR = 1
    zAngle = 0
    dZ = 0.03
    maxZ = np.pi/3
    angle = 0
    dA = 0.1
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]
    height = 0
    acc = -0.01
    dH = .25
    while True:
        points = transform(tree.coordinates, z = -height, yr = -zAngle, zr = -angle)
        for i in range(len(points)):
            if points[i][0]**2 + points[i][1]**2 + points[i][2]**2 <= radius**2:
                tree[i].setColor(colors[int(np.floor((4 * points[i][2]/ radius) + 4))])
        tree.show()
        radius += dR
        if radius >= maxR:
            dR *= -1
            radius += 2*dR
        if radius <= minR:
            dR *= -1
            radius += 2*dR
        zAngle += dZ
        if zAngle > maxZ:
            dZ *= -1
            zAngle += 2*dZ
        if zAngle < -maxZ:
            dZ *= -1
            zAngle += 2*dZ
        angle += dA
        if angle > 2*np.pi:
            angle = angle - 2*np.pi
        dH += acc
        height += dH
        if height < 0:
            height -= dH
            dH = .25
        tree.clear(UPDATE = False)

def zSpiral(twists = 4, sections = 110):
    angle = 0
    deltaA = 2 * np.pi * twists / sections
    
    rs = [pixel.r for pixel in tree]
    r = min(rs)
    deltaR = (max(rs)-r)/sections
    
    Color = lambda i: [255 * max(-3*np.abs(i/sections - 1/3) + 1.0, 0),
                       255 * max( 3*np.abs(i/sections - 0.5) - 0.5, 0),
                       255 * max(-3*np.abs(i/sections - 2/3) + 1.0, 0)]
    
    tree.clear(False)
    for i in range(sections):
        color = Color(i)
        for pixel in tree:
            if (pixel.a - angle) % (2 * np.pi) <= deltaA:
                if pixel.r < r + deltaR and pixel.r > r - deltaR * (2 * np.pi / deltaA):
                    pixel.setColor(color)
        tree.show()
        angle = (angle + deltaA) % (2 * np.pi)
        r += deltaR
        tree.show()
    for angle in np.linspace(0, 2*np.pi, int(sections/twists)):
        for pixel in tree:
            if pixel.color == OFF and pixel.a <= angle:
                pixel.setColor(RED)
        tree.show()

def stripedFill():
    numberOfStripes = 3
    angleDiff = 2 * np.pi / numberOfStripes
    stripeThickness = np.pi/3 # In radians
    stripeThickness /= 2
    zStep = 0.0003
    staticColor = (70, 10, 10)
    firstColor = (5, 90, 5)
    secondColor = staticColor
    z = tree.zMin
    while True:
        for angle in np.linspace(0, angleDiff, 40):
            for pixel in tree:
                if abs(abs(abs((pixel.a % angleDiff) - angle) - angleDiff/2) - angleDiff/2) < stripeThickness:
                    pixel.setColor(staticColor)
                else:
                    if z > tree.zMax or z < tree.zMin:
                        z = tree.zMin
                        firstColor, secondColor = secondColor, firstColor
                    z += zStep
                    if pixel.z < z:
                        pixel.setColor(firstColor)
                    else:
                        pixel.setColor(secondColor)
            tree.show()

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

def cylinder(colors = COLORS):
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
    sections = 20 # Larger = slower
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
    PAT = "/home/pi/Desktop/TreeLights/Images/"
    imgList = os.listdir(PAT)
    for image in imgList:
        displayImage(image)
        input()
        displayImage2(image)
        print(image[:-4])
        input()
    tree.clear()

def displayImage2(fileName, markTemplate = False):
    PATH = "/home/pi/Desktop/TreeLights/Images/" + fileName
    eye = np.array([0, 4.5, 2.2])
    with Image.open(PATH) as im:
        img = im.load()
        tree.clear(False)
        for pixel in tree:
            vect = eye - pixel.coordinate
            t = -eye[1] / vect[1]
            x = (-(vect[0]*t + eye[0]) + 1) * im.size[0]/2
            y = im.size[1] - (vect[2]*t + eye[2])*im.size[1]/tree.zMax
            if x < 0 or y < 0 or x > im.size[0] - 1 or y > im.size[1] - 1:
                continue
            if markTemplate:
                im.putpixel((int(x), int(y)), (0, 0, 0, 255))
            else:
                color = list(img[x, y][0:3])
                color[0], color[1] = color[1], color[0]
                if color != [28, 237, 36]:
                    pixel.setColor(color)
        if markTemplate:
            im.save(PATH[:-4] + "_marked.png")
    tree.show()

def pandemic():
    initialSickRate = 0.05
    newDiseaseRate = 0.001
    mutationRate = 0.3
    fatalityRate = 9999 # Larger = less death
    meanDuration = 40
    interactionRate = 0.4
    tree.clear(False)
    for pixel in tree:
        pixel.flag = [None, rng.random(), 0, []] # [disease, immunity, duration, history]
        if rng.random() < initialSickRate:
            disease = [rng.integers(1, 5), rng.random()**fatalityRate, rng.random(), 0] # [infectivity, fatality, duration, variant]
            pixel.flag[0] = disease
            pixel.flag[2] = (1-pixel.flag[1])*disease[2]*2*meanDuration
            pixel.flag[3].append(disease)
            pixel.setColor(rng.integers(0, 256, 3))
    j = 0
    while True:
        j += 1
        for pixel in tree:
            if pixel.flag == -1:
                continue # Dead
            if pixel.flag[0] == None:
                if rng.random() < newDiseaseRate:
                    disease = [rng.integers(1, 5), rng.random()**fatalityRate, rng.random(), 0]
                    pixel.flag[0] = disease
                    pixel.flag[2] = (1-pixel.flag[1])*disease[2]*2*meanDuration
                    pixel.flag[3].append(disease)
                    pixel.setColor(rng.integers(0, 256, 3))
                continue
            if rng.random() < interactionRate:
                for i in range(int(pixel.flag[0][0])):
                    victim = rng.choice(pixel.neighbors)
                    if victim.flag == -1: continue
                    if rng.random()*pixel.flag[0][0] > victim.flag[1] and pixel.flag[0] not in victim.flag[3]:
                        victim.setColor(pixel.color)
                        victim.flag[0] = pixel.flag[0]
                        victim.flag[2] = rng.random() * (1 - victim.flag[1]) * victim.flag[0][2] * 2 * meanDuration
                        victim.flag[3].append(victim.flag[0])
                        if rng.random() < mutationRate:
                            victim.flag[0][3] += 1
                    elif victim.flag[0] != None and rng.random()*victim.flag[0][0] > pixel.flag[1] and victim.flag[0] not in pixel.flag[3]:
                        pixel.setColor(victim.color)
                        pixel.flag[0] = victim.flag[0]
                        pixel.flag[2] = rng.random() * (1 - pixel.flag[1]) * pixel.flag[0][2] * 2 * meanDuration
                        pixel.flag[3].append(pixel.flag[0])
                if rng.random() < mutationRate:
                    pixel.flag[0][3] += 1
            pixel.flag[2] -= 1
            if pixel.flag[2] <= 0:
                if rng.random() < pixel.flag[0][1]:
                    pixel.flag = -1
                    pixel.setColor(RED)
                    continue
                pixel.setColor(OFF)
                pixel.flag[0] = None
                pixel.flag[2] = 0
        tree.show()

# For testing purposes only
def planar():
    sections = 20
    zRange = tree.zRange / sections
    xRange = tree.xRange / sections
    yRange = tree.yRange / sections
    for z in np.linspace(tree.zMin, tree.zMax, sections + 1):
        continue
        tree.clear(False)
        for pixel in tree:
            if pixel.coordinate[2] >= z and pixel.coordinate[2] <= z + zRange:
                pixel.setColor(WHITE)
        tree.show()
        print("Showing z from", round(z, 5), "to", round(z + zRange, 5))
        input()
    for x in np.linspace(tree.xMin, tree.xMax, sections + 1):
        tree.clear(False)
        for pixel in tree:
            if pixel.coordinate[0] >= x and pixel.coordinate[0] <= x + xRange:
                pixel.setColor(WHITE)
        tree.show()
        print("Showing x from", round(x, 5), "to", round(x + xRange, 5))
        input()
    for y in np.linspace(tree.yMin, tree.yMax, sections + 1):
        continue
        tree.clear(False)
        for pixel in tree:
            if pixel.coordinate[1] >= y and pixel.coordinate[1] <= y + yRange:
                pixel.setColor(WHITE)
        tree.show()
        print("Showing y from", round(y, 5), "to", round(y + yRange, 5))
        input()
    tree.clear()

def pulsatingSphere(colors = None):
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    color1 = Color()
    color2 = BLACK
    while np.array_equal(color1, color2): color2 = Color()
    height = 1.3
    minH = 0.6
    maxH = 2
    deltaH = 0.04
    maxR = 1
    r = 0.31
    deltaR = 0.04
    while True:
        if r <= 0:
            deltaR *= -1
            r += deltaR
            color1 = color2
            while np.array_equal(color1, color2): color1 = rng.choice(COLORS)
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
    newDrop = lambda: [(2*rng.random() - 1) * tree.xRange / 4, (2*rng.random() - 1) * tree.yRange / 4, tree.zMax + rng.random() * 2, Color()]
    raindrops = [newDrop() for i in range(dropCount)]
    while True:
        for i, drop in enumerate(raindrops):
            # Next two lines make drop move away from the trunk, third line makes them move down
            drop[0] *= 1.03
            drop[1] *= 1.03
            drop[2] -= .15
            if drop[2] < tree.zMin or drop[0]**2 + drop[1]**2 > 2:
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
    sections = 400 # larger = slower (550 for 30 fps)
    colorDensity = 2.4 # Number of colors displayed at once
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, [0, 128, 255], [0, 255, 96]]
    fuzzFactor = 1 # 0 for a sharp barrier between colors.  Larger it is from there, the fuzzier the barrier becomes.  Starts glitching after 1.  
    while True:
        for z in np.linspace(tree.zMax, tree.zMax - len(colors) * tree.zRange / colorDensity, sections):
            for pixel in tree:
                index = int(np.floor((pixel.z - z) / (tree.zRange / colorDensity) + fuzzFactor * rng.random()) % len(colors))
                if pixel.color == colors[(index + 1) % len(colors)]:
                    index = (index + 1) % len(colors)
                pixel.setColor(colors[index])
            tree.show()

def randomFill(colors = COLORS):
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
            if tree[i].color == OFF:
                on += 1
                tree[i] = Color()
                tree.show()
        sleep(1)
        while on > 0:
            i = rng.integers(0, tree.LED_COUNT)
            if not tree[i].color == OFF:
                on -= 1
                tree[i] = OFF
                tree.show()
        sleep(1)

def randomPlanes(colors = COLORS):
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
        newCoords = transform(tree.coordinates, xr = angleX, zr = angleZ)
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

# Runs about 30 fps
def runFromCSV(name, m = None):
    if m == None:
        m = [i for i in range(tree.LED_COUNT)]
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
            for i in range(min(tree.LED_COUNT, len(frame))):
                try:
                    tree[m[i]] = frame[i]
                except IndexError:
                    print(i)
                    x = 1/0
            tree.show()
        print(len(frames), "frames in", round(time()-time1, 3), "seconds")
        break

def seizure():
    while True:
        tree.fill(BLUE)
        tree.show()
        tree.clear()
        tree.fill(YELLOW)
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

def snake():
    head = rng.choice(tree)
    pellet = rng.choice(tree)
    length = 1
    head.flag = length
    tree.clear(False)
    while True:
        if head == pellet:
            length += 1
            pellet = rng.choice(tree)
            while pellet.flag > 0: pellet = rng.choice(tree)
        choice = None
        for neighbor in head.neighbors:
            if neighbor.flag == 0 and (choice == None or np.linalg.norm(neighbor.coordinate - pellet.coordinate) < np.linalg.norm(choice.coordinate - pellet.coordinate)):
                choice = neighbor
        if choice == None:
            break
        head = choice
        head.flag = length
        for pixel in tree:
            if pixel.flag > 0:
                f = 1 - pixel.flag / length
                pixel.setColor([max(765*(-np.abs(f-1/3)+1/3), 0), max(510*(np.abs(f-0.5) - 1/6), 0), max(765*(-np.abs(f-2/3)+1/3), 0)])
                pixel.flag -= 1
            else:
                pixel.setColor(OFF)
        pellet.setColor(WHITE)
        tree.show()
        sleep(0.03)
    sleep(2)
    snake()

def spinner(colors = [YELLOW, BLUE]):
    if colors == None:
        color1 = rng.integers(0, 256, 3)
        color2 = rng.integers(0, 256, 3)
    else:
        if type(colors[0]) == list and len(colors) == 2:
            color1 = colors[0]
            color2 = colors[1]
        else:
            print("Must give exactly two colors for this effect")
            return
    color1 = BLUE
    color2 = YELLOW
    speed = 0.1
    height = 1.7
    theta = 0#np.pi/2 # Clockwise angle around z-axis
    phi = np.pi/2 # Angle from positive z-axis
    t = 0
    while True:
        newCoords = transform(tree.coordinates, z = -height, zr = -theta, xr = t, yr = np.pi/2 - phi)
        for i, coord in enumerate(newCoords):
            if coord[2] > 0:
                tree[i].setColor(color1)
            else:
                tree[i].setColor(color2)
        tree.show()
        t += speed

def spinningPlane():
    color = BLUE
    speed = 0.1
    height = 1.7
    theta = 0#np.pi/2 # Clockwise angle around z-axis
    phi = np.pi/2 # Angle from positive z-axis
    t = 0
    while True:
        newCoords = transform(tree.coordinates, z = -height, zr = -theta, xr = t, yr = np.pi/2 - phi)
        for i, coord in enumerate(newCoords):
            if np.abs(coord[2]) < 0.1:
                tree[i].setColor(color)
            else:
                tree[i].setColor(OFF)
        tree.show()
        t += speed

def cylon():
    tree.clear()
    center = 0
    deltaC = 0.1
    while True:
        center += deltaC
        if center > tree.yMax:
            deltaC *= -1
            center += 2 * deltaC
        if center < tree.yMin:
            deltaC *= -1
            center += 2 * deltaC
        for pixel in tree:
            dist = np.abs(pixel.y - center)
            color = [0, max(10, -130/.3*dist + 130), 0]
            pixel.setColor(color)
        tree.show()

def spirals(colors = [RED, ORANGE, YELLOW, GREEN, BLUE, CYAN, PURPLE], numberOfSpirals = 7, spinCount = 2):#[BLUE, WHITE, CYAN, WHITE], numberOfSpirals = 4, spinCount = 2):
    if len(colors) < numberOfSpirals:
        print("Need to supply at least as many colors as spirals")
        return
    heightSections = 80
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
            tree.clear()
            offset = 0 
            #break

def spotlight(colors = [WHITE, BLUE]):
    if colors == None:
        color1 = rng.integers(0, 256, 3)
        color2 = rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            print("Must supply at least two colors")
            return
        color1, color2 = colors[0], colors[1]
    radius = .4 # Of the spotlight
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

def spotlight2(colors = [WHITE, BLUE]):
    if colors == None:
        color1 = rng.integers(0, 256, 3)
        color2 = rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            print("Must supply at least two colors")
            return
        color1, color2 = colors[0], colors[1]
    radius = .4 # Of the spotlight
    radius *= radius
    z = lambda t:-tree.zMax * (0.5 + 0.14*(np.sin(2*t) + np.sin(.3*t) + np.sin(5*t) + np.sin(.7*t) + np.sin(11*t)))
    theta = lambda t:10*np.pi*0.26*(np.sin(.1*t) + np.sin(4*t) + np.sin(.6*t) + np.sin(8*t) + np.sin(.9*t))
    t = rng.integers(-1000, 1001)
    while True:
        t += 0.015
        newCoords = transform(tree.coordinates, z = z(t), zr = theta(t/7))
        for i, coord in enumerate(newCoords):
            if tree[i].surface and coord[0] > 0 and coord[1]**2 + coord[2]**2 < radius:
                tree[i].setColor(color1)
            else:
                tree[i].setColor(color2)
        tree.show()

def test(color = WHITE):
    if color is not None: tree.fill(color)
    while True:
        tree.show()

def testSurface(interior = BLUE, surface = RED):
    setAll(interior)
    for pixel in tree:
        if pixel.surface: pixel.setColor(surface)
    tree.show()

def tinkerbell(colors = [WHITE, OFF]):
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
                    pixel.setColor(0.5 * f * np.array([WHITE, [255, 255, 100]][rng.integers(0, 2)]))
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
                pixel.setColor(WHITE)
            if pixel.flag != 0:
                helper(pixel)
        tree.show()
        tree.fade(.8)
        t += dt

# Translates a point or array of points by x, y, and z, then rotates clockwise by zr,
# yr, and xr radians around each axis, in that order
def transform(points, x = 0, y = 0, z = 0, xr = 0, yr = 0, zr = 0):
    if x != 0 or y != 0 or z != 0:
        points = points + [x, y, z]
    if zr != 0:
        zMatrix = [[np.cos(zr), -np.sin(zr), 0], [np.sin(zr), np.cos(zr), 0], [0, 0, 1]]
        points = points @ zMatrix
    if yr != 0:
        yMatrix = [[np.cos(yr), 0, np.sin(yr)], [0, 1, 0], [-np.sin(yr), 0, np.cos(yr)]]
        points = points @ yMatrix
    if xr != 0:
        xMatrix = [[1, 0, 0], [0, np.cos(xr), -np.sin(xr)], [0, np.sin(xr), np.cos(xr)]]
        points = points @ xMatrix
    return points

def wander(colors = None):
    white = False
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    elif colors == WHITE or colors == [WHITE]:
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
        setAllRandom(TREECOLORS)
    else:
        setAllRandom(COLORS)
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
    while True:
        for pixel in tree:
            tree.clear(False)
            pixel.setColor(RED)
            for neighbor in pixel.neighbors:
                neighbor.setColor(GREEN)
            tree.show()
            input()

def findTreeNeighbors(distances = None):
    if distances == None:
        distances = []
        for mPixel in mTree:
            dists = []
            for pixel in tree:
                dists.append(((mPixel.x - pixel.x)**2 + (mPixel.y - pixel.y)**2 + (mPixel.z - pixel.z)**2)**0.5)
            distances.append(dists)
    newMap = [dists.index(min(dists)) for dists in distances]
    iCounts = []
    for i in range(tree.LED_COUNT):
        iCounts.append(newMap.count(i))
    redo = False
    for i in range(len(iCounts)):
        if iCounts[i] > 1 and i != newMap[0]:
            redo = True
            reps = [newMap.index(i)]
            for j in range(1, iCounts[i]):
                reps.append(newMap.index(i, reps[-1] + 1))
            dists = [distances[k][i] for k in reps]
            del reps[dists.index(min(dists))]
            for k in reps:
                distances[k][i] = 1000000
    if redo:
        return findTreeNeighbors(distances)
    return newMap
B = [371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 372, 226, 387, 373, 206, 374, 293, 379, 294, 292, 295, 376, 375, 377, 227, 378, 224, 367, 370, 228, 296, 230, 368, 29, 31, 600, 398, 199, 391, 289, 200, 201, 399, 395, 390, 299, 1, 225, 297, 203, 202, 392, 298, 500, 393, 396, 389, 96, 388, 397, 394, 98, 16, 300, 11, 400, 0, 322, 321, 318, 101, 5, 97, 20, 316, 12, 15, 315, 317, 313, 592, 591, 590, 304, 303, 305, 589, 306, 307, 588, 326, 309, 308, 311, 586, 314, 312, 725, 265, 310, 585, 724, 264, 587, 584, 271, 327, 262, 726, 261, 266, 583, 263, 582, 267, 332, 721, 681, 684, 409, 575, 330, 48, 46, 38, 37, 105, 192, 45, 39, 41, 407, 719, 57, 92, 106, 47, 49, 277, 276, 268, 578, 259, 581, 676, 728, 260, 7, 729, 343, 270, 363, 253, 579, 730, 248, 245, 731, 247, 246, 338, 269, 249, 341, 732, 739, 340, 673, 668, 242, 734, 339, 738, 733, 672, 748, 736, 667, 665, 241, 663, 735, 664, 362, 449, 237, 238, 365, 235, 222, 232, 233, 9, 223, 448, 240, 239, 662, 221, 220, 234, 661, 236, 445, 361, 231, 366, 208, 213, 51, 356, 655, 211, 656, 283, 357, 358, 360, 209, 670, 658, 218, 212, 659, 749, 219, 660, 747, 737, 216, 359, 210, 444, 443, 554, 442, 284, 441, 457, 510, 437, 438, 355, 154, 433, 626, 552, 653, 625, 353, 354, 352, 351, 281, 558, 624, 555, 347, 217, 346, 657, 745, 666, 254, 742, 744, 348, 572, 279, 335, 334, 256, 278, 740, 746, 743, 243, 741, 675, 257, 336, 674, 244, 252, 337, 250, 577, 258, 251, 727, 677, 580, 273, 576, 722, 678, 723, 679, 275, 680, 274, 195, 613, 102, 325, 329, 405, 194, 324, 404, 702, 402, 614, 704, 701, 615, 603, 607, 403, 612, 499, 44, 93, 418, 189, 181, 497, 288, 498, 502, 501, 386, 290, 204, 503, 205, 385, 504, 291, 384, 381, 382, 509, 454, 453, 507, 506, 455, 505, 440, 380, 207, 383, 508, 287, 439, 496, 187, 285, 456, 286, 186, 458, 495, 182, 512, 185, 184, 494, 163, 515, 628, 110, 71, 491, 111, 517, 492, 644, 645, 518, 643, 516, 493, 183, 629, 513, 630, 162, 511, 627, 460, 514, 164, 463, 145, 489, 521, 526, 144, 542, 479, 134, 128, 132, 135, 142, 136, 139, 138, 137, 478, 480, 131, 528, 529, 487, 648, 647, 486, 176, 636, 420, 415, 413, 618, 706, 417, 567, 410, 408, 695, 568, 156, 687, 157, 67, 79, 562, 564, 649, 428, 143, 126, 547, 477, 476, 545, 544, 543, 520, 539, 548, 549, 468, 429, 430, 118, 148, 650, 171, 170, 561, 560, 557, 553, 169, 652, 651, 80, 432, 147, 68, 551, 550, 435, 434, 167, 436, 654, 459, 166, 153, 461, 165, 462, 70, 69, 120, 525, 464]

def CSVshow():
    tree.clear()
    csvList = os.listdir("/home/pi/Desktop/TreeLights/CSVs/")
    for csv in csvList:
        tree.clear()
        input("Press enter to play " + csv)
        try:
            runFromCSV(csv[:-4], B)
        except KeyboardInterrupt:
            pass
    tree.clear()
    print("Done")

def saveCoordinates():
    import pickle
    coordinates = [list(pixel.coordinate) for pixel in tree]
    with open("/home/pi/Desktop/TreeLights/Trees/coordinates.list", "wb") as f:
        pickle.dump(coordinates, f)

from multiprocessing import Process
from time import time, sleep
from random import choice
def randomEffects():
    funcs = [pulsatingRainbow, zSpiral, stripedFill, sequence, cylinder, pulsatingSphere, rain, spirals
             , rainingRainbow, randomFill, randomPlanes, snake, spinner, spinningPlane, cylon, spotlight, wander, twinkle]
    while True:
        effect = choice(funcs)
        print(effect)
        p1 = Process(target=effect)
        p1.start()
        sleep(90)
        p1.terminate()
#randomEffects()
    