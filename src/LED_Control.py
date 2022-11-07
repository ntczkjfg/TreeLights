from Common_Variables import rng, tree, mTree
from StaticEffects import *
from Transitions import *
from Colors import *
from TestingFunctions import *
from HelperFunctions import *
import numpy as np
import os
from time import sleep, time

# When the tree first receives power, some lights turn on randomly - clear to fix
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

# A growing and shrinking cylinder that changes the tree colors
def cylinder(colors = COLORS, duration = 99999):
	startTime = time()
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
    midZ = tree.zRange/2 + tree.zMin
    rRange = 2**.5
    minR = rRange / 4
    sections = 20 # Larger = slower
    while time() - startTime < duration:
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

# Looks like a cylon's eyes
def cylon(duration = 99999):
	startTime = time()
    tree.clear()
    center = 0
    deltaC = 0.1
    while time() - startTime < duration:
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

# Displays the images in sequence, requires keyboard input
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

# Courtesy of Arby
# A bouncing rainbow ball that changes size and wobbles
def pulsatingRainbow(duration = 99999):
	startTime = time()
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
    while time() - startTime < duration:
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

# A growing and shrinking spear that moves up and down and changes colors
def pulsatingSphere(colors = None, duration = 99999):
	startTime = time()
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
    while time() - startTime < duration:
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

# A raining effect
def rain(colors = [[55, 55, 255]], duration = 99999):
	startTime = time()
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
    while time() - startTime < duration:
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

# Courtesy of Nekisha
# A rainbow rains down from above
def rainingRainbow(duration = 99999):
	startTime = time()
    sections = 400 # larger = slower (550 for 30 fps)
    colorDensity = 2.4 # Number of colors displayed at once
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, [0, 128, 255], [0, 255, 96]]
    fuzzFactor = 1 # 0 for a sharp barrier between colors.  Larger it is from there, the fuzzier the barrier becomes.  Starts glitching after 1.  
    while time() - startTime < duration:
        for z in np.linspace(tree.zMax, tree.zMax - len(colors) * tree.zRange / colorDensity, sections):
            for pixel in tree:
                index = int(np.floor((pixel.z - z) / (tree.zRange / colorDensity) + fuzzFactor * rng.random()) % len(colors))
                if pixel.color == colors[(index + 1) % len(colors)]:
                    index = (index + 1) % len(colors)
                pixel.setColor(colors[index])
            tree.show()

# Turns lights on one at a time in random order in random colors, then turns them off in the same fashion
def randomFill(colors = COLORS, cycles = 99999):
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            # Assume function was provided a single color, make a list with just that color
            colors = [colors]
        Color = lambda: rng.choice(colors)
    tree.clear()
    on = 0
    for cycle in range(cycles):
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

# Random colored planes fly through the tree, leaving trails
def randomPlanes(colors = COLORS, duration = 99999):
	startTime = time()
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    sections = 50 # Larger = slower
    while time() - startTime < duration:
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

# Rapid flashing of blue and yellow
def seizure(duration = 99999):
	startTime = time()
    while time() - startTime < duration:
        tree.fill(BLUE)
        tree.show()
        tree.clear()
        tree.fill(YELLOW)
        tree.show()
        tree.clear()

# Lights up each LED in their wiring order
def sequence(colors = None, cycles = 1):
	for cycle in range(cycles):
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

# Plays the game "snake"
def snake(cycles = 99999):
    head = rng.choice(tree)
    pellet = rng.choice(tree)
    length = 1
    head.flag = length
    tree.clear(False)
    for cycle in range(cycles):
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

# Rotates two colors through the tree about the viewing axis
def spinner(colors = [WHITE, BLUE], duration = 99999):
	startTime = time()
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
    speed = 0.1
    height = 1.7
    theta = 0#np.pi/2 # Clockwise angle around z-axis
    phi = np.pi/2 # Angle from positive z-axis
    t = 0
    while time() - startTime < duration:
        newCoords = transform(tree.coordinates, z = -height, zr = -theta, xr = t, yr = np.pi/2 - phi)
        for i, coord in enumerate(newCoords):
            if coord[2] > 0:
                tree[i].setColor(color1)
            else:
                tree[i].setColor(color2)
        tree.show()
        t += speed

