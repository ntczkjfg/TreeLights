from Common_Variables import rng, tree, PI, TAU
from Colors import *
from Simple_Effects import *
from Helper_Functions import *
from Testing_Functions import *
from Effect_Control import *
import numpy as np
from time import sleep, time
from os import listdir
import datetime

# Random stripes
# Expanding shapes from center
# Expanding / contracting stripes at random angles
# Letters
# Small number of points moving around with fading trails
# Sierpinski?
# Tartan
# Digital Clock
# Breakout
# Look like a traffic cone, wizard hat
# Falling leaves
# Jack-o-lantern?                

# Rotates the tree while running alternatingly colored vertical stripes alternatingly up and down
def alternatingStripes(colors = [[0, 10, 90], [5, 90, 5], [70, 15, 15]], duration = np.inf):
    startTime = time()
    if colors == None:
        colors = [[0, 10, 90], [5, 90, 5], [70, 15, 15]]
    else:
        if type(colors[0]) != list or len(colors) != 3:
            print("Must supply exactly three colors for this effect.")
            return
    numberOfStripes = 2
    angleDiff = 0
    dAngle = -0.00025
    z = tree.zMin
    dz = 0.0003
    while time() - startTime < duration:
        tree.clear(UPDATE = False)
        for pixel in tree:
            if not pixel.surface: continue
            pixel.setColor(colors[0])
            if ((pixel.a + angleDiff) // (PI/numberOfStripes)) % 2 == 0:
                if pixel.z < z and pixel.z > z - tree.zRange:
                    pixel.setColor(colors[1])
            else:
                if pixel.z > tree.zMax - z and pixel.z < tree.zMax - z + tree.zRange:
                    pixel.setColor(colors[2])
            z += dz
            if z > 2 * tree.zMax:
                dz = -abs(dz)
            if z < tree.zMin:
                dz = abs(dz)
            angleDiff = (angleDiff + dAngle) % TAU
        tree.show()

# Blinks lights on and off
def blink(colors = TRADITIONALCOLORS, groups = 7, p = 0.7, slowness = 1, duration = np.inf):
    startTime = time()
    setAllRandom(colors)
    tree.clear(FLAGSONLY = True)
    for pixel in tree:
        pixel.flag = [rng.integers(0, groups), pixel.color]
    while time() - startTime < duration:
        groupStatuses = [True if rng.random() < p else False for i in range(groups)]
        sleep(slowness)
        for pixel in tree:
            if not groupStatuses[pixel.flag[0]]:
                pixel.setColor(OFF)
            else:
                pixel.setColor(pixel.flag[1])
        tree.show()
        tree.show()

# Courtesy of Arby
# A bouncing rainbow ball that changes size and wobbles
def bouncingRainbowBall(duration = np.inf):
    startTime = time()
    radius = .7
    dR = 0.01
    minR = 0.4
    maxR = .75
    zAngle = 0
    dZ = 0.03
    maxZ = PI/3
    angle = 0
    dA = 0.1
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]
    height = radius
    acc = -0.01
    initialV = 0.21
    dH = initialV
    while time() - startTime < duration:
        points = transform(tree.coordinates, z = -height, yr = -zAngle, zr = -angle)
        for i in range(len(points)):
            if points[i][0]**2 + points[i][1]**2 + points[i][2]**2 <= radius**2:
                tree[i].setColor(colors[int(4 * points[i][2] / radius + 4)])
        tree.show()
        radius += dR
        if radius >= maxR:
            dR = -abs(dR)
            radius += dR
        if radius <= minR:
            dR = abs(dR)
            radius += dR
        zAngle += dZ
        if zAngle > maxZ:
            dZ = -abs(dZ)
            zAngle += dZ
        if zAngle < -maxZ:
            dZ  = abs(dZ)
            zAngle += 2*dZ
        angle += dA
        if angle > TAU:
            angle = angle - TAU
        dH += acc
        height += dH
        if height - radius < 0:
            height -= dH
            dH = initialV
        tree.clear(UPDATE = False)

