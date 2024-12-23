from time import sleep, time

from common_variables import rng, tree, save_coords, build_tree
from colors import *
from simple_effects import color_builder

# Has each light blink out its index number in binary
def binary(sleep_length = .5, backwards = False):
    max_length = len(bin(tree.n - 1)[2:])
    binary_reps = [(max_length * "0" + bin(i)[2:])[-max_length:] for i in range(tree.n)]
    if backwards: binary_reps = [rep[::-1] for rep in binary_reps]
    for d in range(max_length):
        for i in range(tree.n):
            if binary_reps[i][d] == "0":
                tree[i] = RED
            else:
                tree[i] = GREEN
        tree.show()
        sleep(sleep_length)
        tree.clear()
        sleep(sleep_length)

# Sequentially shows all LEDs and their "connected" neighbors
def connectivity_test():
    total_connections = 0
    lone_leds = 0
    poorly_connected = 0
    for pixel in tree:
        connections = len(pixel.neighbors)
        total_connections += connections
        pixel.set_color(GREEN)
        if connections < 4:
            poorly_connected += 1
            pixel.set_color(YELLOW)
        if connections == 2:
            lone_leds += 1
            pixel.set_color(RED)
    print(total_connections, "connections among", tree.n, "with", lone_leds, "neighborless LEDs and", poorly_connected,
          "poorly connected LEDs, and an average of", total_connections/tree.n, "connections per LED")
    tree.show()
    input()
    for pixel in tree:
        tree.clear(update= False)
        pixel.set_color(RED)
        for neighbor in pixel.neighbors:
            tree[neighbor].set_color(GREEN)
        tree.show()
        input()
    tree.clear()

# Continuously updates all LEDs with a color - useful when stringing the tree
def continuous_update(color = WHITE):
    if color is not None: tree.fill(color)
    while True:
        tree.show()
        sleep(0.5)

# Lights up all pixels that are locally the lowest
def find_floor():
    tree.clear()
    for pixel in tree:
        lowest = True
        for neighbor in pixel.neighbors:
            if tree[neighbor].z < pixel.z:
                lowest = False
                break
        if lowest:
            pixel.set_color(RED)
    tree.show()

# Used by adjustLight below
# Lights up all LEDs with a similar coordinate to the indicated LED
def light_slice(n, dim, width = 0.015):
    for pixel in tree:
        if abs(pixel.coordinate[dim] - tree[n].coordinate[dim]) < width:
            pixel.set_color(WHITE)
        else:
            pixel.set_color(OFF)
    tree[n].set_color(GREEN)
    tree.show()

# Used to adjust a specific coordinate for a specific light
def adjust_light(n, dim):
    global tree
    dims = ["x", "y", "z"]
    if dim not in dims:
        print("""Must specify "x", "y", or "z" dimension""")
        return
    dim = dims.index(dim)
    if n < 0 or n >= tree.n:
        print("Given n is outside of acceptable range.")
        return
    while True:
        light_slice(n, dim)
        print("Current " + str(dims[dim]) + "-coord: " + str(tree[n].coordinate[dim]))
        delta = input("Increase (+) or decrease (-)? ")
        if delta == "":
            break
        elif delta == "+":
            delta = .02
        elif delta == "-":
            delta = -.02
        else:
            continue
        tree[n].coordinate[dim] += delta
    save = input("Save (y/n)? ")
    if save not in ["y", "Y"]:
        return
    coordinates = []
    for pixel in tree:
        coordinates.append(pixel.coordinate)
    save_coords(coordinates)
    tree = build_tree()

# Help determine the maximum theoretical framerate of the tree under various circumstances
def max_framerate(duration = 10, variant = 0):
    start_time = time()
    tree.frames = 0
    while time() - start_time < duration:
        if variant == 0: # tree.setColors
            colors = rng.integers(0, 256, 3*tree.n)
            tree.set_colors(colors)
        elif variant == 1: # pixel.setColor
            colors = rng.integers(0, 256, 3*tree.n)
            colors = colors.reshape(tree.n, 3)
            for i, pixel in enumerate(tree):
                pixel.set_color(colors[i])
        elif variant == 2: # No color changing
            pass
        tree.show()
    duration = time() - start_time
    print(f"maxFramerate: {tree.frames} frames in {round(duration, 2)} seconds for {round(tree.frames/duration, 2)} fps")

# Divide the tree into halves to detect (and fix) misplaced lights
def plane_test(sections = 20, variant ="y", start_at = 1):
    property_index = ["x", "y", "z"].index(variant)
    min_val = [-1, -1, 0][property_index]
    increment = [2 / sections, 2 / sections, tree.z_max / sections][property_index]
    for boundary in range(start_at, sections + 1):
        tree.clear(update= False)
        boundary_val = boundary*increment
        for pixel in tree:
            if pixel.coordinate[property_index] <= min_val + boundary_val:
                pixel.set_color(RED)
            else:
                pixel.set_color(GREEN)
        tree.show()
        if boundary == sections: continue
        x = input("Enter to continue, anything else to flash binary and fix")
        if x == "":
            continue
        binary(sleep_length= 0.25)
        x = input()
        x = int(x, 2)
        adjust_light(x, variant)
        plane_test(sections, variant, start_at= boundary)
        return
    tree.clear()

# Turns on lights one-by-one in the sorted directions
def sorted_test(colors = None, speed = 1, variant ="z"):
    pick_color = color_builder(colors)
    index = ["i", "x", "y", "z", "r", "a"].index(variant)
    order = tree.indices[index]
    color = pick_color()
    for count, i in enumerate(order, start = 1):
        tree[i].set_color(color)
        if count % speed == 0 or count == tree.n:
            tree.show()

# Illuminates the interior and surface LEDs on the tree in different colors
def surface_test(interior = BLUE, surface = RED):
    for pixel in tree:
        if pixel.surface:
            pixel.set_color(surface)
        else:
            pixel.set_color(interior)
    tree.show()