# Rotates a plane through the viewing axis
def spinningPlane(duration = 99999):
	startTime = time()
    color = BLUE
    speed = 0.1
    height = 1.7
    theta = 0#np.pi/2 # Clockwise angle around z-axis
    phi = np.pi/2 # Angle from positive z-axis
    t = 0
    while time() - startTime < duration:
        newCoords = transform(tree.coordinates, z = -height, zr = -theta, xr = t, yr = np.pi/2 - phi)
        for i, coord in enumerate(newCoords):
            if np.abs(coord[2]) < 0.1:
                tree[i].setColor(color)
            else:
                tree[i].setColor(OFF)
        tree.show()
        t += speed

# Creates spirals
def spirals(colors = [RED, ORANGE, YELLOW, GREEN, BLUE, CYAN, PURPLE], spinCount = 2, cycles = 99999):#[BLUE, WHITE, CYAN, WHITE], spinCount = 2):
    numberOfSpirals = len(colors)
    heightSections = 80
    angleStep = 2 * np.pi * spinCount / heightSections
    angle = 0
    offset = 0
    tree.clear(False)
    for cycle in range(cycles):
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

# Has a circle wander around the tree
def spotlight(colors = [WHITE, BLUE], duration = 99999):
	startTime = time()
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
    while time() - startTime < duration:
        z += dz
        theta += dTheta
        if z > tree.zMax:dz = -abs(dz) # It tends to get stuck at the top, give it a little push
        if z < 0: dz = abs(dz)
        point = [(m*z+b)*np.cos(theta), (m*z+b)*np.sin(theta)] + [z] # On or near surface of tree
        for pixel in tree:
            if pixel.surface and (pixel.x - point[0])**2 + (pixel.y - point[1])**2 + (pixel.z - point[2])**2 < radius:
                pixel.setColor(color1)
            else:
                pixel.setColor(color2)
        tree.show()
        dz = min(.1, max(-.1, dz + .06*rng.random() - 0.03))
        dTheta = min(.1, max(-.1, dTheta + .06*rng.random() - 0.03))

# Rotates vertical stripes around the tree while changing the color of every other stripe
def stripedFill(duration = 99999):
	startTime = time()
    numberOfStripes = 3
    angleDiff = 2 * np.pi / numberOfStripes
    stripeThickness = np.pi/3 # In radians
    stripeThickness /= 2
    zStep = 0.0003
    staticColor = (70, 10, 10)
    firstColor = (5, 90, 5)
    secondColor = staticColor
    z = tree.zMin
    while time() - startTime < duration:
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

# Sets all LEDs randomly then lets their brightness vary
def twinkle(variant = 0, duration = 99999):
	startTime = time()
    if variant == 0:
        setAll([50, 50, 50])
    elif variant == 1:
        setAllRandom(TREECOLORS)
    else:
        setAllRandom(COLORS)
    while time() - startTime < duration:
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

# Sets all LEDs at random then lets their colors gradually change
def wander(colors = None, duration = 99999):
	startTime = time()
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
    while time() - startTime < duration:
        for pixel in tree:
            drift = rng.integers(-wander, wander + 1)
            pixel.setColor([max((0, 30)[white], min(255, pixel.color[0] + (rng.integers(-wander, wander + 1), drift)[white])),
                            max((0, 30)[white], min(255, pixel.color[1] + (rng.integers(-wander, wander + 1), drift)[white])),
                            max((0, 30)[white], min(255, pixel.color[2] + (rng.integers(-wander, wander + 1), drift)[white]))])
        tree.show()

# Spirals out from the tree's z-axis, in rainbow colors
def zSpiral(twists = 4, sections = 110, cycles = 99999):
    angle = 0
    deltaA = 2 * np.pi * twists / sections
    
    rs = [pixel.r for pixel in tree]
    r = min(rs)
    deltaR = (max(rs)-r)/sections
    
    Color = lambda i: [255 * max(-3*np.abs(i/sections - 1/3) + 1.0, 0),
                       255 * max( 3*np.abs(i/sections - 0.5) - 0.5, 0),
                       255 * max(-3*np.abs(i/sections - 2/3) + 1.0, 0)]
    for cycle in cycles:
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

# Puts on a curated show of effects
def show():
	pass