def clock(duration = np.inf):
    startTime = time()
    center = None
    for pixel in tree:
        if center == None:
            center = pixel
            continue
        if     (.5*( pixel.x - tree.xMax)**2 + 5* pixel.y**2 + ( pixel.z - 0.45*tree.zMax)**2
              < .5*(center.x - tree.xMax)**2 + 5*center.y**2 + (center.z - 0.45*tree.zMax)**2):
            center = pixel
    while time() - startTime < duration:
        tree.clear(False)
        currentTime = datetime.datetime.now()
        hour = currentTime.hour % 12
        minute = currentTime.minute
        second = currentTime.second
        hourAngle = (-(hour*TAU/12 + minute*TAU/12/60 + second*TAU/12/60/60 - PI/2)) % TAU
        minuteAngle = (-(minute*TAU/60 + second*TAU/60/60 - PI/2)) % TAU
        secondAngle = (-(second*TAU/60 - PI/2)) % TAU
        m1 = min(max(-np.tan(hourAngle), -15), 15)
        m2 = min(max(-np.tan(minuteAngle), -15), 15)
        m31 = -np.tan(secondAngle)
        m3 = min(max(m31, -15), 15)
        b1 = -m1*center.y - center.z
        b2 = -m2*center.y - center.z
        b3 = -m3*center.y - center.z
        c1 = (m1**2+1)**0.5
        c2 = (m2**2+1)**0.5
        c3 = (m3**2+1)**0.5
        center.setColor(RED)
        for pixel in tree:
            if not pixel.surface or pixel.x < 0 or pixel == center: continue
            if currentTime.hour >= 12 and pixel.z > 0.85*tree.zMax:
                pixel.setColor(BLUE)
                continue
            dist = ((pixel.y - center.y)**2 + (pixel.z - center.z)**2)**0.5
            if dist > 0.9: continue
            if (dist >= .7
                and dist < .9):
                pixel.setColor(WHITE)
                continue
            if dist < 0.05:
                pixel.setColor(RED)
                continue
            angle = np.arctan((pixel.z - center.z) / (pixel.y - center.y))
            if pixel.y < center.y: angle += PI
            angle = angle % TAU
            if (abs(m1*pixel.y + pixel.z + b1) / c1 < 0.085
                and dist < .5
                and abs(angle - hourAngle) < 2):
                pixel.setColor(GREEN)
            elif (abs(m2*pixel.y + pixel.z + b2) / c2 < 0.12
                  and dist < .7
                  and abs(angle - minuteAngle) < 2):
                pixel.setColor(BLUE)
            elif (abs(m3*pixel.y + pixel.z + b3) / c3 < 0.12
                  and dist < .7
                  and abs(angle - secondAngle) < 2):
                pixel.setColor(YELLOW)
        tree.show()

# A growing and shrinking cylinder that changes the tree colors
def cylinder(colors = COLORS, duration = np.inf):
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
    while not contrast(color1, color2): color2 = Color()
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
        while not contrast(color1, newColor) or np.array_equal(color2, newColor): newColor = Color()
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
        while np.array_equal(color1, newColor) or not contrast(color2, newColor): newColor = Color()
        color1 = newColor

# Looks like a cylon's eyes
def cylon(color = RED, duration = np.inf):
    startTime = time()
    if color == None:
        color = rng.integers(0, 256, 3)
    else:
        if type(color[0]) != list:
            color = [color]
        color = rng.choice(color)
    color = np.array([130*k/np.linalg.norm(color) for k in color])
    tree.clear()
    center = 0
    deltaC = 0.1
    while time() - startTime < duration:
        center += deltaC
        if center > tree.yMax:
            deltaC = -abs(deltaC)
            center += deltaC
        if center < tree.yMin:
            deltaC = abs(deltaC)
            center += deltaC
        for pixel in tree:
            dist = abs(pixel.y - center)
            factor = max(10, -130/.3*dist + 130)/130
            c = [factor * k for k in color]
            pixel.setColor(c)
        tree.show()

# Fades in and out
def fade(colors = TRADITIONALCOLORS, midline = 1.5, divisions = 6, amplitude = 1, speed = 1.5, duration = np.inf):
    startTime = time()
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    if midline + abs(amplitude) > divisions or midline - abs(amplitude) < 0 or midline < 0:
        print("Invalid values will lead to invalid colors")
        return
    for pixel in tree:
        pixel.flag = np.array(Color()) / divisions
        pixel.setColor(pixel.flag)
    tree.show()
    while time() - startTime < duration:
        f = midline + amplitude * np.sin(speed * time())
        for pixel in tree:
            pixel.setColor(f * pixel.flag)
        tree.show()

