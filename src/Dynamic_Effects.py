from time import sleep, time
from pathlib import Path
import datetime

import numpy as np

from Common_Variables import rng, tree, PI, TAU
from Colors import *
from Simple_Effects import *
from Helper_Functions import *
from Testing_Functions import *
from Effect_Control import *

# Vague ideas, not necessarily todo list
# Upgrade zSpiral to support arbitrary colors like gradient(), plus option to
# draw spirals instantly - so it can be used to crate any shimmering radial cycle
# Alternate: Helper function to build sorted angles in a spiral, using code from zSpiral
# to be fed to gradient function through indices argument
# Smarter accumulating snow that doesn't fake it as much:  Picks snow path by working
# backwards from empty LEDs near tree bottom, filling it and neighbors as it falls
# Random stripes
# Expanding shapes from center
# Expanding / contracting stripes at random angles
# Letters
# Small number of points moving around with fading trails
# Digital Clock
# Breakout
# Look like a wizard hat
# Falling leaves
# Jack-o-lantern?

# Rotates the tree while running alternatingly colored vertical stripes alternatingly up and down
def alternatingStripes(backgroundC = [0, 10, 90], stripe1C = [5, 90, 5], stripe2C = [70, 15, 15],
                       stripeSpeed = 3, spinSpeed = PI, stripeCount = 2, duration = np.inf):
    startTime = time()
    lastTime = startTime
    # numberOfStripes is per stripe, so double for actual number
    stripeWidth = TAU / (2*stripeCount) # Stripe angular width
    # Current rotation in radians
    angle = 0
    # Height of stripe1
    height = 0
    # Used below, needs to be defined before loop is run
    # Helps create transition effect
    prevStripes = np.arange(tree.n)
    # Used to let the stripes go a set amount off-tree
    # To give some pause where no stripes are visible
    extra = 0.1*tree.zMax
    for pixel in tree:
        pixel.flag = np.array(pixel.color)
    maintainBackground = True
    stripe1C = np.array(stripe1C)
    stripe2C = np.array(stripe2C)
    backgroundC = np.array(backgroundC)
    while time() - startTime < duration:
        dt = time() - lastTime
        lastTime = time()
        height += stripeSpeed * dt
        if maintainBackground and height >= tree.zMax:
            maintainBackground = False
        if height > 2*tree.zMax + extra:
            stripeSpeed = -abs(stripeSpeed)
        elif height < tree.zMin - extra:
            stripeSpeed = abs(stripeSpeed)
        angle += (spinSpeed * dt) % TAU
        stripe1 = ((((tree.a - angle) // stripeWidth) % 2 == 0)
                   & (tree.z < height)
                   & (tree.z > height - tree.zRange))
        stripe2 = ((((tree.a - angle) // stripeWidth) % 2 == 1)
                   & (tree.z < 2*tree.zRange - height)
                   & (tree.z > tree.zRange - height))
        stripe1 = np.where(stripe1)[0]
        stripe2 = np.where(stripe2)[0]
        # Background is handled like this intentionally to create a natural transition effect
        # Only pixels which were previously part of a stripe become part of the background
        # Lets the stripes swipe away previous effect, instead of having it become all background right away
        background = np.setdiff1d(np.setdiff1d(prevStripes, stripe1), stripe2)
        prevStripes = np.union1d(stripe1, stripe2)
        if maintainBackground:
            for i in background:
                tree[i].setColor(tree[i].flag)
        else:
            for i in background:
                tree[i].setColor(backgroundC)
        for i in stripe1:
            tree[i].setColor(stripe1C)
        for i in stripe2:
            tree[i].setColor(stripe2C)
        tree.show()

# Blinks lights on and off
def blink(colors = TRADITIONALCOLORS, groupCount = 7, p = 0.7, delay = 1, duration = np.inf):
    startTime = time()
    lastTime = startTime
    tree.clear(UPDATE = False)
    set_all_random(colors)
    for pixel in tree:
        pixel.flag = np.array(pixel.color)
    groups = rng.integers(0, groupCount, tree.n)
    oldGroups = np.array([True for i in range(groupCount)])
    dt = 0
    while time() - startTime < duration:
        dt += time() - lastTime
        lastTime = time()
        if dt < delay:
            sleep(.01)
            continue
        else:
            dt = 0
        newGroups = np.array([True if rng.random() < p else False for i in range(groupCount)])
        turnOn = np.where((newGroups > oldGroups)[groups])[0]
        turnOff = np.where((newGroups < oldGroups)[groups])[0]
        oldGroups = newGroups
        for i in turnOn:
            tree[i].setColor(tree[i].flag)
        for i in turnOff:
            tree[i].setColor(OFF)
        tree.show()

# Courtesy of Arby
# A bouncing rainbow ball that changes size and wobbles
def bouncingRainbowBall(duration = np.inf):
    startTime = time()
    lastTime = startTime
    radius = .7
    dR = 0.15
    minR = 0.5
    maxR = .75
    zAngle = 0
    dZ = 0.45
    maxZ = PI/3
    angle = 0
    dA = 1.5
    colors = np.array([RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK])
    height = radius
    acceleration = -2.5
    initialV = 3.15
    dH = initialV
    while (t := time()) - startTime < duration:
        dt = t - lastTime
        lastTime = t
        points = transform(tree.coordinates[:,0:3], z = -height, yr = -zAngle, zr = -angle)
        ball = np.where(points[:,0]**2 + points[:,1]**2 + points[:,2]**2 <= radius**2)[0]
        indices = (4*points[:,2] / radius + 4).astype(np.uint8)[ball]
        ballColors = colors[indices]
        for i, j in enumerate(ball):
            tree[j].setColor(ballColors[i])
        radius += dR*dt
        if radius >= maxR:
            dR = -abs(dR)
            radius = maxR
        if radius <= minR:
            dR = abs(dR)
            radius = minR
        zAngle += dZ*dt
        if zAngle > maxZ:
            dZ = -abs(dZ)
            zAngle = maxZ
        if zAngle < -maxZ:
            dZ  = abs(dZ)
            zAngle = -maxZ
        angle = (angle + dA*dt) % TAU
        dH += acceleration*dt
        height += dH*dt
        if height - radius < 0:
            height = radius
            dH = initialV
        tree.show()
        tree.clear(UPDATE = False)

# Displays an analogue clock
def clock(duration = np.inf):
    startTime = time()
    # Aim to put center of clock here, at y = 0, with a large x-value
    centerZ = tree.zMin + 0.35*tree.zRange
    # All coordinates, with index appended on
    coords = np.hstack((tree.coordinates[:,0:3], np.reshape(np.arange(tree.n), (-1, 1))))
    # Sort by z distance from centerZ, keep closest 5%
    coords[:,2] = abs(coords[:,2] - centerZ)
    sortOrder = np.argsort(coords[:,2])
    coords = coords[sortOrder][:int(.05*len(coords))]
    # Side quest:  Find good radius
    sortOrder = np.argsort(-abs(coords[:,1]))
    coords = coords[sortOrder]
    radius = round(4/3*abs(tree[int(coords[5][3])].y), 2)
    # Sort by y distance from 0, keep closest 10
    coords[:,1] = abs(coords[:,1])
    sortOrder = np.argsort(coords[:,1])
    coords = coords[sortOrder][:10]
    # Sort by largest x-value, take largest 3
    sortOrder = np.argsort(-coords[:,0])
    coords = coords[sortOrder][:3]
    # Sort by y distance from 0 again, pick the best one
    sortOrder = np.argsort(coords[:,1])
    center = tree[int(coords[sortOrder][0][3])]
    # Calculate distances and angles from center
    dists = ((tree.y-center.y)**2 + (tree.z-center.z)**2)**0.5
    angles = np.arctan((tree.z - center.z) / (tree.y - center.y + .00001))
    angles[tree.y < center.y] += PI
    angles = angles % TAU
    oldColors = np.array([BLACK for i in range(tree.n)])
    tree.clear(UPDATE = False)
    while time() - startTime < duration:
        newColors = np.array([BLACK for i in range(tree.n)])
        currentTime = datetime.datetime.now()
        hour = currentTime.hour % 12
        minute = currentTime.minute
        second = currentTime.second
        hourAngle = (-(hour*TAU/12 + minute*TAU/12/60 + second*TAU/12/60/60 - PI/2)) % TAU
        minuteAngle = (-(minute*TAU/60 + second*TAU/60/60 - PI/2)) % TAU
        secondAngle = (-(second*TAU/60 - PI/2)) % TAU
        mH = min(max(-np.tan(hourAngle), -15), 15)
        mM = min(max(-np.tan(minuteAngle), -15), 15)
        mS = min(max(-np.tan(secondAngle), -15), 15)
        bH = -mH*center.y - center.z
        bM = -mM*center.y - center.z
        bS = -mS*center.y - center.z
        cH = (mH**2+1)**0.5
        cM = (mM**2+1)**0.5
        cS = (mS**2+1)**0.5
        if currentTime.hour >= 12:
            newColors[tree.z > 0.85*tree.zMax] = BLUE
        frame = abs(dists - radius) < 0.1
        middle = dists < 0.05
        hourHand = ((abs(mH*tree.y + tree.z + bH) / cH < 0.085)
                    & (dists < 0.6)
                    & (abs(angles - hourAngle) < 2))
        minuteHand = ((abs(mM*tree.y + tree.z + bM) / cM < 0.12)
                      & (dists < 0.7)
                      & (abs(angles - minuteAngle) < 2))
        secondHand = ((abs(mS*tree.y + tree.z + bS) / cS < 0.12)
                      & (dists < 0.7)
                      & (abs(angles - secondAngle) < 2))
        newColors[secondHand] = YELLOW
        newColors[minuteHand] = GREEN
        newColors[hourHand] = BLUE
        newColors[frame] = WHITE
        newColors[middle] = RED
        different = np.where(newColors != oldColors)[0]
        for i in different:
            tree[i].setColor(newColors[i])
        oldColors = newColors
        tree.show()

# Cylinders that grow tall then wide, then shrink
def cylinder(colors = COLORS, duration = np.inf):
    startTime = time()
    lastTime = startTime
    if colors is None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != np.ndarray or len(colors) < 3:
            print("Must supply at least 3 colors for this effect")
            return
        Color = lambda: rng.choice(colors)
    def newColor(c1, c2):
        newColor = Color()
        while np.array_equal(c1, newColor) or not contrast(c2, newColor): newColor = Color()
        return newColor
    color1 = Color()
    color2 = Color()
    while not contrast(color1, color2): color2 = Color()
    midZ = tree.zRange / 2 + tree.zMin
    maxH = tree.zRange / 2
    maxR = 2**0.5
    minR = maxR / 4
    r = minR
    h = 0
    dH = 2
    dR = 1.25
    # Adds some pause between the transitions
    extra = .1
    minH = 0 - extra*dH
    maxH += 3*extra*dH
    maxR += extra*dR
    vertical = True
    # Used below, needs to be initialized here
    oldCylinder = np.array([])
    while time() - startTime < duration:
        dt = time() - lastTime
        lastTime = time()
        if vertical: # H is growing or shrinking
            h += dt*dH
            if h < minH:
                dH = abs(dH)
                color1 = newColor(color1, color2)
            elif h > maxH:
                dH = -abs(dH)
                vertical = False
        else: # R is growing or shrinking
            r += dt*dR
            if r < minR:
                r = minR
                dR = abs(dR)
                vertical = True
            elif r > maxR:
                dR = -abs(dR)
                color2 = newColor(color2, color1)
        cylinder = ((tree.r <= r)
                    & (abs(tree.z - midZ) <= h))
        cylinder = np.where(cylinder)[0]
        # newCylinder is an optimization, adds about 6 fps
        newCylinder = np.setdiff1d(cylinder, oldCylinder)
        background = np.setdiff1d(oldCylinder, cylinder)
        for i in newCylinder:
            tree[i].setColor(color1)
        for i in background:
            tree[i].setColor(color2)
        oldCylinder = cylinder
        tree.show()

# Looks like a cylon's eyes
def cylon(color = RED, duration = np.inf):
    startTime = time()
    lastTime = startTime
    Color = color_builder(color)
    color = Color()
    color = np.array([[130*k/np.linalg.norm(color) for k in color]])
    tree.clear()
    center = 0
    deltaC = 1.7
    while time() - startTime < duration:
        dt = time() - lastTime
        lastTime = time()
        center += deltaC*dt
        if center > tree.yMax:
            deltaC = -abs(deltaC)
            center += deltaC*dt
        if center < tree.yMin:
            deltaC = abs(deltaC)
            center += deltaC*dt
        dists = np.abs(tree.y - center)
        factors = np.maximum(1/13, -dists/.3 + 1)
        colors = factors.reshape(tree.n, 1) * color
        for i, pixel in enumerate(tree):
            pixel.setColor(colors[i])
        tree.show()

# Fades in and out
def fade(colors = TRADITIONALCOLORS, midline = .7, amplitude = .7, speed = 1.5, duration = np.inf):
    # midline and amplitude define a sine function determining brightness as the light fades
    # It will reject a sine with a minimum below 0 or maximum above 1
    startTime = time()
    Color = color_builder(colors)
    amplitude = abs(amplitude)
    if midline < 0 or midline > 1 or amplitude > midline:
        print("Midline must be between 0 and 1, amplitude cannot be larger than midline")
        return
    pre_fade_buffer = np.concatenate([Color() for _ in range(tree.n)])
    while time() - startTime < duration:
        # f is factor, varies sinuosidally
        f = max(0, min(1, midline + amplitude * np.sin(speed * time())))
        if f <= 0.003:
            pre_fade_buffer = np.concatenate([Color() for _ in range(tree.n)])
        tree.setColors(pre_fade_buffer*f)
        tree.show()

# Randomly restores lights to full brightness while constantly fading
def fadeRestore(colors = TRADITIONALCOLORS, p = 0.95, halflife = 0.3, duration = np.inf):
    startTime = time()
    lastTime = startTime
    Color = color_builder(colors)
    color_buffer = np.array([Color() for _ in range(tree.n)])
    while (t := time()) - startTime < duration:
        dt = t - lastTime
        lastTime = t
        # p is probability of each light restoring per second
        # exp adjusts this to work with dt seconds
        exp = (1-p)**dt
        tree.fade(halflife = halflife, dt = dt)
        renew = np.where(rng.random(tree.n) >= exp)[0]
        for i in renew:
            tree[i].setColor(color_buffer[i])
        tree.show()

# Courtesy of Nekisha
# Colors fall down from above
def fallingColors(colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE], duration = np.inf):
    startTime = time()
    lastTime = startTime
    colors = np.array(colors)
    colorDensity = 2.4 # Number of colors displayed at once
    # height of all colors stacked together
    height = len(colors)/colorDensity*tree.zRange
    # moving height that pixels are colord with respect to
    h = tree.zMax
    fallSpeed = .35 # units/second
    fuzzFactor = .25 # 0 for a sharp barrier between colors.  Larger it is from there, the fuzzier the barrier becomes.  Starts glitching after 1.
    fuzzedZ = tree.z + fuzzFactor * np.random.uniform(-1, 1, tree.n)
    while time() - startTime < duration:
        dt = time() - lastTime
        lastTime = time()
        h -= fallSpeed * dt
        indices = (len(colors)*((fuzzedZ - h) % height)/height).astype(np.int32)
        tree.setColors(colors[indices].flatten())
        tree.show()

# Meant to imitate a fire
def fire(duration = np.inf):
    startTime = time()
    lastTime = startTime
    one = np.array([75, 55, 0])
    two = np.array([75, 10, 0])
    twoone = two - one
    tree.flags = np.full(tree.n, 0, dtype=object)
    def flagNeighbors(flame):
        for neighbor in flame.neighbors:
            neighbor = tree[neighbor]
            if neighbor.z < flame.z and ((neighbor.x - flame.x)**2 + (neighbor.y - flame.y)**2)<.008:
                neighbor.flag = flame.flag - 1
                if neighbor.flag > 1: flagNeighbors(neighbor)
    smokeC = np.array([5, 5, 5])
    while time() - startTime < duration:
        dt = time() - lastTime
        lastTime = time()
        tree.fade(halflife = 0.05, dt = dt)
        if rng.random() < 2:
            flames = rng.choice(tree.pixels, 20)
            for i, flame in enumerate(flames):
                if flame.z > 0.75*tree.zMax or (flame.z > 0.5*tree.zMax and rng.random() < .6):
                    continue
                flame.flag = 20
                flagNeighbors(flame)
        smoke = np.where((tree.z > 0.65*tree.zMax) & (rng.random(tree.n) < 0.1))[0]
        onetwoone = np.where(tree.z < 1.1*np.cos(0.5*PI*tree.x)*np.cos(0.5*PI*tree.y) + 0.3)[0]
        for i in smoke:
            tree[i].setColor(smokeC)
        for i in onetwoone:
            tree[i].setColor(one + twoone*rng.random())
        for pixel in tree:
            if pixel.flag > 0:
                if rng.random() < 0.9:
                    pixel.setColor(RED)
                else:
                    pixel.setColor(ORANGE)
                pixel.flag -= 6
        tree.show()

# Creates a gradient between all the colors specified
# Can soften or harshen the gradient if desired
def gradient(colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
                 , softness = 2, variant = 3, NORMALIZE = False, indices = None):
    if colors is None:
        Color = lambda: rng.integers(0, 256, 3)
        color1 = Color()
        color2 = contrast_color(color1, Color)
        colors = [color1, color2]
    n = len(colors)
    # Softness determines how much colors overlap
    # At softness = 2, pure colors with no overlap will exist at single points
    # At softness = 1, colors will fade to black before fading into the new color (if normalizing)
    # Each increase in softness by 2 will extend the time it takes for one color to fade
    # all the way to 0 into the peak of one additional color
    # fractional values are fine
    softness = min(softness, n)
    period = softness / n
    # Used to adjust the period of the functions
    p = TAU / period
    width = period / 2
    def Color(x):
        factors = []
        for i in range(n):
            if abs(x - i/n) < width:
                factor = 0.5*np.cos(p*(x - i/n)) + 0.5
            elif (i/n > x) and (i/n + width > 1) and (((i/n + width) % 1) > x):
                factor = 0.5*np.cos(p*(x + 1 - i/n)) + 0.5
            elif (i/n < x) and (i/n - width < 0) and (((i/n - width) % 1) < x):
                factor = 0.5*np.cos(p*(x - 1 - i/n)) + 0.5
            else:
                factor = 0
            factors.append(factor)
        factors = np.array(factors)
        if NORMALIZE:
            # Normalize the factors so they add to 1
            factorSum = max(1, np.sum(factors))
            factors = factors / factorSum
        color = colors * factors.reshape(n, -1)
        color = np.sum(color, axis = 0)
        if not NORMALIZE:
            # Normalize the color so its brightest component is 255
            maxC = np.max(color)
            color = 255 * color / maxC
        return color.astype(np.uint8)
    if indices is None:
        indices = tree.indices[variant]
    for i, j in enumerate(indices):
        tree[j].setColor(Color(i/(tree.n - 1)))
    tree.show()

# Displays the images in sequence, requires keyboard input
def imageSlideshow():
    for image in Path('/home/pi/Desktop/TreeLights/Images/').iterdir():
        display_image(image)
        input()
        display_image2(image)
        print(image[:-4])
        input()
    tree.clear()

# All blue, flickers random lights white, like twinkling stars
def nightSky(duration = np.inf):
    startTime = time()
    lastTime = startTime
    flickerLength = 0.2 # seconds
    p = 0.07 # probability per light per second
    twinkleTimes = np.zeros(tree.n)
    tree.fill(BLUE)
    while (t := time()) - startTime < duration:
        dt = t - lastTime
        lastTime = t
        twinkleTimes -= dt
        twinkle = (twinkleTimes <= 0) & (rng.random(tree.n) > (1-p)**dt)
        twinkleTimes[twinkle] = flickerLength
        twinkleOn = np.where(twinkle)[0]
        twinkleOff = np.where((-dt < twinkleTimes) & (twinkleTimes < 0))[0]
        for i in twinkleOn:
            tree[i].setColor(WHITE)
        for i in twinkleOff:
            tree[i].setColor(BLUE)
        tree.show()

# A growing and shrinking spear that moves up and down and changes colors
def pulsatingSphere(colors = None, dR = 0.7, dH = 0.3, duration = np.inf):
    startTime = time()
    lastTime = startTime
    Color = color_builder(colors)
    color1 = Color()
    color2 = BLACK
    while not contrast(color1, color2): color2 = Color()
    height = 0.45 * tree.zMax + 0.1 * rng.random()
    minH = tree.zMin
    maxH = tree.zMax
    maxR = .75*tree.rMax
    minR = 0
    r = minR
    while time() - startTime < duration:
        dt = time() - lastTime
        lastTime = time()
        if r <= minR:
            dR = abs(dR)
            color1 = color2
            while not contrast(color1, color2): color1 = rng.choice(COLORS)
        elif r > maxR:
            dR = -abs(dR)
        if height - r < minH:
            dH = abs(dH)
            height = minH + r
        elif height + r > maxH:
            dH = -abs(dH)
            height = maxH - r
        ball = ((tree.x**2 + tree.y**2 + (tree.z - height)**2) <= (r**2))
        bg = np.where(np.logical_not(ball))[0]
        ball = np.where(ball)[0]
        for i in ball:
            tree[i].setColor(color1)
        for i in bg:
            tree[i].setColor(color2)
        r += dR*dt
        height += dH*dt
        tree.show()

# A raining effect
def rain(color = CYAN, speed = 5, wind = -4, dropCount = 8, accumulationSpeed = 0, duration = np.inf):
    startTime = time()
    lastTime = startTime
    width = 0.12
    height = 0.15
    floor = tree.zMin - 0.1
    newDrop = lambda floor: [rng.random()*TAU, rng.random()*(tree.zMax-floor) + tree.zMax]
    drops = [newDrop(floor) for i in range(dropCount)]
    while time() - startTime < duration:
        dt = time() - lastTime
        lastTime = time()
        for i in range(len(drops) - 1, -1, -1):
            drops[i][1] -= speed*dt
            drops[i][0] = (drops[i][0] + wind*dt) % TAU
            if drops[i][1] < floor:
                del drops[i]
                drops.append(newDrop(floor))
                continue
            wet = np.where((tree.z < floor) | (tree.s & (np.abs(tree.a - drops[i][0]) < width) & (abs(tree.z - drops[i][1]) < height)))[0]
            for j in wet:
                tree[j].setColor(color)
        floor += accumulationSpeed*dt
        if floor >= tree.zMax: floor = 0
        tree.show()
        tree.fade(halflife = 0.125, dt = dt)

# Random colored planes fly through the tree, leaving trails
def randomPlanes(colors = COLORS, duration = np.inf):
    startTime = time()
    lastTime = startTime
    Color = color_builder(colors)
    z = 10
    maxZ = 0
    while time() - startTime < duration:
        dt = time() - lastTime
        lastTime = time()
        if z > maxZ + 1.5:
            angleZ = rng.uniform(0, TAU)
            angleX = rng.uniform(0, PI)
            newCoords = transform(tree.coordinates[:,0:3], xr = angleX, zr = angleZ)
            minZ = np.min(newCoords[:,2])
            maxZ = np.max(newCoords[:,2])
            # Take 2.5 seconds per plane
            # Intentionally go off-tree a bit to give the fade time to fade more
            speed = (maxZ + 1.5 - minZ)/2.5
            z = minZ
            factor = rng.uniform(0, .15) # Randomized fade speed
            color = Color()
        zStep = speed * dt
        z += speed*dt
        plane = np.where(np.abs(newCoords[:,2] - z) < zStep)[0]
        for i in plane:
            tree[i].setColor(color)
        tree.show()
        tree.fade(halflife = factor, dt = dt)

# Plays the game "snake"
def snake(cycles = np.inf, duration = np.inf):
    startTime = time()
    cycle = 0
    while time() - startTime < duration and cycle < cycles:
        tree.clear(UPDATE = False)
        snake = [rng.choice(tree)]
        pellet = rng.choice(tree)
        visited = [] # Prevents loops
        while time() - startTime < duration:
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
                neighbor = tree[neighbor]
                if (neighbor == pellet
                    or (neighbor not in snake
                        and neighbor not in visited
                        and (destination is None
                             or np.linalg.norm(neighbor.coordinate - pellet.coordinate) < np.linalg.norm(destination.coordinate - pellet.coordinate)))):
                    freeSpots = 0
                    for neigh in neighbor.neighbors:
                        if tree[neigh] not in snake and tree[neigh] not in visited: freeSpots += 1
                    if neighbor == pellet or freeSpots >= 1: destination = neighbor
            if destination is None: # No valid spots to move to
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
                    snake[i].setColor([max(510*(abs(f-0.5) - 1/6), 0), max(765*(-abs(f-1/3)+1/3), 0), max(765*(-abs(f-2/3)+1/3), 0)])
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
            cycle += 1

# Rotates a plane about some axis
def spinningPlane(colors = COLORS, variant = 0, speed = 4, width = 0.15, height = tree.zMid
                  , TWOCOLORS = False, BACKGROUND = False, SPINNER = False, duration = np.inf):
    startTime = time()
    lastTime = startTime
    Color = color_builder(colors)
    color1 = Color()
    color2 = contrast_color(color1, Color)
    colors = [color1, color2]
    if SPINNER: BACKGROUND, TWOCOLORS = True, True
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
    while (tt := time()) - startTime < duration:
        dt = tt - lastTime
        lastTime = tt
        newCoords = transform(tree.coordinates[:,0:3], z = -height, zr = -theta, xr = t, yr = PI/2 - phi)
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
        t += speed * dt
        tree.show()

# Makes spirals
def spirals(colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
             , variant = 1, spinCount = 2, zSpeed = 1, spinSpeed = -2, SURFACE = False, offset = 0
             , SKIPBLACK = True, GENERATEINSTANTLY = False, GENERATETOGETHER = False, ENDAFTERSPIRALS = False
             , PRECLEAR = True, POSTCLEAR = False, SPINAFTERDONE = False
             , duration = np.inf, cycles = 1):
    startTime = time()
    lastTime = startTime
    colors = np.array(colors)
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
    cycle, angleOffset, z = 0, 0, 0
    # Set spiral to first non-black spiral
    spiral = np.argmax(np.all(colors == OFF))
    # Precomputing some values becaues this function sometimes gets laggy
    m1 = sectionH / TAU
    m2 = -TAU / sectionH
    m2sp1 = m2**2 + 1
    tree.flags = np.array([None, sectionH*(tree.z // sectionH)], dtype=object)
    npA = np.array([pixel.a for pixel in tree])
    npZ = np.array([pixel.z for pixel in tree])
    npSpirals = np.array([[i] for i in range(spiralCount)])
    npSpirals = (npSpirals + 1)*dTheta
    while (t := time()) - startTime < duration:
        dt = t - lastTime
        lastTime = t
        if PRECLEAR or spinSpeed != 0:
            tree.fill(OFF)
        angle = (tree.a + angleOffset + offset) % TAU
        m = ((tree.z % sectionH - variant*angle*sectionH/TAU) // spiralH) % spiralCount
        m = m.astype(np.int32)
        drawNow = ((GENERATEINSTANTLY | DONE | (m < spiral))
                   & ((not GENERATETOGETHER) or DONE)
                   & ((not SURFACE) | tree.s)
                   & (SKIPBLACK & ~np.all(colors[m] == BLACK, axis=1)))
        drawNow = np.where(drawNow)[0]
        for i in drawNow:
            tree[i].setColor(colors[m[i]])
        if not GENERATEINSTANTLY and not DONE:
            npAngle = (variant * (tree.a + angleOffset) - npSpirals) % TAU
            npTopOfSpiral = m1*npAngle + sectionH * (tree.z // sectionH)
            npAngle += TAU * (((tree.z - m1*npAngle) // sectionH) + 1)
            npSpiralEdge = m2*npAngle + m2sp1*z
            for spi in range(*[[spiral, spiral + 1], [spiralCount]][GENERATETOGETHER]):
                condition = ((tree.z < npSpiralEdge[spi])
                             & (((tree.z <= npTopOfSpiral[spi])
                                 & (tree.z > npTopOfSpiral[spi] - spiralH))
                                | ((tree.z <= npTopOfSpiral[spi] + spiralDistBetweenTops)
                                   & (tree.z > npTopOfSpiral[spi] + spiralDistBetweenTops - spiralH)))
                             & ((not SURFACE) | tree.s))
                condition = np.where(condition)[0]
                for i in condition:
                    tree[i].setColor(colors[m[i]])
        tree.show()
        if (not SPINAFTERDONE or DONE): angleOffset = (angleOffset + spinSpeed * dt) % TAU
        if GENERATEINSTANTLY or DONE:
            if ENDAFTERSPIRALS:
                if POSTCLEAR: tree.clear(UPDATE = False)
                return
            continue
        if z <= tree.zRange + spiralH: z += zSpeed * dt # Mid-stripe, increase z and continue
        else: # Stripe is complete
            z = 0 # Reset z
            if spiral < spiralCount: # If we aren't done
                spiral += 1 # Then move on to the next stripe
                while spiral < spiralCount and SKIPBLACK and np.array_equal(colors[spiral], OFF): # Option to skip black because it just keeps the pixels off
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
    lastTime = startTime
    if colors is None:
        color1 = rng.integers(0, 256, 3)
        color2 = rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != np.ndarray:
            print("Must supply at least two colors")
            return
        color1, color2 = colors[0], colors[1]
    radius = 0.45 # Of the spotlight
    dzMax = 2.5
    dThetaMax = 4
    z = rng.uniform(0, 0.6*tree.zMax) # Spotlight's initial z-coordinate
    dz = rng.uniform(-dzMax, dzMax) # units/second
    theta = rng.uniform(0, TAU) # Spotlight's initial angle around z-axis
    dTheta = rng.uniform(-dThetaMax, dThetaMax) # radians/second
    # m and b used to calculate point on tree's surface from z and theta
    m = tree.xMax / (tree[tree.sortedX[-1]].z - tree[tree.sortedZ[-1]].z)
    b = -m * tree[tree.sortedZ[-2]].z
    while (t := time()) - startTime < duration:
        dt = t - lastTime
        lastTime = t
        z += dz * dt
        theta += dTheta * dt
        if z + radius > tree.zMax:dz = -abs(dz)
        if z - radius < 0: dz = abs(dz)
        point = [(m*z+b)*np.cos(theta), (m*z+b)*np.sin(theta)] + [z] # On or near surface of tree
        light = tree.s & (((tree.x - point[0])**2 + (tree.y - point[1])**2 + (tree.z - point[2])**2) < radius**2)
        bg = np.where(np.logical_not(light))[0]
        light = np.where(light)[0]
        for i in light:
            tree[i].setColor(color1)
        for i in bg:
            tree[i].setColor(color2)
        dz = min(dzMax, max(-dzMax, dz + rng.uniform(-.5, .5)))
        dTheta = min(dThetaMax, max(-dThetaMax, dTheta + rng.uniform(-2.2, 2.2)))
        tree.show()

# Sweeps colors around the tree
def sweep(colors = COLORS, speed = 5, CLOCKWISE = False, ALTERNATE = True, duration = np.inf):
    startTime = time()
    lastTime = startTime
    Color = color_builder(colors)
    color = Color()
    newColor = Color()
    speed = abs(speed)
    angle = 0
    while (t := time()) - startTime < duration:
        dt = t - lastTime
        lastTime = t
        angle += speed * dt
        if angle >= TAU + speed: # Adding speed adds 1 second delay
            if ALTERNATE: CLOCKWISE = not CLOCKWISE
            angle = 0
            while not contrast(newColor, color): newColor = Color()
            color = newColor
        if CLOCKWISE:
            front = np.where(np.abs(tree.a - angle) <= speed*dt)[0]
        else:
            front = np.where(np.abs(TAU - tree.a - angle) <= speed*dt)[0]
        for i in front:
            tree[i].setColor(color)
        tree.show()

# Sweeps around the tree continuously and smoothly changing colors
def sweeper(colors = COLORS[1:], speed = 5, SEQUENCE = True, duration = np.inf):
    startTime = time()
    lastTime = startTime
    if SEQUENCE:
        Color = lambda k: colors[((np.where(np.all(colors == k, axis = 1))[0][0] + 1) % len(colors))]
    else:
        Color = color_builder(colors)
    if SEQUENCE:
        oldColor = colors[0]
        nextColor = colors[1]
    else:
        oldColor = Color()
        nextColor = Color()
        while not contrast(nextColor, oldColor): nextColor = Color()
    angles = tree.a
    if speed < 0:
        speed = abs(speed)
        angles = TAU - angles
    angle = 0
    while (t := time()) - startTime < duration:
        dt = t - lastTime
        lastTime = t
        angle += speed * dt
        if angle > TAU:
            angle = 0
            oldColor = nextColor
            if SEQUENCE:
                nextColor = Color(oldColor)
            else:
                while not contrast(nextColor, oldColor): nextColor = Color()
        color = oldColor + (angle/TAU)*(nextColor - oldColor)
        front = np.where(np.abs(angles - angle) <= speed*dt)[0]
        for i in front:
            tree[i].setColor(color)
        tree.show()

# Sets all LEDs randomly then lets their brightness vary
def twinkle(colors = TRADITIONALCOLORS, intensity = 1.8, length = .3, p = 0.04, duration = np.inf):
    startTime = time()
    lastTime = startTime
    colors = np.array(colors)
    factor = 255 / np.max(intensity*colors)
    if factor < 1:
        colors = (factor * colors).astype(np.uint8)
    set_all_random(colors)
    buffer = np.array(tree._pre_brightness_buffer)
    intensity -= 1
    tree.flags = np.full(tree.n, 0.0)
    while (t := time()) - startTime < duration:
        dt = t - lastTime
        lastTime = t
        # Negative flags are inactive and regular brightness
        # Randomly set lights to length to activate twinkle
        # Brightness increases, peaks, decreases, and hits regular again as flag decreases to 0 and below
        tree.flags -= dt
        tree.flags[((tree.flags <= 0) & (np.random.rand(tree.n) < p))] = length
        activeLights = (tree.flags > 0)
        f = np.full(tree.n, 1.0)
        f[activeLights] = (1 + intensity * (1 - np.abs(2*tree.flags[activeLights]/length - 1)))
        f = np.column_stack((f, f, f)).flatten()
        new_buffer = buffer * f
        tree.setColors(new_buffer)
        tree.show()

# Has all LEDs let their color wander around at random
def wander(colors = COLORS, wanderTime = 1, variance = None, duration = np.inf):
    startTime = time()
    lastTime = startTime
    Color = color_builder(colors)
    if variance is None:
        variance = wanderTime / 5
    # Start with colors the tree already has, for nice fade-in effect
    oldColors = np.array([pixel.color for pixel in tree])
    color_buffer = oldColors
    newColors = np.array([Color() for _ in range(tree.n)])
    lengths = np.array([rng.uniform(wanderTime - variance, wanderTime + variance) for _ in range(tree.n)])
    # Add variance to the initial lengths so they aren't synchronized. This is done to avoid lag.
    lengths = lengths + rng.random(tree.n)*wanderTime
    times = np.full(tree.n, time())
    while (t := time()) - startTime < duration:
        dt = t - lastTime
        lastTime = t
        elapsedTimes = t - times
        expiredLights = elapsedTimes > lengths
        if (expiredLen := len(np.where(expiredLights)[0])) > 0:
            oldColors[expiredLights] = color_buffer[expiredLights]
            newColorsTemp = [Color() for _ in range(expiredLen)]
            newColors[expiredLights] = newColorsTemp
            times[expiredLights] = t - dt
            elapsedTimes[expiredLights] = dt
            lengths[expiredLights] = [rng.uniform(wanderTime - variance, wanderTime + variance) for _ in range(expiredLen)]
        f = np.array([elapsedTimes / lengths])
        color_buffer = oldColors + f.T * (newColors - oldColors)
        tree.setColors(color_buffer.flatten())
        tree.show()

# Draws spirals and winds them up
def windingSpirals(colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], maxSpinCount = 4, dSpin = 3, dOffset = 1, duration = np.inf):
    startTime = time()
    lastTime = startTime
    variant = 1
    spinCount = 0.01
    offset = 0
    while (t := time()) - startTime < duration:
        dt = t - lastTime
        lastTime = t
        spirals(colors = colors, variant = variant, spinCount = spinCount, GENERATEINSTANTLY = True, offset = offset, ENDAFTERSPIRALS = True)
        spinCount += dSpin * dt
        offset += dOffset * dt
        if spinCount > maxSpinCount:
            dSpin = -abs(dSpin)
            spinCount += dSpin * dt
        if spinCount <= 0.01:
            dSpin = abs(dSpin)
            spinCount = 0.01
            variant *= -1
            colors.reverse()

# Spirals out from the tree's z-axis, in rainbow colors
def zSpiral(twists = 8, speed = TAU, backwards = True, duration = np.inf, cycles = np.inf):
    startTime = time()
    lastTime = startTime
    totalAngle = TAU * twists
    # Finds the angle of each light in the correct section of spiral - so going beyond TAU
    # Makes sense if you diagram it out: x-axis from 0 to 2PI, y-axis from 0 to tree.rMax, plot spiral
    # Fullly simplified
    angles = tree.a + TAU * np.ceil(twists*tree.r/tree.rMax - tree.a/TAU)
    if backwards:
        angles = (TAU-tree.a) + TAU * np.ceil(twists*tree.r/tree.rMax - (TAU - tree.a)/TAU)
    # Use of the following 3 variables is mostly to make sure red definitely shows up
    # Not certain otherwise as Color is only red for very small and very large angles
    aMin = np.min(angles)
    aMax = np.max(angles)
    aRange = aMax - aMin
    # Color is intentionally basd on angle around spiral instead of radius, even though
    # the two are very similar and radius is way easier to calculate
    # This is because it creates a nice shimmer effect when run through the radial cycle after
    Color = lambda a: [255 * max(min( 3*abs(a/aRange - 0.5) - 0.5, 1), 0),
                       255 * max(min(-3*abs(a/aRange - 1/3) + 1.0, 1), 0),
                       255 * max(min(-3*abs(a/aRange - 2/3) + 1.0, 1), 0)]
    colors = [Color(a - aMin) for a in angles]
    tree.clear(UPDATE = False)
    angle = 0
    done = 0
    cycle = 0
    while cycle < cycles and (t := time()) - startTime < duration:
        dt = t - lastTime
        lastTime = t
        angle += dt*speed
        # Find lights between current and previous angle
        angleDiffs = angle - angles
        newLights = np.where((angleDiffs <= dt*speed) & (angleDiffs > 0))[0]
        for i in newLights:
            tree[i].setColor(colors[i])
        done += len(newLights)
        tree.show()
        if done == tree.n:
            cycle += 1
            angle = 0
            done = 0
            if cycle != cycles:
                tree.clear(UPDATE = False)
