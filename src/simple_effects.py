from common_variables import rng, tree, PI
from colors import *
from helper_functions import color_builder
import numpy as np
from time import time
from PIL import Image

def pickle():
    # Last updated 2022
    # Use to show position of pickle and ketchup on tree
    tree.clear(update= False)
    tree[548].set_color(GREEN)
    tree[61].set_color(GREEN)
    tree[49].set_color(RED)
    tree.show()

# Makes the tree look like a candy corn
def candy_corn():
    for pixel in tree:
        if pixel.z <= 0.25*tree.z_max:
            pixel.set_color(YELLOW)
        elif pixel.z <= 0.7*tree.z_max:
            pixel.set_color(ORANGE)
        else:
            pixel.set_color(WHITE)
    tree.show()

# Displays images
def display_image(file_name, mark_template = False):
    path = '/home/pi/Desktop/TreeLights/Images/' + file_name
    with Image.open(path) as im:
        img = im.load()
        tree.clear(update= False)
        xs = im.size[0] * (tree.y + 1) / 2
        ys = im.size[1] - 1 - (im.size[0] * tree.z / 2)
        do = np.where(np.logical_not((xs < 0) | (ys < 0) | (xs > (im.size[0] - 1)) | (ys > (im.size[1] - 1))))[0]
        for i in do:
            x = xs[i]
            y = ys[i]
            if mark_template:
                im.putpixel((int(x), int(y)), (0, 0, 0, 255))
            else:
                color = list(img[x, y][0:3])
                if color != [237, 28, 36]:
                    tree[i].set_color(color)
        if mark_template:
            im.save(path[:-4] + '_marked.png')
    tree.show()

# Displays images, but with perspective
def display_image2(file_name, mark_template = False):
    path = '/home/pi/Desktop/TreeLights/Images/' + file_name
    eye = np.array([17, 0, 1.5])
    with Image.open(path) as im:
        img = im.load()
        tree.clear(update= False)
        vect = eye - tree.coordinates[:,0:3]
        t = -eye[0] / vect[:,0]
        xs = (-(vect[:,1]*t + eye[1]) + 1) * im.size[0] / 2
        ys = im.size[1] - (vect[:,2]*t + eye[2]) * im.size[1] / tree.z_max
        do = np.where(np.logical_not((xs < 0) | (ys < 0) | (xs > im.size[0] - 1) | (ys > im.size[1] - 1)))[0]
        for i in do:
            x = xs[i]
            y = ys[i]
            if mark_template:
                im.putpixel((int(x), int(y)), (0, 0, 0, 255))
            else:
                color = list(img[-x, y][0:3])
                if color != [237, 28, 36]:
                    tree[i].set_color(color)
        if mark_template:
            im.save(path[:-4] + '_marked.png')
    tree.show()

# Makes the tree pizza
def pizza():
    # Pepperonis are randomly generated, and rejected if poorly positioned
    # Try to make this many - usually only accept 4-7 total
    pepperoni_count = 100
    r = .35
    crust_height = 0.15*tree.z_max
    cheese_color = [255, 140, 0]
    crust_color = [64, 12, 0]
    # Entire backside of the pizza plus the bottom part is crust
    crust = tree.z < crust_height
    # Everywhere else is cheese
    cheese = np.where(np.logical_not(crust))[0]
    crust = np.where(crust)[0]
    for i in crust:
        tree[i].set_color(crust_color)
    for i in cheese:
        tree[i].set_color(cheese_color)
    pepperonis = []
    # m and b used to calculate point on tree's surface from z and theta
    m = tree.x_max / (tree[tree.sorted_x[-1]].z - tree[tree.sorted_z[-1]].z)
    b = -m * tree[tree.sorted_z[-2]].z
    for _ in range(pepperoni_count):
        z = crust_height + r + rng.random()*(tree.z_max - crust_height - r)
        theta = rng.random() * 2 * PI
        pepperoni = [(m*z+b)*np.cos(theta), (m*z+b)*np.sin(theta)] + [z] # On or near surface of tree
        #add = True
        #for oldPepperoni in pepperonis:
        #    dist = ((oldPepperoni[0] - pepperoni[0])**2 + (oldPepperoni[1]-pepperoni[1])**2 + (oldPepperoni[2]-pepperoni[2])**2)**0.5
        #    # Any closer and it can look like they're overlapping - ugly
        #    if dist < 2.3*r:
        #        add = False
        #        break
        #if not add: continue
        add = True
        dists = ((tree.x - pepperoni[0])**2 + (tree.y - pepperoni[1])**2 + (tree.z - pepperoni[2])**2)**0.5
        to_light = tree.s & (dists < r)
        big_r = tree.s & (0.6*r < dists) & (dists < 1.15*r)
        to_light = np.where(to_light)[0]
        big_r = np.where(big_r)[0]
        for old_pepperoni in pepperonis:
            common = np.intersect1d(old_pepperoni[4], big_r)
            if common.size > 0:
                add = False
                break
        if not add: continue
        pepperonis.append([pepperoni[0], pepperoni[1], pepperoni[2], to_light, big_r])
    if len(pepperonis) < 7:
        return pizza()
    for pepperoni in pepperonis:
        for i in pepperoni[3]:
            tree[i].set_color(RED)
    tree.show()

