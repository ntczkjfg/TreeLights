from Common_Variables import rng, tree, PI, TAU
from Colors import *
from Helper_Functions import *
import numpy as np
from time import time, sleep
from PIL import Image

def pickle():
    # Last updated 2022
    # Use to show position of pickle and ketchup on tree
    tree.clear(UPDATE = False)
    tree[548].setColor(GREEN)
    tree[61].setColor(GREEN)
    tree[49].setColor(RED)
    tree.show()

# Displays images
def displayImage(fileName, markTemplate = False):
    PATH = "/home/pi/Desktop/TreeLights/Images/" + fileName
    with Image.open(PATH) as im:
        img = im.load()
        tree.clear(UPDATE = False)
        xs = im.size[0] * (tree.y + 1) / 2
        ys = im.size[1] - 1 - (im.size[0] * tree.z / 2)
        do = np.where(np.logical_not((xs < 0) | (ys < 0) | (xs > (im.size[0] - 1)) | (ys > (im.size[1] - 1))))[0]
        for i in do:
            x = xs[i]
            y = ys[i]
            if markTemplate:
                im.putpixel((int(x), int(y)), (0, 0, 0, 255))
            else:
                color = list(img[x, y][0:3])
                if color != [237, 28, 36]:
                    tree[i].setColor(color)
        if markTemplate:
            im.save(PATH[:-4] + "_marked.png")
    tree.show()

# Displays images, but with perspective
def displayImage2(fileName, markTemplate = False):
    PATH = "/home/pi/Desktop/TreeLights/Images/" + fileName
    eye = np.array([17, 0, 1.5])
    with Image.open(PATH) as im:
        img = im.load()
        tree.clear(UPDATE = False)
        vect = eye - tree.coordinates[:,0:3]
        t = -eye[0] / vect[:,0]
        xs = (-(vect[:,1]*t + eye[1]) + 1) * im.size[0] / 2
        ys = im.size[1] - (vect[:,2]*t + eye[2]) * im.size[1] / tree.zMax
        do = np.where(np.logical_not((xs < 0) | (ys < 0) | (xs > im.size[0] - 1) | (ys > im.size[1] - 1)))[0]
        for i in do:
            x = xs[i]
            y = ys[i]
            if markTemplate:
                im.putpixel((int(x), int(y)), (0, 0, 0, 255))
            else:
                color = list(img[-x, y][0:3])
                if color != [237, 28, 36]:
                    tree[i].setColor(color)
        if markTemplate:
            im.save(PATH[:-4] + "_marked.png")
    tree.show()

# Creates a gradient betwen all the colors specified
def gradient(colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, RED], variant = 2, indices = None):
    if colors is None:
        Color = lambda: rng.integers(0, 256, 3)
        color1 = Color()
        color2 = contrastColor(color1, Color)
        colors = np.array([color1, color2, color1])
    else:
        colors = np.array(colors)
    if indices is None:
        if variant is None:
            variant = rng.integers(1, 6)
        indices = tree.indices[variant]
    separation = 1 / (len(colors) - 1)
    def Color(f):
        group = int(f/separation)
        along = (f % separation)/separation
        return colors[group] + along * (colors[group + 1] - colors[group])
    for i in indices:
        tree[indices[i]].setColor(Color(i/tree.n))
    tree.show()

# Makes the tree pizza
def pizza():
    # Pepperonis are randomly generated, and rejected if poorly positioned
    # Try to make this many - usually only accept 4-7 total
    pepperoniCount = 200
    pepperoniRadius = .35
    crustHeight = 0.7
    cheeseColor = [255, 140, 0]
    crustColor = [64, 12, 0]
    # Entire backside of the pizza plus the bottom part is crust
    crust = (tree.x < 0) | (tree.z < crustHeight)
    # Everywhere else is cheese
    cheese = np.where(np.logical_not(crust))[0]
    crust = np.where(crust)[0]
    for i in crust:
        tree[i].setColor(crustColor)
    for i in cheese:
        tree[i].setColor(cheeseColor)
    pepperonis = []
    for pepperoni in range(pepperoniCount):
        pepperoniZ = crustHeight + pepperoniRadius + rng.random()*(tree.zMax - crustHeight)
        pepperoniY = (tree.yMin + rng.random() * tree.yRange) / max(1, 3 * pepperoniZ / tree.zMax)
        add = True
        for oldPepperoni in pepperonis:
            dist = ((oldPepperoni[0]-pepperoniY)**2 + (oldPepperoni[1]-pepperoniZ)**2)**0.5
            # Any closer and it can look like they're overlapping - ugly
            if dist < 2.3*pepperoniRadius:
                add = False
                break
        if not add: continue
        toLight = np.where((tree.x > 0) & (((tree.z-pepperoniZ)**2+(tree.y-pepperoniY)**2) < (pepperoniRadius**2)))[0]
        # Check if the pepperoni is off-tree
        # Want to reject these because they'll still prevent other good pepperoni spawns
        if len(toLight) == 0:
            add = False
        if add:
            pepperonis.append([pepperoniY, pepperoniZ, toLight])
    for pepperoni in pepperonis:
        for i in pepperoni[2]:
            tree[i].setColor(RED)
    tree.show()