# Courtesy of Nekisha
# Colors fall down from above
def fallingColors(colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE], duration = np.inf):
    startTime = time()
    sections = 350 # larger = slower (550 for 30 fps)
    colorDensity = 2.4 # Number of colors displayed at once
    fuzzFactor = 1 # 0 for a sharp barrier between colors.  Larger it is from there, the fuzzier the barrier becomes.  Starts glitching after 1.  
    while time() - startTime < duration:
        for z in np.linspace(tree.zMax, tree.zMax - len(colors) * tree.zRange / colorDensity, sections):
            if time() - startTime >= duration: return
            for pixel in tree:
                index = int(np.floor((pixel.z - z) / (tree.zRange / colorDensity) + fuzzFactor * rng.random()) % len(colors))
                if pixel.color == colors[(index + 1) % len(colors)]:
                    index = (index + 1) % len(colors)
                pixel.setColor(colors[index])
            tree.show()

def fire(duration = np.inf):
    startTime = time()
    one = np.array([55, 75, 0])
    two = np.array([10, 75, 0])
    twoone = two - one
    tree.clear(FLAGSONLY = True)
    def flagNeighbors(flame):
        for neighbor in flame.neighbors:
            if neighbor.z < flame.z and ((neighbor.x - flame.x)**2 + (neighbor.y - flame.y)**2)<.008:
                neighbor.flag = flame.flag - 1
                if neighbor.flag > 1: flagNeighbors(neighbor)
    while time() - startTime < duration:
        tree.fade(.2)
        if rng.random() < 2:
            flames = list(rng.choice(tree.pixels, 20))
            for i, flame in enumerate(flames):
                if flame.z > 0.75*tree.zMax or (flame.z > 0.5*tree.zMax and rng.random() < .6):
                    continue
                flame.flag = 20
                flagNeighbors(flame)
        for pixel in tree:
            if pixel.z > 0.65*tree.zMax and rng.random() < 0.1:
                pixel.setColor([5, 5, 5])
            if pixel.z < 1.1*np.cos(0.5*PI*pixel.x)*np.cos(0.5*PI*pixel.y) + 0.3:
                pixel.setColor(one + twoone * rng.random())
            if pixel.flag > 0:
                if rng.random() < 0.9:
                    pixel.setColor(RED)
                else:
                    pixel.setColor(ORANGE)
                pixel.flag -= 6
        tree.show()

# Displays the images in sequence, requires keyboard input
def imageSlideshow():
    PATH = "/home/pi/Desktop/TreeLights/Images/"
    imgList = listdir(PATH)
    for image in imgList:
        displayImage(image)
        input()
        displayImage2(image)
        print(image[:-4])
        input()
    tree.clear()

# A growing and shrinking spear that moves up and down and changes colors
def pulsatingSphere(colors = None, dR = 0.035, dH = 0.015, duration = np.inf):
    startTime = time()
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    color1 = Color()
    color2 = BLACK
    while not contrast(color1, color2): color2 = Color()
    height = 0.45 * tree.zMax + 0.1 * rng.random()
    minH = tree.zMin
    maxH = tree.zMax
    maxR = .75
    minR = 0.05
    r = 0.31
    while time() - startTime < duration:
        if r <= minR:
            dR = abs(dR)
            r += dR
            color1 = color2
            while not contrast(color1, color2): color1 = rng.choice(COLORS)
        elif r > maxR:
            dR = -abs(dR)
            r += dR
        if height - r < minH:
            dH = abs(dH)
            height = minH + r
        elif height + r > maxH:
            dH = -abs(dH)
            height = maxH - r
        for pixel in tree:
            if (pixel.x**2 + pixel.y**2 + (pixel.z - height)**2) <= r**2:
                pixel.setColor(color1)
            else:
                pixel.setColor(color2)
        tree.show()
        r += dR
        height += dH

