from Common_Variables import rng, tree, C
import numpy as np
from PIL import Image

def displayImage(fileName, markTemplate = False):
    PATH = "/home/pi/Desktop/TreeLights/Images/" + fileName
    with Image.open(PATH) as im:
        img = im.load()
        tree.clear(False)
        for pixel in tree:
            x = im.size[0] * (pixel.y + 1) / 2
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

def gradient(colors = C["COLORS"], variant = None, backwards = False):
    if colors == None:
        color1 = rng.integers(0, 256, 3)
        color2 = rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list or len(colors) < 2:
            print("You must supply at least two colors for this effect")
            return
        color1, color2 = rng.choice(colors, 2, False)
    speed = 10
    if variant == None: variant = rng.integers(2, 5)
    index = tree.indices[variant]
    greenDiff = (color2[0] - color1[0])/(tree.LED_COUNT - 1)*2
    redDiff = (color2[1] - color1[1])/(tree.LED_COUNT - 1)*2
    blueDiff = (color2[2] - color1[2])/(tree.LED_COUNT - 1)*2
    for i in range(tree.LED_COUNT):
        if i < tree.LED_COUNT / 2:
            tree[index[i]] = [color1[0] + i*greenDiff
                                , color1[1] + i*redDiff
                                , color1[2] + i*blueDiff]
        else:
            tree[index[i]] = tree[index[tree.LED_COUNT - i - 1]].color
    tree.show()
    tree.cycle(variant, step = speed, backwards = backwards)

def pokeball():
    tree.fill([25, 25, 0])
    height = 1.1
    radius = 0.9
    for pixel in tree:
        if (pixel.x**2 + pixel.y**2 + (pixel.z-height)**2)**.5 < radius**2:
            if pixel.z > height:
                pixel.setColor(C["RED"])
            else:
                pixel.setColor(C["WHITE"])
    tree.show()

def rainbow(variant = None, cycle = True):
    if variant == None: variant = rng.integers(2, 5)
    speed = 5
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
    if cycle: tree.cycle(variant, step = speed)

def rotate2(colors = [C["BLUE"], C["YELLOW"]]):
    if colors == None:
        color1 = rng.integers(0, 256, 3)
        color2 = rng.integers(0, 256, 3)
    else:
        if type(colors[0]) == list and len(colors) == 2:
            color1 = C[0]
            color2 = C[1]
        else:
            print("Must give exactly two colors for this effect")
            return
    speed = 10
    for pixel in tree:
        pixel.setColor(color1) if pixel.y > 0 else pixel.setColor(color2)
    tree.show()
    tree.cycle(4, step = speed)

def setAll(colors = None):
    if colors == None:
        color = rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        color = rng.choice(colors)
    tree.fill(color)
    tree.show()

def setAllRandom(colors = None):
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    for pixel in tree:
        pixel.setColor(Color())
    tree.show()

def setPixel(index, colors = None):
    if colors == None:
        color = rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        color = rng.choice(colors)
    tree[index] = color
    tree.show()