# Displays a pokéball
def pokeball():
    tree.clear(UPDATE = False)
    height = 1.1
    radius = 0.9
    ball = (tree.x**2 + tree.y**2 + (tree.z - height)**2) < radius**2
    bg = np.where(np.logical_not(ball))[0]
    top = np.where((tree.z > height) & ball)[0]
    bottom = np.where((tree.z <= height) & ball)[0]
    for i in bg:
        tree[i].setColor([25, 25, 0])
    for i in top:
        tree[i].setColor(RED)
    for i in bottom:
        tree[i].setColor(WHITE)
    tree.show()

def trafficCone():
    # Values determined experimentally
    topStripeHeight = 0.715*tree.zMax
    bottomStripeHeight = 0.466*tree.zMax
    topStripeWidth = 0.124*tree.zMax
    bottomStripeWidth = topStripeWidth / 2
    white = (np.abs(tree.z - topStripeHeight) < topStripeWidth) | (np.abs(tree.z - bottomStripeHeight) < bottomStripeWidth)
    orange = np.where(np.logical_not(white))[0]
    white = np.where(white)[0]
    for i in white:
        tree[i].setColor(WHITE)
    for i in orange:
        tree[i].setColor(ORANGE)
    tree.show()

# Turns lights on one at a time in random order in random colors, then turns them off in the same fashion
def randomFill(colors = COLORS, speed = 100, SEQUENCE = False, EMPTY = True, cycles = np.inf, duration = np.inf):
    startTime = time()
    lastTime = startTime
    Color = ColorBuilder(colors)
    tree.clear()
    done = 0
    cycle = 0
    ON = True
    limit = tree.n + EMPTY * speed
    order = np.arange(800) if SEQUENCE else rng.permutation(tree.n)
    tree.clear(UPDATE = False)
    if not EMPTY: setAllRandom(colors = colors)
    frames = 0
    while (t := time()) - startTime < duration and cycle < cycles:
        dt = t - lastTime
        lastTime = t
        lightsToDo = max(int(dt*speed), 1)
        for i in range(min(done, tree.n), min(done + lightsToDo, tree.n)):
            if ON:
                tree[order[i]].setColor(Color())
            else:
                tree[order[i]].setColor(OFF)
        done += lightsToDo
        if done >= limit:
            done = 0
            order = np.arange(800) if SEQUENCE else rng.permutation(tree.n)
            if ON:
                if EMPTY: ON = False
                limit = tree.n
                if SEQUENCE: order = np.flip(order)
            else:
                ON = True
                limit = tree.n + EMPTY * speed
            cycle += 1
        tree.show()
        frames += 1
    duration = round(time() - startTime, 2)
    print(f"randomFill: {frames} frames in {duration} seconds for {round(frames/duration, 1)} fps")

# Rapid flashing of blue and yellow
def seizure(duration = np.inf):
    startTime = time()
    frames = 0
    while time() - startTime < duration:
        tree.fill(BLUE)
        tree.show()
        tree.fill(YELLOW)
        tree.show()
        frames += 2
    duration = round(time() - startTime, 2)
    print(f"seizure: {frames} frames in {duration} seconds for {round(frames/duration, 1)} fps")

# Sets all LEDs to the same color
def setAll(colors = None):
    Color = ColorBuilder(colors)
    tree.fill(Color())
    tree.show()

# Sets all LEDs to a random color
def setAllRandom(colors = None):
    startTime = time()
    lastTime = startTime
    Color = ColorBuilder(colors)
    for pixel in tree:
        pixel.setColor(Color())
    tree.show()