# Radial gradient that flows outward
def radialGradient(colors = [RED, GREEN], duration = np.inf):
    startTime = time()
    if colors == None:
        colors = [rng.integers(0, 256, 3), rng.integers(0, 256, 3)]
    else:
        if type(colors[0]) != list or len(colors) != 2:
            print(colors, "Must supply exactly 2 colors for this effect")
            return
    colors[0] = np.array(colors[0])
    colors[1] = np.array(colors[1])
    radii = [pixel.r for pixel in tree]
    minR = min(radii)
    maxR = max(radii)
    deltaR = maxR - minR
    deltaP = 1/30
    while time() - startTime < duration:
        deltaP -= 1/30
        for pixel in tree:
            p = ((pixel.r - minR)/deltaR + deltaP) % 1
            if p < 0.5:
                color = colors[0] + 2*p*(colors[1] - colors[0])
            else:
                color = colors[1] + 2*(p-0.5)*(colors[0] - colors[1])
            pixel.setColor(color)
        tree.show()

# A raining effect
def rain(color = CYAN, speed = 0.35, wind = -0.2, dropCount = 8, accumulationSpeed = 0, duration = np.inf):
    startTime = time()
    width = 0.12
    height = 0.15
    floor = tree.zMin - 0.1
    newDrop = lambda floor: [rng.random()*TAU, rng.random()*(tree.zMax-floor) + tree.zMax]
    drops = [newDrop(floor) for i in range(dropCount)]
    while time() - startTime < duration:
        for i, drop in enumerate(drops):
            drop[1] -= speed
            drop[0] = (drop[0] + wind) % TAU
            if drop[1] < floor:
                del drops[i]
                drops.append(newDrop(floor))
                continue
            for pixel in tree:
                if (pixel.z < floor
                    or (pixel.surface
                        and abs(pixel.a - drop[0]) < width
                        and abs(pixel.z - drop[1]) < height)):
                    pixel.setColor(color)
        tree.show()
        tree.fade(0.7)
        floor += accumulationSpeed
        if floor >= tree.zMax: floor = 0

# Random colored planes fly through the tree, leaving trails
def randomPlanes(colors = COLORS, duration = np.inf):
    startTime = time()
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    sections = 50 # Larger = slower
    while time() - startTime < duration:
        angleZ = rng.random() * TAU
        angleX = rng.random() * PI
        newCoords = transform(tree.coordinates, xr = angleX, zr = angleZ)
        minZ = min(newCoords, key = lambda i: i[2])[2]
        maxZ = max(newCoords, key = lambda i: i[2])[2]
        zStep = (maxZ - minZ) / sections
        factor = 0.8 * rng.random() # Randomized fade speed
        tree.clear(UPDATE = False)
        color = Color()
        for z in np.linspace(minZ, maxZ + 1.5, sections):
            for i in range(len(newCoords)):
                if abs(newCoords[i][2] - z) < zStep:
                    tree[i] = color
            tree.show()
            tree.fade(factor)

# Plays the game "snake"
def snake(cycles = 99999):
    for cycle in range(cycles):
        tree.clear(UPDATE = False)
        snake = [rng.choice(tree)]
        pellet = rng.choice(tree)
        visited = [] # Prevents loops
        while True:
            if snake[0] == pellet: # Snake got the food
                snake += [snake[-1]] # Grow longer
                while pellet in snake: pellet = rng.choice(tree) # Place new food
                visited = []
            destination = None # Where will the snake go?
            for neighbor in snake[0].neighbors:
                # If the neighbor isn't part of the snake
                # And the neighbor hasn't already been visited this cycle
                # and there either isn't a destination yet
                    # or this neighbor is closer to the pellet than the current destination
                if (neighbor == pellet
                    or (neighbor not in snake
                        and neighbor not in visited
                        and (destination == None
                             or np.linalg.norm(neighbor.coordinate - pellet.coordinate) < np.linalg.norm(destination.coordinate - pellet.coordinate)))):
                    freeSpots = 0
                    for neigh in neighbor.neighbors:
                        if neigh not in snake and neigh not in visited: freeSpots += 1
                    if neighbor == pellet or freeSpots >= 1: destination = neighbor
            if destination == None: # No valid spots to move to
                break # Snake dies of starvation
            visited += [snake[0]]
            snake = [destination] + snake
            snake[-1].setColor(OFF) # Turn the tail off then remove it
            snake = snake[:-1]
            for i in range(len(snake)):
                f = i / len(snake)
                if i == 0:
                    snake[i].setColor(WHITE)
                else: # Rainbow colors
                    snake[i].setColor([max(765*(-abs(f-1/3)+1/3), 0), max(510*(abs(f-0.5) - 1/6), 0), max(765*(-abs(f-2/3)+1/3), 0)])
            pellet.setColor(WHITE)
            tree.show()
            sleep(0.05)
        for i in range(3): # Death animation
            for segment in snake:
                segment.setColor(RED)
            tree.show()
            sleep(0.5)
            for segment in snake:
                segment.setColor(OFF)
            tree.show()
            sleep(0.5)