# Displays a pokéball
def pokeball():
    tree.clear(update= False)
    height = 1.1
    radius = 0.9
    ball = (tree.x**2 + tree.y**2 + (tree.z - height)**2) < radius**2
    bg = np.where(np.logical_not(ball))[0]
    top = np.where((tree.z > height) & ball)[0]
    bottom = np.where((tree.z <= height) & ball)[0]
    for i in bg:
        tree[i].set_color([25, 25, 0])
    for i in top:
        tree[i].set_color(RED)
    for i in bottom:
        tree[i].set_color(WHITE)
    tree.show()

def traffic_cone():
    # Values determined experimentally
    top_stripe_height = 0.715*tree.z_max
    bottom_stripe_height = 0.466*tree.z_max
    top_stripe_width = 0.124*tree.z_max
    bottom_stripe_width = top_stripe_width / 2
    white = (np.abs(tree.z - top_stripe_height) < top_stripe_width) | (np.abs(tree.z - bottom_stripe_height) < bottom_stripe_width)
    orange = np.where(np.logical_not(white))[0]
    white = np.where(white)[0]
    for i in white:
        tree[i].set_color(WHITE)
    for i in orange:
        tree[i].set_color(ORANGE)
    tree.show()

# Turns lights on one at a time in random order in random colors, then turns them off in the same fashion
def random_fill(colors = COLORS, speed = 100, sequence = False, empty = True, cycles = np.inf, duration = np.inf):
    start_time = time()
    last_time = start_time
    pick_color = color_builder(colors)
    tree.clear()
    done = 0
    cycle = 0
    on = True
    limit = tree.n + empty * speed
    order = np.arange(tree.n) if sequence else rng.permutation(tree.n)
    tree.clear(update= False)
    if not empty: set_all_random(colors = colors)
    while (t := time()) - start_time < duration and cycle < cycles:
        dt = t - last_time
        last_time = t
        lights_to_do = max(int(dt*speed), 1)
        for i in range(min(done, tree.n), min(done + lights_to_do, tree.n)):
            if on:
                tree[order[i]].set_color(pick_color())
            else:
                tree[order[i]].set_color(OFF)
        done += lights_to_do
        if done >= limit:
            done = 0
            order = np.arange(tree.n) if sequence else rng.permutation(tree.n)
            if on:
                if empty: on = False
                limit = tree.n
                if sequence: order = np.flip(order)
            else:
                on = True
                limit = tree.n + empty * speed
            cycle += 1
        tree.show()

# Rapid flashing of blue and yellow
def seizure(duration = np.inf):
    start_time = time()
    while time() - start_time < duration:
        tree.fill(BLUE)
        tree.show()
        tree.fill(YELLOW)
        tree.show()

# Sets all LEDs to the same color
def set_all(colors = None):
    pick_color = color_builder(colors)
    tree.fill(pick_color())
    tree.show()

# Sets all LEDs to a random color
def set_all_random(colors = None):
    pick_color = color_builder(colors)
    for pixel in tree:
        pixel.set_color(pick_color())
    tree.show()
