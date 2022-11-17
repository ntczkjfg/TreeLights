from Common_Variables import rng, tree
from StaticEffects import *
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
# Look like a traffic cone, wizard hat
# Quicker rain from cloud
# Falling leaves
# Jack-o-lantern?

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
    maxZ = np.pi/3
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
                tree[i].setColor(colors[4 * points[i][2] // radius + 4])
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
        if angle > np.tau:
            angle = angle - np.tau
        dH += acc
        height += dH
        if height - radius < 0:
            height -= dH
            dH = initialV
        tree.clear(UPDATE = False)

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
def cylon(color = RED, duration = np.inf):
    startTime = time()
    if color == None:
        color = rng.integers(0, 256, 3)
    else:
        if type(color[0]) != list:
            color = [color]
        color = rng.choice(color)
    color = np.array(color)/np.linalg.norm(color)*130
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
            c = factor * color
            pixel.setColor(c)
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
            for pixel in tree:
                index = int(np.floor((pixel.z - z) / (tree.zRange / colorDensity) + fuzzFactor * rng.random()) % len(colors))
                if pixel.color == colors[(index + 1) % len(colors)]:
                    index = (index + 1) % len(colors)
                pixel.setColor(colors[index])
            tree.show()

def fire(duration = np.inf):
    startTime = time()
    one = np.array([75, 75, 0])
    two = np.array([20, 75, 0])
    twoone = two - one
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
            if pixel.z < 1.1*np.cos(0.5*np.pi*pixel.x)*np.cos(0.5*np.pi*pixel.y) + 0.3:
                pixel.setColor(one + twoone * rng.random())
            if pixel.flag > 0:
                pixel.setColor(RED)
                pixel.flag -= 6
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

# A growing and shrinking spear that moves up and down and changes colors
def pulsatingSphere(colors = None, duration = np.inf):
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
    height = tree.zMax*0.45
    minH = tree.zMin
    maxH = tree.zMax
    deltaH = 0.015
    maxR = .75
    minR = 0.05
    r = 0.31
    deltaR = 0.03
    while time() - startTime < duration:
        if r <= minR:
            deltaR = abs(deltaR)
            r += deltaR
            color1 = color2
            while np.array_equal(color1, color2): color1 = rng.choice(COLORS)
        elif r > maxR:
            deltaR = -abs(deltaR)
            r += deltaR
        if height - r < minH:
            deltaH = abs(deltaH)
            height += deltaH
        elif height + r > maxH:
            deltaH = -abs(deltaH)
            height += deltaH
        for pixel in tree:
            if (pixel.x**2 + pixel.y**2 + (pixel.z-height)**2)**0.5 <= r:
                pixel.setColor(color1)
            else:
                pixel.setColor(color2)
        tree.show()
        r += deltaR
        height += deltaH

# Radial gradient that flows outward
def radialGradient(colors = [RED, GREEN], duration = np.inf):
    startTime = time()
    if colors == None:
        colors = [rng.integers(0, 256, 3), rng.integers(0, 256, 3)]
    else:
        if type(colors[0]) != list or len(colors) != 2:
            print("Must supply exactly 2 colors for this effect")
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
def rain(color = CYAN, duration = np.inf):
    startTime = time()
    dropCount = 8
    radius = 0.08
    fallSpeed = 0.15
    newDrop = lambda: [rng.random()*np.tau, rng.random()*tree.zMax + tree.zMax]
    drops = [newDrop() for i in range(dropCount)]
    while time() - startTime < duration:
        for i, drop in enumerate(drops):
            drop[1] -= fallSpeed
            if drop[1] < tree.zMin:
                del drops[i]
                drops.append(newDrop())
                continue
            for pixel in tree:
                if pixel.surface and abs(pixel.a - drop[0]) < 0.1 and abs(pixel.z - drop[1]) < radius:
                    pixel.setColor(color)
        tree.show()
        tree.fade(0.75)
#rain()

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
        angleZ = rng.random() *np.tau
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
def seizure(duration = np.inf):
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
    for cycle in range(cycles):
        tree.clear(False)
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
                if (neighbor not in snake
                    and neighbor not in visited
                    and (destination == None
                         or np.linalg.norm(neighbor.coordinate - pellet.coordinate) < np.linalg.norm(destination.coordinate - pellet.coordinate))):
                    destination = neighbor
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

# Rotates a plane through the viewing axis
def spinningPlane(colors = COLORS, variant = 0, speed = 0.2, width = 0.15, height = tree.zMax / 2
                  , TWOCOLORS = False, BACKGROUND = False, SPINNER = False, duration = np.inf):
    startTime = time()
    if colors == None:
        colors = [rng.integers(0, 256, 3), rng.integers(0, 256, 3)]
    else:
        if type(colors[0]) != list:
            colors = [colors]
        rng.shuffle(colors)
    if SPINNER: BACKGROUND, TWOCOLORS = True, True
    colors = [colors[0], colors[-1]]
    colors += [list([0.04, 1][SPINNER] * np.array(colors[0])), list([0.04, 1][SPINNER] * np.array(colors[1]))]
    # theta gives the angle of the axis of rotation with respect to the positive x-axis
    # phi gives the angle of the axis of rotation with respect to the positive z-axis
    # Height adds directly to the z-coordinate for the axis of rotation
    if variant == 0: # Axis of rotation along x-axis
        theta = 0
        phi = np.pi / 2
    elif variant == 1: # Axis of rotation along y-axis
        theta = np.pi / 2
        phi = np.pi / 2
    elif variant == 2: # Axis of rotation along z-axis
        theta = 0
        phi = 0
    elif variant == 3: # Axis of rotation is random
        theta = rng.random() * np.tau
        phi = rng.random() * np.pi
    t = 0
    while time() - startTime < duration:
        newCoords = transform(tree.coordinates, z = -height, zr = -theta, xr = t, yr = np.pi/2 - phi)
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

def spirals(colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
             , variant = 1, spinCount = 2, sections = 30, spinSpeed = -.1, surface = False
             , SKIPBLACK = True, GENERATEINSTANTLY = False, GENERATETOGETHER = False, ENDAFTERSPIRALS = False
             , PRECLEAR = True, POSTCLEAR = False, ONLYSPINAFTERDONE = False
             , duration = np.inf, cycles = 1):
    startTime = time()
    if variant**2 != 1: # variant determines which way the spirals slope.  1 = positive slope, -1 = negative slope
        print("variant must be 1 or -1")
        return
    DONE = GENERATEINSTANTLY
    spiralCount = len(colors) # Number of spirals
    sectionH = tree.zRange / spinCount # Works in sections of one spin each to make things simpler
    dTheta = -np.tau / spiralCount # theta gives the initial angle for the current spiral, dTheta is the angle difference between each spiral
    totalAngle = np.tau * spiralCount # Total angle drawn by each spiral
    spiralH = sectionH / spiralCount # Vertical height of each spiral
    spiralDistBetweenTops = spiralCount * spiralH # Vertical distance between top of the same spiral at corresponding points 2π radians apart
    dz = tree.zRange / sections
    spiral, cycle, angleOffset, z = 0, 0, 0, dz
    while colors[spiral] == OFF: spiral += 1
    # Gives the height of the top of the spiral being worked on, with respect to angle in the tree
    spiralTop = lambda angle, z: angle * sectionH / np.tau + sectionH * (z // sectionH)
    spiralTerminus =  lambda angle, z: z - (np.tau / sectionH) * (angle - np.tau * z / sectionH)
    def getAngle(angle, z):
        while angle < np.tau * (spinCount + 1):
            if z < angle * sectionH / np.tau and z > angle * sectionH / np.tau - spiralH:
                return angle
            angle += np.tau
        return angle % np.tau
    while time() - startTime < duration:
        if PRECLEAR or spinSpeed != 0: tree.clear(False)
        for pixel in tree: # Sets correct color for each pixel
            angle = (pixel.a + angleOffset) % np.tau
            zModH = pixel.z % sectionH
            m = int(((zModH - variant * angle * sectionH / np.tau) // spiralH) % spiralCount)
            if (GENERATEINSTANTLY or DONE or m < spiral) and not (GENERATETOGETHER and not DONE) and (not surface or pixel.surface):
                if SKIPBLACK and colors[m] != OFF: pixel.setColor(colors[m])
            else:
                pixel.flag = m
        if not GENERATEINSTANTLY and not DONE:
            for pixel in tree:
                for spi in range(*[[spiral, spiral + 1], [0, spiralCount]][GENERATETOGETHER]):
                    if SKIPBLACK and colors[spi] == OFF: continue
                    topOfSpiral = spiralTop((pixel.a + angleOffset - (spi+1)*dTheta) % np.tau, pixel.z)
                    spiralEdge = spiralTerminus(getAngle((pixel.a + angleOffset - (spi+1)*dTheta) % np.tau, pixel.z), z)
                    if (pixel.z < spiralEdge
                        and ((pixel.z <= topOfSpiral
                              and pixel.z > topOfSpiral - spiralH)
                             or (pixel.z <= topOfSpiral + spiralDistBetweenTops
                                 and pixel.z > topOfSpiral + spiralDistBetweenTops - spiralH))
                        and (not surface or pixel.surface)):
                        pixel.setColor(colors[pixel.flag])
        tree.show()
        if (not ONLYSPINAFTERDONE or DONE): angleOffset = (angleOffset + spinSpeed) % np.tau
        if z < tree.zRange: # Mid-stripe, increase z and continue
            z += dz
        else: # Stripe is complete
            z = dz # Reset z
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
                        if POSTCLEAR: tree.clear(False)
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
    radius *= radius
    z = tree.zMax * rng.random() * 0.8# Spotlight's z-coordinate
    dz = .2 * rng.random()
    theta = np.tau * rng.random() # Spotlight's angle around z-axis
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
def stripedFill(duration = np.inf):
    startTime = time()
    numberOfStripes = 3
    angleDiff = np.tau / numberOfStripes
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

# Sweeps colors around the tree
def sweep(colors = COLORS, duration = np.inf):
    startTime = time()
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    sections = 30
    color = Color()
    newColor = Color()
    while time() - startTime < duration:
        while np.array_equal(newColor, color): newColor = Color()
        for i in range(sections + 1):
            for pixel in tree:
                if pixel.a < np.tau*i/sections:
                    pixel.setColor(newColor)
            tree.show()
        color = newColor
        sleep(1)

# Sets all LEDs randomly then lets their brightness vary
def twinkle(variant = 0, color = [50, 50, 50], intensity = 0, duration = np.inf):
    startTime = time()
    if variant == 0:
        setAll(color)
    elif variant == 1:
        setAllRandom(TREECOLORS)
    else:
        setAllRandom(COLORS)
    if variant != 0:
        for pixel in tree:
            pixel.setColor(np.array(pixel.color)/2)
    while time() - startTime < duration:
        for pixel in tree:
            if pixel.flag == 0 and rng.random() < 0.03:
                pixel.flag = 5
            if pixel.flag > 0:
                if pixel.flag >= 3:
                    f = (9 - intensity + pixel.flag)/(12 - intensity)
                else:
                    f = (12 - intensity)/(15 - intensity - pixel.flag)
                c = np.array(pixel.color) * f
                c[0] = min(255, max(0, c[0]))
                c[1] = min(255, max(0, c[1]))
                c[2] = min(255, max(0, c[2]))
                pixel.setColor(c)
                pixel.flag -= 1
        tree.show()

# Sets all LEDs at random then lets their colors gradually change
def wander(colors = None, duration = np.inf):
    startTime = time()
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
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
            pixel.setColor([max(0, min(255, pixel.color[0] + rng.integers(-wander, wander + 1))),
                            max(0, min(255, pixel.color[1] + rng.integers(-wander, wander + 1))),
                            max(0, min(255, pixel.color[2] + rng.integers(-wander, wander + 1)))])
        tree.show()

# Spirals out from the tree's z-axis, in rainbow colors
def zSpiral(twists = 4, cycles = 99999):
    sections = 100
    deltaA = np.tau * twists / sections
    # To find minimum and maximum radius
    radii = [pixel.r for pixel in tree]
    deltaR = (max(radii)-min(radii))/sections
    Color = lambda i: [255 * max(-3*abs(i/sections - 1/3) + 1.0, 0),
                       255 * max( 3*abs(i/sections - 0.5) - 0.5, 0),
                       255 * max(-3*abs(i/sections - 2/3) + 1.0, 0)]
    for cycle in range(cycles):
        tree.clear(False)
        angle = 0
        r = min(radii)
        for i in range(sections):
            color = Color(i)
            for pixel in tree:
                if (pixel.a - angle) % np.tau <= deltaA:
                    if pixel.r < r + deltaR and pixel.r > r - deltaR * (np.tau / deltaA):
                        pixel.setColor(color)
            tree.show()
            angle = (angle + deltaA) % np.tau
            r += deltaR
            tree.show()
        for angle in np.linspace(0, np.tau, sections//twists):
            for pixel in tree:
                if pixel.color == OFF and pixel.a <= angle:
                    pixel.setColor(RED)
            tree.show()