# Rotates a plane about some axis
def spinningPlane(colors = COLORS, variant = 0, speed = 0.2, width = 0.15, height = tree.zMax / 2
                  , TWOCOLORS = False, BACKGROUND = False, SPINNER = False, duration = np.inf):
    startTime = time()
    if colors == None:
        color1, color2 = rng.integers(0, 256, 3), rng.integers(0, 256, 3)
        while not contrast(color1, color2): color2 = rng.integers(0, 256, 3)
        colors = [color1, color2]
    else:
        if type(colors[0]) != list:
            colors = [colors]
        rng.shuffle(colors)
    if SPINNER: BACKGROUND, TWOCOLORS = True, True
    colors = [colors[0], colors[-1]]
    colors += [[[0.04, 1][SPINNER] * k for k in colors[0]], [[0.04, 1][SPINNER] * k for k in colors[1]]]
    # theta gives the angle of the axis of rotation with respect to the positive x-axis
    # phi gives the angle of the axis of rotation with respect to the positive z-axis
    # Height adds directly to the z-coordinate for the axis of rotation
    if variant == 0: # Axis of rotation along x-axis
        theta = 0
        phi = PI / 2
    elif variant == 1: # Axis of rotation along y-axis
        theta = PI / 2
        phi = PI / 2
    elif variant == 2: # Axis of rotation along z-axis
        theta = 0
        phi = 0
    elif variant == 3: # Axis of rotation is random
        theta = rng.random() * TAU
        phi = rng.random() * PI
    t = 0
    while time() - startTime < duration:
        newCoords = transform(tree.coordinates, z = -height, zr = -theta, xr = t, yr = PI/2 - phi)
        for i, coord in enumerate(newCoords):
            if abs(coord[2]) < width:
                if TWOCOLORS:
                    if coord[2] >= 0:
                        tree[i].setColor(colors[0])
                    else:
                        tree[i].setColor(colors[1])
                else:
                    tree[i].setColor(colors[0])
            else:
                if BACKGROUND:
                    if TWOCOLORS:
                        if coord[2] >= 0:
                            tree[i].setColor(colors[2])
                        else:
                            tree[i].setColor(colors[3])
                    else:
                        tree[i].setColor(colors[2])
                else:
                    tree[i].setColor(OFF)
        tree.show()
        t += speed

