from Common_Variables import rng, tree, PI, TAU
from Colors import *
from Helper_Functions import *
import numpy as np
from time import time, sleep
from PIL import Image

def pickle():
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
        for pixel in tree:
            x = im.size[0] * (-pixel.x + 1) / 2
            y = im.size[1] - 1 - (im.size[0] * pixel.z / 2)
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

# Displays images, but with perspective
def displayImage2(fileName, markTemplate = False):
    PATH = "/home/pi/Desktop/TreeLights/Images/" + fileName
    eye = np.array([0, 4.5, 2.2])
    with Image.open(PATH) as im:
        img = im.load()
        tree.clear(UPDATE = False)
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

def gradient(colors = COLORS, variant = None, backwards = False, speed = 10, duration = 99999):
    if colors == None:
        color1 = rng.integers(0, 256, 3)
        color2 = rng.integers(0, 256, 3)
        while not contrast(color1, color2): color2 = rng.integers(0, 256, 3)
        color1 = 255 * color1 / (color1[0] + color1[1] + color1[2])
        color2 = 255 * color2 / (color2[0] + color2[1] + color2[2])
    else:
        if type(colors[0]) != list or len(colors) < 2:
            print("You must supply at least two colors for this effect")
            return
        color1, color2 = rng.choice(colors, 2, False)
        while not contrast(color1, color2): color2 = rng.choice(colors)
    if variant == None: variant = rng.integers(3, 5)
    index = tree.indices[variant]
    diff = 2*(color2 - color1)/(tree.LED_COUNT - 1)
    for i in range(tree.LED_COUNT):
        if i < tree.LED_COUNT / 2:
            tree[index[i]] = color1 + i*diff
        else:
            tree[index[i]] = tree[index[tree.LED_COUNT - i - 1]].color
    tree.show()
    tree.cycle(variant, step = speed, backwards = backwards, duration = duration)

# Makes the tree pizza
def pizza():
    pepperoniCount = 5
    pepperoniRadius = 1/8
    crustHeight = 0.7
    cheeseColor = [140, 255, 0]
    crustColor = [12, 64, 0]
    for pixel in tree:
        if pixel.z < crustHeight or pixel.x < 0:
            pixel.setColor(crustColor)
        else:
            pixel.setColor(cheeseColor)
    for pepperoni in range(pepperoniCount):
        pepperoniHeight = crustHeight + rng.random()*(tree.zMax - crustHeight)
        pepperoniY = tree.yMin + rng.random() * (tree.yMax - tree.yMin)
        for pixel in tree:
            if (pixel.surface
                and pixel.x > 0
                and ((pixel.z-pepperoniHeight)**2 + (pixel.y-pepperoniY)**2)**0.5 < pepperoniRadius):
                pixel.setColor(RED)
                for neighbor in pixel.neighbors:
                    neighbor.setColor(RED)
    tree.show()

# Displays a pokéball
def pokeball():
    tree.fill([25, 25, 0])
    height = 1.1
    radius = 0.9
    for pixel in tree:
        if (pixel.x**2 + pixel.y**2 + (pixel.z-height)**2)**.5 < radius**2:
            if pixel.z > height:
                pixel.setColor(RED)
            else:
                pixel.setColor(WHITE)
    tree.show()

def rainbow(variant = None, cycle = True, duration = 99999):
    if variant == None: variant = rng.integers(2, 5)
    speed = 20
    # Cycles from red to green to blue, for 3*256 total possible colors.
    # diffBetweenLEDs determines based on LED_COUNT how much to advance
    # each LED to make this as smooth as possible
    diffBetweenLEDs = 3*256/(tree.LED_COUNT - 1)
    # Determines next color in sequence given input color and diffBetweenLEDs
    def advance(green, red, blue):
        if red == 0 and blue != 255: # Green falling, blue rising
            green = max(0, green - diffBetweenLEDs)
            blue = min(255, blue + diffBetweenLEDs)
        elif green == 0 and red != 255: # Blue falling, red rising
            blue = max(0, blue - diffBetweenLEDs)
            red = min(255, red + diffBetweenLEDs)
        elif blue == 0 and green != 255: # Red falling, green rising
            red = max(0, red - diffBetweenLEDs)
            green = min(255, green + diffBetweenLEDs)
        return [green, red, blue]
    # Initial configuration
    color = [0, 255, 0]
    index = tree.indices[variant]
    tree[index[0]] = color
    for i in range(1, tree.LED_COUNT):
        color = advance(*color)
        tree[index[i]] = color
    tree.show()
    if cycle: tree.cycle(variant, step = speed, duration = duration)

# Turns lights on one at a time in random order in random colors, then turns them off in the same fashion
def randomFill(colors = COLORS, speed = 1, cycles = 99999):
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            # Assume function was provided a single color, make a list with just that color
            colors = [colors]
        Color = lambda: rng.choice(colors)
    tree.clear()
    order = [i for i in range(tree.LED_COUNT)]
    for cycle in range(cycles):
        rng.shuffle(order)
        for i in range(tree.LED_COUNT // speed + 1):
            for j in range(speed):
                index = speed*i + j
                if index >= tree.LED_COUNT: continue
                tree[order[index]].setColor(Color())
            tree.show()
        sleep(1)
        rng.shuffle(order)
        for i in range(tree.LED_COUNT // speed + 1):
            for j in range(speed):
                index = speed*i + j
                if index >= tree.LED_COUNT: continue
                tree[order[index]].setColor(OFF)
            tree.show()
        sleep(1)

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
def sequence(colors = None, speed = 1, cycles = 1):
    for cycle in range(cycles):
        if colors == None:
            color = rng.integers(0, 256, 3)
        else:
            if type(colors[0]) != list:
                colors = [colors]
            color = rng.choice(colors)
        tree.clear()
        i = 0
        for pixel in tree:
            pixel.setColor(color)
            i += 1
            if i % speed == 0 or i == tree.LED_COUNT: tree.show()

# Sets all LEDs to the same color
def setAll(colors = None):
    if np.array_equal(colors, None):
        color = rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        color = rng.choice(colors)
    tree.fill(color)
    tree.show()

# Sets all LEDs to a random color
def setAllRandom(colors = None, speed = 0, duration = 99999):
    startTime = time()
    continuous = speed > 0
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    for pixel in tree:
        pixel.setColor(Color())
    tree.show()
    while continuous and time() - startTime < duration:
        for i in range(speed):
            tree[rng.integers(0, tree.LED_COUNT)].setColor(Color())
        tree.show()

# Sets an individual LED a given color
def setPixel(index, colors = None):
    if colors == None:
        color = rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        color = rng.choice(colors)
    tree[index] = color
    tree.show()