# Makes spirals
def spirals(colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
             , variant = 1, spinCount = 2, zSpeed = 1, spinSpeed = -2, SURFACE = False
             , SKIPBLACK = True, GENERATEINSTANTLY = False, GENERATETOGETHER = False, ENDAFTERSPIRALS = False
             , PRECLEAR = True, POSTCLEAR = False, SPINAFTERDONE = False
             , duration = np.inf, cycles = 1):
    startTime = time()
    if variant**2 != 1: # variant determines which way the spirals slope.  1 = positive slope, -1 = negative slope
        print("variant must be 1 or -1")
        return
    DONE = GENERATEINSTANTLY
    spiralCount = len(colors) # Number of spirals
    sectionH = tree.zRange / spinCount # Works in sections of one spin each to make things simpler
    dTheta = -TAU / spiralCount # theta gives the initial angle for the current spiral, dTheta is the angle difference between each spiral
    totalAngle = TAU * spiralCount # Total angle drawn by each spiral
    spiralH = sectionH / spiralCount # Vertical height of each spiral
    spiralDistBetweenTops = spiralCount * spiralH # Vertical distance between top of the same spiral at corresponding points 2π radians apart
    spiral, cycle, angleOffset, z = 0, 0, 0, 0
    while colors[spiral] == OFF: spiral += 1
    # Precomputing some values becaues this function sometimes gets laggy
    m1 = sectionH / TAU
    m2 = -TAU / sectionH
    m2sp1 = m2**2 + 1
    # Gives the height of the top of the spiral being worked on, with respect to angle in the tree
    spiralTop      = lambda angle, z: m1*angle + sectionH*(z // sectionH)
    # Gives the height of the spiral front with respect to the angle in the tree - to make leading edge neater
    spiralTerminus = lambda angle, z: m2*angle + m2sp1*z
    loopStart = time()
    while time() - startTime < duration:
        loopStart = time()
        if PRECLEAR or spinSpeed != 0: tree.clear(UPDATE = False)
        for pixel in tree: # Sets correct color for each pixels
            angle = (pixel.a + angleOffset) % TAU
            m = int(((pixel.z % sectionH - variant * angle * sectionH / TAU) // spiralH) % spiralCount)
            if SKIPBLACK and colors[m] == BLACK: continue
            if ((GENERATEINSTANTLY or DONE or m < spiral) # Safe to draw this spiral in full
                and not (GENERATETOGETHER and not DONE) # Above condition is wrong if GENERATETOGETHER and not DONE
                and (not SURFACE or pixel.surface)): # Avoid setting interior pixels if SURFACE
                pixel.setColor(colors[m])
            else:
                pixel.flag = m
        if not GENERATEINSTANTLY and not DONE:
            for pixel in tree:
                for spi in range(*[[spiral, spiral + 1], [spiralCount]][GENERATETOGETHER]):
                    if SKIPBLACK and colors[spi] == OFF: continue
                    angle = (variant * (pixel.a + angleOffset - variant * (spi+1)*dTheta)) % TAU
                    topOfSpiral = spiralTop(angle, pixel.z)
                    angle += TAU * (((pixel.z - m1*angle) // sectionH) + 1)
                    spiralEdge = spiralTerminus(angle, z)
                    if (pixel.z < spiralEdge
                        and ((pixel.z <= topOfSpiral
                              and pixel.z > topOfSpiral - spiralH)
                             or (pixel.z <= topOfSpiral + spiralDistBetweenTops
                                 and pixel.z > topOfSpiral + spiralDistBetweenTops - spiralH))
                        and (not SURFACE or pixel.surface)):
                        pixel.setColor(colors[pixel.flag])
        tree.show()
        if (not SPINAFTERDONE or DONE): angleOffset = (angleOffset + spinSpeed * (time() - loopStart)) % TAU
        if GENERATEINSTANTLY or DONE: continue
        if z < tree.zRange: z += zSpeed * (time() - loopStart) # Mid-stripe, increase z and continue
        else: # Stripe is complete
            z = 0 # Reset z
            if spiral < spiralCount: # If we aren't done
                spiral += 1 # Then move on to the next stripe
                while spiral < spiralCount and SKIPBLACK and colors[spiral] == OFF: # Option to skip black because it just keeps the pixels off
                    if spiral < spiralCount - 1: # Keep skipping as long as they're black
                        spiral += 1
                    else:
                        spiral += 1
                        break # Rest of spirals were black - jumps into below if statement to complete the cycle
            if spiral >= spiralCount or GENERATETOGETHER: # Not an else statement because above while loop can trigger this code too
                cycle += 1 # Otherwise start the next cycle
                if cycle >= cycles: # Unless that was the last cycle
                    DONE = True # In which case we're done drawing spirals and just spin
                    if ENDAFTERSPIRALS:
                        if POSTCLEAR: tree.clear(UPDATE = False)
                        return # Or done entirely if that flag was set
                else:
                    spiral = 0 # If that wasn't the last cycle, start the drawing process over

# Has a circle wander around the tree
def spotlight(colors = [WHITE, BLUE], duration = np.inf):
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
    radiusS = radius**2
    z = tree.zMax * rng.random() * 0.6 # Spotlight's z-coordinate
    dz = .2 * rng.random()
    theta = TAU * rng.random() # Spotlight's angle around z-axis
    dTheta = .2 * rng.random()
    # m and b used to calculate point on tree's surface from z and theta
    m = tree.xMax / (tree[tree.sortedX[-1]].z - tree[tree.sortedZ[-1]].z)
    b = -m * tree[tree.sortedZ[-2]].z
    while time() - startTime < duration:
        z += dz
        theta += dTheta
        if z + radius > tree.zMax:dz = -abs(dz)
        if z - radius < 0: dz = abs(dz)
        point = [(m*z+b)*np.cos(theta), (m*z+b)*np.sin(theta)] + [z] # On or near surface of tree
        for pixel in tree:
            if pixel.surface and (pixel.x - point[0])**2 + (pixel.y - point[1])**2 + (pixel.z - point[2])**2 < radiusS:
                pixel.setColor(color1)
            else:
                pixel.setColor(color2)
        tree.show()
        dz = min(.1, max(-.1, dz + .06*rng.random() - 0.03))
        dTheta = min(.1, max(-.1, dTheta + .06*rng.random() - 0.03))

# Sweeps colors around the tree
def sweep(colors = COLORS, sections = 30, CLOCKWISE = False, ALTERNATE = True, duration = np.inf):
    startTime = time()
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    pixelsPerSection = tree.LED_COUNT // sections + 1
    color = Color()
    newColor = Color()
    a = [1, -1][CLOCKWISE]
    section = 0
    while time() - startTime < duration:
        for i in range(a*section*pixelsPerSection, a*(section+1)*pixelsPerSection, a):
            if i > tree.LED_COUNT - 1 or i < -tree.LED_COUNT: break
            tree[tree.sortedA[i]].setColor(color)
        tree.show()
        section += 1
        if section >= sections:
            section = 0
            if ALTERNATE: a *= -1
            while not contrast(newColor, color): newColor = Color()
            color = newColor
            sleep(1)

# Sets all LEDs randomly then lets their brightness vary
def twinkle(colors = TRADITIONALCOLORS, intensity = 0, duration = np.inf):
    startTime = time()
    setAllRandom(colors)
    tree.clear(FLAGSONLY = True)
    while time() - startTime < duration:
        for pixel in tree:
            if pixel.flag == 0 and rng.random() < 0.03:
                pixel.flag = 5
            if pixel.flag > 0:
                if pixel.flag >= 3:
                    f = (9 - intensity + pixel.flag)/(12 - intensity)
                else:
                    f = (12 - intensity)/(15 - intensity - pixel.flag)
                pixel.setColor([min(255, max(0, k*f)) for k in pixel.color])
                pixel.flag -= 1
        tree.show()

# Sets all LEDs at random then lets their colors gradually change
def wander(colors = None, slowness = 15, duration = np.inf):
    startTime = time()
    if colors == None:
        Color = lambda: rng.integers(0, 128, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    tree.clear(FLAGSONLY = True)
    while time() - startTime < duration:
        for pixel in tree:
            if pixel.flag == 0:
                newColor = Color()
                diff = (newColor - pixel.color) / slowness
                pixel.flag = [diff, slowness]
            if pixel.flag != 0:
                pixel.setColor(pixel.color + pixel.flag[0])
                pixel.flag[1] -= 1
                if pixel.flag[1] <= 0:
                    pixel.flag = 0
        tree.show()

# Spirals out from the tree's z-axis, in rainbow colors
def zSpiral(twists = 8, duration = np.inf, cycles = 99999):
    startTime = time()
    sections = 100
    totalAngle = TAU * twists
    dA = totalAngle / sections
    dR = tree[tree.sortedR[-1]].r - tree[tree.sortedR[0]].r
    minR = tree[tree.sortedR[0]].r
    Color = lambda i: [255 * max(min(-3*abs(i/sections - 1/3) + 1.0, 1), 0),
                       255 * max(min( 3*abs(i/sections - 0.5) - 0.5, 1), 0),
                       255 * max(min(-3*abs(i/sections - 2/3) + 1.0, 1), 0)]
    for cycle in range(cycles):
        tree.clear(UPDATE = False)
        angle = dA
        for i in range(1 + sections + sections // twists):
            color = Color(i - sections // 10)
            for pixel in tree:
                if (pixel.a - (angle % TAU)) % TAU <= dA:
                    if pixel.color == OFF and pixel.r < minR + dR*angle/totalAngle:
                        pixel.setColor(color)
            tree.show()
            angle += dA
            tree.show()