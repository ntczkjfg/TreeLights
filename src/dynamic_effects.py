from time import sleep, time
from pathlib import Path
import datetime

import numpy as np

from common_variables import rng, tree, PI, TAU
from colors import *
from simple_effects import set_all, set_all_random, display_image, display_image2
from helper_functions import transform, contrast, contrast_color, color_builder

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

# Rotates the tree while running alternating colored vertical stripes alternating up and down
def alternating_stripes(background_c=None, stripe1_c=None, stripe2_c=None,
                        stripe_speed = 3, spin_speed = PI, stripe_count = 2, duration = np.inf):
    if stripe2_c is None:
        stripe2_c = [70, 15, 15]
    if stripe1_c is None:
        stripe1_c = [5, 90, 5]
    if background_c is None:
        background_c = [0, 10, 90]
    start_time = time()
    last_time = start_time
    # stripe_count is per stripe, so double for actual number
    stripe_width = TAU / (2 * stripe_count) # Stripe angular width
    # Current rotation in radians
    angle = 0
    # Height of stripe_1
    height = 0
    # Used below, needs to be defined before loop is run
    # Helps create transition effect
    prev_stripes = np.arange(tree.n)
    # Used to let the stripes go a set amount off-tree
    # To give some pause where no stripes are visible
    extra = 0.1*tree.z_max
    for pixel in tree:
        pixel.flag = np.array(pixel.color)
    maintain_background = True
    stripe1_c = np.array(stripe1_c)
    stripe2_c = np.array(stripe2_c)
    background_c = np.array(background_c)
    while time() - start_time < duration:
        dt = time() - last_time
        last_time = time()
        height += stripe_speed * dt
        if maintain_background and height >= tree.z_max:
            maintain_background = False
        if height > 2*tree.z_max + extra:
            stripe_speed = -abs(stripe_speed)
        elif height < tree.z_min - extra:
            stripe_speed = abs(stripe_speed)
        angle += (spin_speed * dt) % TAU
        stripe_1 = ((((tree.a - angle) // stripe_width) % 2 == 0)
                    & (tree.z < height)
                    & (tree.z > height - tree.z_range))
        stripe_2 = ((((tree.a - angle) // stripe_width) % 2 == 1)
                    & (tree.z < 2 * tree.z_range - height)
                    & (tree.z > tree.z_range - height))
        stripe_1 = np.where(stripe_1)[0]
        stripe_2 = np.where(stripe_2)[0]
        # Background is handled like this intentionally to create a natural transition effect
        # Only pixels which were previously part of a stripe become part of the background
        # Lets the stripes swipe away previous effect, instead of having it become all background right away
        background = np.setdiff1d(np.setdiff1d(prev_stripes, stripe_1), stripe_2)
        prev_stripes = np.union1d(stripe_1, stripe_2)
        if maintain_background:
            for i in background:
                tree[i].set_color(tree[i].flag)
        else:
            for i in background:
                tree[i].set_color(background_c)
        for i in stripe_1:
            tree[i].set_color(stripe1_c)
        for i in stripe_2:
            tree[i].set_color(stripe2_c)
        tree.show()

# Blinks lights on and off
def blink(colors = TRADITIONAL_COLORS, group_count = 7, p = 0.7, delay = 1, duration = np.inf):
    start_time = time()
    last_time = start_time
    tree.clear(update= False)
    set_all_random(colors)
    for pixel in tree:
        pixel.flag = np.array(pixel.color)
    groups = rng.integers(0, group_count, tree.n)
    old_groups = np.array([True for _ in range(group_count)])
    dt = 0
    while time() - start_time < duration:
        dt += time() - last_time
        last_time = time()
        if dt < delay:
            sleep(.01)
            continue
        else:
            dt = 0
        new_groups = np.array([True if rng.random() < p else False for _ in range(group_count)])
        turn_on = np.where((new_groups > old_groups)[groups])[0]
        turn_off = np.where((new_groups < old_groups)[groups])[0]
        old_groups = new_groups
        for i in turn_on:
            tree[i].set_color(tree[i].flag)
        for i in turn_off:
            tree[i].set_color(OFF)
        tree.show()

# Courtesy of Arby
# A bouncing rainbow ball that changes size and wobbles
def bouncing_rainbow_ball(duration = np.inf):
    start_time = time()
    last_time = start_time
    radius = .7
    dr = 0.15
    min_r = 0.5
    max_r = .75
    z_angle = 0
    dz = 0.45
    max_z = PI/3
    angle = 0
    da = 1.5
    colors = np.array([RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK])
    height = radius
    acceleration = -2.5
    initial_v = 3.15
    dh = initial_v
    while (t := time()) - start_time < duration:
        dt = t - last_time
        last_time = t
        points = transform(tree.coordinates[:,0:3], z = -height, yr = -z_angle, zr = -angle)
        ball = np.where(points[:,0]**2 + points[:,1]**2 + points[:,2]**2 <= radius**2)[0]
        indices = (4*points[:,2] / radius + 4).astype(np.uint8)[ball]
        ball_colors = colors[indices]
        for i, j in enumerate(ball):
            tree[j].set_color(ball_colors[i])
        radius += dr*dt
        if radius >= max_r:
            dr = -abs(dr)
            radius = max_r
        if radius <= min_r:
            dr = abs(dr)
            radius = min_r
        z_angle += dz * dt
        if z_angle > max_z:
            dz = -abs(dz)
            z_angle = max_z
        if z_angle < -max_z:
            dz  = abs(dz)
            z_angle = -max_z
        angle = (angle + da * dt) % TAU
        dh += acceleration * dt
        height += dh * dt
        if height - radius < 0:
            height = radius
            dh = initial_v
        tree.show()
        tree.clear(update= False)

# Displays an analogue clock
def clock(duration = np.inf):
    start_time = time()
    # Aim to put center of clock here, at y = 0, with a large x-value
    center_z = tree.z_min + 0.35 * tree.z_range
    # All coordinates, with index appended on
    coords = np.hstack((tree.coordinates[:,0:3], np.reshape(np.arange(tree.n), (-1, 1))))
    # Sort by z distance from center_z, keep closest 5%
    coords[:,2] = abs(coords[:,2] - center_z)
    sort_order = np.argsort(coords[:,2])
    coords = coords[sort_order][:int(.05*len(coords))]
    # Side quest:  Find good radius
    sort_order = np.argsort(-abs(coords[:,1]))
    coords = coords[sort_order]
    radius = round(4/3*abs(tree[int(coords[5][3])].y), 2)
    # Sort by y distance from 0, keep closest 10
    coords[:,1] = abs(coords[:,1])
    sort_order = np.argsort(coords[:,1])
    coords = coords[sort_order][:10]
    # Sort by largest x-value, take largest 3
    sort_order = np.argsort(-coords[:,0])
    coords = coords[sort_order][:3]
    # Sort by y distance from 0 again, pick the best one
    sort_order = np.argsort(coords[:,1])
    center = tree[int(coords[sort_order][0][3])]
    # Calculate distances and angles from center
    dists = ((tree.y-center.y)**2 + (tree.z-center.z)**2)**0.5
    angles = np.arctan((tree.z - center.z) / (tree.y - center.y + .00001))
    angles[tree.y < center.y] += PI
    angles = angles % TAU
    old_colors = np.array([BLACK for _ in range(tree.n)])
    tree.clear(update= False)
    while time() - start_time < duration:
        new_colors = np.array([BLACK for _ in range(tree.n)])
        current_time = datetime.datetime.now()
        hour = current_time.hour % 12
        minute = current_time.minute
        second = current_time.second
        hour_angle = (-(hour*TAU/12 + minute*TAU/12/60 + second*TAU/12/60/60 - PI/2)) % TAU
        minute_angle = (-(minute*TAU/60 + second*TAU/60/60 - PI/2)) % TAU
        second_angle = (-(second*TAU/60 - PI/2)) % TAU
        m_hour = min(max(-np.tan(hour_angle), -15), 15)
        m_minute = min(max(-np.tan(minute_angle), -15), 15)
        m_second = min(max(-np.tan(second_angle), -15), 15)
        b_hour = -m_hour*center.y - center.z
        b_minute = -m_minute*center.y - center.z
        b_second = -m_second*center.y - center.z
        c_hour = (m_hour**2+1)**0.5
        c_minute = (m_minute**2+1)**0.5
        c_second = (m_second**2+1)**0.5
        if current_time.hour >= 12:
            new_colors[tree.z > 0.85 * tree.z_max] = BLUE
        frame = abs(dists - radius) < 0.1
        middle = dists < 0.05
        hour_hand = ((abs(m_hour*tree.y + tree.z + b_hour) / c_hour < 0.085)
                    & (dists < 0.6)
                    & (abs(angles - hour_angle) < 2))
        minute_hand = ((abs(m_minute*tree.y + tree.z + b_minute) / c_minute < 0.12)
                      & (dists < 0.7)
                      & (abs(angles - minute_angle) < 2))
        second_hand = ((abs(m_second*tree.y + tree.z + b_second) / c_second < 0.12)
                      & (dists < 0.7)
                      & (abs(angles - second_angle) < 2))
        new_colors[second_hand] = YELLOW
        new_colors[minute_hand] = GREEN
        new_colors[hour_hand] = BLUE
        new_colors[frame] = WHITE
        new_colors[middle] = RED
        different = np.where(new_colors != old_colors)[0]
        for i in different:
            tree[i].set_color(new_colors[i])
        old_colors = new_colors
        tree.show()

# Cylinders that grow tall then wide, then shrink
def cylinder(colors = COLORS, duration = np.inf):
    start_time = time()
    last_time = start_time
    if colors is None:
        pick_color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != np.ndarray or len(colors) < 3:
            print("Must supply at least 3 colors for this effect")
            return
        pick_color = lambda: rng.choice(colors)
    def new_color(c1, c2):
        next_color = pick_color()
        while np.array_equal(c1, next_color) or not contrast(c2, next_color): next_color = pick_color()
        return next_color
    color1 = pick_color()
    color2 = pick_color()
    while not contrast(color1, color2): color2 = pick_color()
    mid_z = tree.z_range / 2 + tree.z_min
    max_h = tree.z_range / 2
    max_r = 2**0.5
    min_r = max_r / 4
    r = min_r
    h = 0
    dh = 2
    dr = 1.25
    # Adds some pause between the transitions
    extra = .1
    min_h = 0 - extra * dh
    max_h += 3 * extra * dh
    max_r += extra * dr
    vertical = True
    # Used below, needs to be initialized here
    old_cylinder = np.array([])
    while time() - start_time < duration:
        dt = time() - last_time
        last_time = time()
        if vertical: # H is growing or shrinking
            h += dt*dh
            if h < min_h:
                dh = abs(dh)
                color1 = new_color(color1, color2)
            elif h > max_h:
                dh = -abs(dh)
                vertical = False
        else: # R is growing or shrinking
            r += dt*dr
            if r < min_r:
                r = min_r
                dr = abs(dr)
                vertical = True
            elif r > max_r:
                dr = -abs(dr)
                color2 = new_color(color2, color1)
        cylinder_new = ((tree.r <= r)
                    & (abs(tree.z - mid_z) <= h))
        cylinder_new = np.where(cylinder_new)[0]
        # new_cylinder is an optimization, adds about 6 fps
        new_cylinder = np.setdiff1d(cylinder_new, old_cylinder)
        background = np.setdiff1d(old_cylinder, cylinder_new)
        for i in new_cylinder:
            tree[i].set_color(color1)
        for i in background:
            tree[i].set_color(color2)
        old_cylinder = cylinder_new
        tree.show()

# Looks like a cylon's eyes
def cylon(color = RED, duration = np.inf):
    start_time = time()
    last_time = start_time
    pick_color = color_builder(color)
    color = pick_color()
    color = np.array([[130*k/np.linalg.norm(color) for k in color]])
    center = 0
    delta_c = 1.7
    while time() - start_time < duration:
        dt = time() - last_time
        last_time = time()
        center += delta_c*dt
        if center > tree.y_max:
            delta_c = -abs(delta_c)
            center += delta_c*dt
        if center < tree.y_min:
            delta_c = abs(delta_c)
            center += delta_c*dt
        dists = np.abs(tree.y - center)
        factors = np.maximum(1/13, -dists/.3 + 1)
        colors = factors.reshape(tree.n, 1) * color
        for i, pixel in enumerate(tree):
            pixel.set_color(colors[i])
        tree.show()

# Fades in and out
def fade(colors = TRADITIONAL_COLORS, midline = .7, amplitude = .7, speed = 1.5, duration = np.inf):
    # midline and amplitude define a sine function determining brightness as the light fades
    # It will reject a sine with a minimum below 0 or maximum above 1
    start_time = time()
    pick_color = color_builder(colors)
    amplitude = abs(amplitude)
    if midline < 0 or midline > 1 or amplitude > midline:
        print("Midline must be between 0 and 1, amplitude cannot be larger than midline")
        return
    pre_fade_buffer = np.concatenate([pick_color() for _ in range(tree.n)])
    while time() - start_time < duration:
        # f is factor, varies sinusoidally
        f = max(0, min(1, midline + amplitude * np.sin(speed * time())))
        if f <= 0.003:
            pre_fade_buffer = np.concatenate([pick_color() for _ in range(tree.n)])
        tree.set_colors(pre_fade_buffer * f)
        tree.show()

# Randomly restores lights to full brightness while constantly fading
def fade_restore(colors = TRADITIONAL_COLORS, p = 0.95, halflife = 0.3, duration = np.inf):
    start_time = time()
    last_time = start_time
    pick_color = color_builder(colors)
    color_buffer = np.array([pick_color() for _ in range(tree.n)])
    while (t := time()) - start_time < duration:
        dt = t - last_time
        last_time = t
        # p is probability of each light restoring per second
        # exp adjusts this to work with dt seconds
        exp = (1-p)**dt
        tree.fade(halflife = halflife, dt = dt)
        renew = np.where(rng.random(tree.n) >= exp)[0]
        for i in renew:
            tree[i].set_color(color_buffer[i])
        tree.show()

# Courtesy of Nekisha
# Colors fall down from above
def falling_colors(colors=None, duration = np.inf):
    if colors is None:
        colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE]
    start_time = time()
    last_time = start_time
    colors = np.array(colors)
    color_density = 2.4 # Number of colors displayed at once
    # height of all colors stacked together
    height = len(colors)/color_density*tree.z_range
    # moving height that pixels are colord with respect to
    h = tree.z_max
    fall_speed = .35 # units/second
    fuzz_factor = .25 # 0 for a sharp barrier between colors.  Larger it is from there, the fuzzier the barrier becomes.  Starts glitching after 1.
    fuzzed_z = tree.z + fuzz_factor * np.random.uniform(-1, 1, tree.n)
    while time() - start_time < duration:
        dt = time() - last_time
        last_time = time()
        h -= fall_speed * dt
        indices = (len(colors)*((fuzzed_z - h) % height)/height).astype(np.int32)
        tree.set_colors(colors[indices].flatten())
        tree.show()

# Meant to imitate a fire
def fire(duration = np.inf):
    #return # Currently bugged, needs fixing - optimizing?
    start_time = time()
    last_time = start_time
    one = np.array([75, 55, 0])
    two = np.array([75, 10, 0])
    two_one = two - one
    tree.flags = np.full(tree.n, 0, dtype=object)
    def flag_neighbors(flame_part):
        for neighbor in flame_part.neighbors:
            neighbor = tree[neighbor]
            if neighbor.z < flame_part.z and ((neighbor.x - flame_part.x) ** 2 + (neighbor.y - flame_part.y) ** 2) < .008:
                neighbor.flag = flame_part.flag - 1
                if neighbor.flag > 1: flag_neighbors(neighbor)
    smoke_c = np.array([5, 5, 5])
    while time() - start_time < duration:
        dt = time() - last_time
        last_time = time()
        tree.fade(halflife = 0.05, dt = dt)
        if rng.random() < .2:
            flames = rng.choice(tree.pixels, 20)
            for i, flame in enumerate(flames):
                if flame.z > 0.75*tree.z_max or (flame.z > 0.5 * tree.z_max and rng.random() < .6):
                    continue
                flame.flag = 20
                print(1)
                flag_neighbors(flame)
                print(2)
        smoke = np.where((tree.z > 0.65 * tree.z_max) & (rng.random(tree.n) < 0.1))[0]
        one_two_one = np.where(tree.z < 1.1*np.cos(0.5*PI*tree.x)*np.cos(0.5*PI*tree.y) + 0.3)[0]
        for i in smoke:
            tree[i].set_color(smoke_c)
        for i in one_two_one:
            tree[i].set_color(one + two_one * rng.random())
        for pixel in tree:
            if pixel.i in smoke or pixel.i in one_two_one:
                continue
            if pixel.flag > 0:
                if True:#rng.random() < 0.9:
                    pixel.set_color(RED)
                else:
                    pixel.set_color(ORANGE)
                pixel.flag -= 6
        tree.show()

# Creates a gradient between all the colors specified
# Can soften or harden the gradient if desired
def gradient(colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
             , softness = 2, variant = 3, normalize = False, indices = None):
    if colors is None:
        pick_color = lambda: rng.integers(0, 256, 3)
        color1 = pick_color()
        color2 = contrast_color(color1, pick_color)
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
    def pick_color(x):
        factors = []
        for k in range(n):
            if abs(x - k/n) < width:
                factor = 0.5*np.cos(p*(x - k/n)) + 0.5
            elif (k/n > x) and (k/n + width > 1) and (((k/n + width) % 1) > x):
                factor = 0.5*np.cos(p*(x + 1 - k/n)) + 0.5
            elif (k/n < x) and (k/n - width < 0) and (((k/n - width) % 1) < x):
                factor = 0.5*np.cos(p*(x - 1 - k/n)) + 0.5
            else:
                factor = 0
            factors.append(factor)
        factors = np.array(factors)
        if normalize:
            # Normalize the factors so they add to 1
            factor_sum = max(1, np.sum(factors))
            factors = factors / factor_sum
        color = colors * factors.reshape(n, -1)
        color = np.sum(color, axis = 0)
        if not normalize:
            # Normalize the color so its brightest component is 255
            max_c = np.max(color)
            color = 255 * color / max_c
        return color.astype(np.uint8)
    if indices is None:
        indices = tree.indices[variant]
    for i, j in enumerate(indices):
        tree[j].set_color(pick_color(i / (tree.n - 1)))
    tree.show()

# Displays the images in sequence, requires keyboard input
def image_slideshow():
    for image in Path('/home/pi/Desktop/TreeLights/Images/').iterdir():
        display_image(image)
        input()
        display_image2(image)
        print(image[:-4])
        input()
    tree.clear()

# All blue, flickers random lights white, like twinkling stars
def night_sky(duration = np.inf):
    start_time = time()
    last_time = start_time
    flicker_length = 0.2 # seconds
    p = 0.07 # probability per light per second
    twinkle_times = np.zeros(tree.n)
    tree.fill(BLUE)
    while (t := time()) - start_time < duration:
        dt = t - last_time
        last_time = t
        twinkle_times -= dt
        twinkle_lights = (twinkle_times <= 0) & (rng.random(tree.n) > (1-p)**dt)
        twinkle_times[twinkle_lights] = flicker_length
        twinkle_on = np.where(twinkle_lights)[0]
        twinkle_off = np.where((-dt < twinkle_times) & (twinkle_times < 0))[0]
        for i in twinkle_on:
            tree[i].set_color(WHITE)
        for i in twinkle_off:
            tree[i].set_color(BLUE)
        tree.show()

# A growing and shrinking spear that moves up and down and changes colors
def pulsating_sphere(colors = None, dr = 0.7, dh = 0.3, duration = np.inf):
    start_time = time()
    last_time = start_time
    pick_color = color_builder(colors)
    color1 = pick_color()
    color2 = BLACK
    while not contrast(color1, color2): color2 = pick_color()
    height = 0.45 * tree.z_max + 0.1 * rng.random()
    min_h = tree.z_min
    max_h = tree.z_max
    max_r = .75*tree.r_max
    min_r = 0
    r = min_r
    while time() - start_time < duration:
        dt = time() - last_time
        last_time = time()
        if r <= min_r:
            dr = abs(dr)
            color1 = color2
            while not contrast(color1, color2): color1 = rng.choice(COLORS)
        elif r > max_r:
            dr = -abs(dr)
        if height - r < min_h:
            dh = abs(dh)
            height = min_h + r
        elif height + r > max_h:
            dh = -abs(dh)
            height = max_h - r
        ball = ((tree.x**2 + tree.y**2 + (tree.z - height)**2) <= (r**2))
        bg = np.where(np.logical_not(ball))[0]
        ball = np.where(ball)[0]
        for i in ball:
            tree[i].set_color(color1)
        for i in bg:
            tree[i].set_color(color2)
        r += dr * dt
        height += dh * dt
        tree.show()

# A raining effect
def rain(colors = CYAN, speed = 5, wind = -4, drop_count = 8, accumulation_speed = 0, do_fade = True, duration = np.inf):
    start_time = time()
    last_time = start_time
    if len(colors.shape) == 1:
        colors = np.array(colors)
    width = 0.12
    height = 0.15
    floor = tree.z_min - 0.1
    new_drop = lambda bottom: [rng.random() * TAU, rng.random() * (tree.z_max - bottom) + tree.z_max, rng.choice(colors)]
    drops = [new_drop(floor) for _ in range(drop_count)]
    while time() - start_time < duration:
        dt = time() - last_time
        last_time = time()
        for i in range(len(drops) - 1, -1, -1):
            drops[i][1] -= speed*dt
            drops[i][0] = (drops[i][0] + wind*dt) % TAU
            if drops[i][1] < floor:
                del drops[i]
                drops.append(new_drop(floor))
                continue
            wet = np.where((tree.z < floor) | (tree.s & (np.abs(tree.a - drops[i][0]) < width) & (abs(tree.z - drops[i][1]) < height)))[0]
            for j in wet:
                tree[j].set_color(drops[i][2])
        floor += accumulation_speed * dt
        if floor >= tree.z_max: floor = 0
        tree.show()
        if do_fade:
            tree.fade(halflife = 0.125, dt = dt)

def test_mod(duration = np.inf):
    start_time = time()
    last_time = start_time
    set_all(WHITE)
    mod = 20
    m = 1
    width = 3
    speed = 1/200
    next_time = speed
    d_mod = 0
    max_mod = np.inf
    color1 = rng.choice([OFF])
    color2 = rng.choice([WHITE])
    while time() - start_time < duration:
        dt = time() - last_time
        last_time = time()
        next_time -= dt
        if next_time <= 0:
            next_time = speed
        else:
            continue
        for pixel in tree:
            if ((pixel.i - m) % mod) < width:
                pixel.set_color(color1)
            else:
                pixel.set_color(color2)
        tree.show()
        mod += d_mod
        if mod < 1:
            mod = 1
            d_mod = abs(d_mod)
            color2 = rng.choice(COLORS)
            while np.all(color2 == color1):
                color2 = rng.choice(COLORS)
        if mod > max_mod:
            mod = max_mod
            d_mod = -abs(d_mod)
            color1 = rng.choice(COLORS)
            while np.all(color1 == color2):
                color1 = rng.choice(COLORS)
        m = (m + 1) % mod

# Random colored planes fly through the tree, leaving trails
def random_planes(colors = COLORS, duration = np.inf):
    start_time = time()
    last_time = start_time
    pick_color = color_builder(colors)
    z = 10
    max_z = 0
    speed, new_coords, color, factor = None, None, None, None
    while time() - start_time < duration:
        dt = time() - last_time
        last_time = time()
        if z > max_z + 1.5:
            angle_z = rng.uniform(0, TAU)
            angle_x = rng.uniform(0, PI)
            new_coords = transform(tree.coordinates[:,0:3], xr = angle_x, zr = angle_z)
            min_z = np.min(new_coords[:,2])
            max_z = np.max(new_coords[:,2])
            # Take 2.5 seconds per plane
            # Intentionally go off-tree a bit to give the fade time to fade more
            speed = (max_z + 1.5 - min_z)/2.5
            z = min_z
            factor = rng.uniform(0, .15) # Randomized fade speed
            color = pick_color()
        z_step = speed * dt
        z += speed*dt
        plane = np.where(np.abs(new_coords[:,2] - z) < z_step)[0]
        for i in plane:
            tree[i].set_color(color)
        tree.show()
        tree.fade(halflife = factor, dt = dt)

# Plays the game "snake"
def snake(cycles = np.inf, duration = np.inf):
    start_time = time()
    cycle = 0
    while time() - start_time < duration and cycle < cycles:
        tree.clear(update= False)
        body = [rng.choice(tree)]
        pellet = rng.choice(tree)
        visited = [body[0]] # Prevents loops
        while time() - start_time < duration:
            if body[0] == pellet: # Snake got the food
                body += [body[-1]] # Grow longer
                while pellet in body: pellet = rng.choice(tree) # Place new food
                visited = [body[0]]
            destination = None # Where will the snake go?
            for neighbor in body[0].neighbors:
                # If the neighbor isn't part of the snake
                # and there either isn't a destination yet
                    # or this neighbor is closer to the pellet than the current destination
                neighbor = tree[neighbor]
                if neighbor == pellet:
                    destination = neighbor
                    break
                elif (neighbor not in body
                        and (destination is None
                             or np.linalg.norm(pellet.coordinate - neighbor.coordinate) < np.linalg.norm(pellet.coordinate - destination.coordinate))):
                    pattern = visited[-1:] + [neighbor]
                    if any(visited[i:i+len(pattern)] == pattern for i in range(len(visited) - len(pattern))):
                        # Avoid loops
                        continue
                    free_spots = 0
                    for neigh in neighbor.neighbors:
                        if tree[neigh] not in body: free_spots += 1
                    if free_spots >= 1: destination = neighbor
            if destination is None: # No valid spots to move to
                break # Snake dies of starvation
            body = [destination] + body
            visited.append(body[0])
            body[-1].setColor(OFF) # Turn the tail off then remove it
            body.pop()
            for i in range(len(body)):
                f = i / len(body)
                if i == 0:
                    body[i].setColor(WHITE)
                else: # Rainbow colors
                    body[i].setColor([max(510*(abs(f-0.5) - 1/6), 0), max(765*(-abs(f-1/3)+1/3), 0), max(765*(-abs(f-2/3)+1/3), 0)])
            pellet.set_color(WHITE)
            tree.show()
            sleep(0.05)
        for i in range(3): # Death animation
            for segment in body:
                segment.setColor(RED)
            tree.show()
            sleep(0.5)
            for segment in body:
                segment.setColor(OFF)
            tree.show()
            sleep(0.5)
            cycle += 1

# Rotates a plane about some axis
def spinning_plane(colors = COLORS, variant = 0, speed = 4, width = 0.15, height = tree.z_mid
                   , two_colors = False, background = False, spinner = False, duration = np.inf):
    start_time = time()
    last_time = start_time
    pick_color = color_builder(colors)
    color1 = pick_color()
    color2 = contrast_color(color1, pick_color)
    colors = [color1, color2]
    if spinner: background, two_colors = True, True
    colors += [[[0.04, 1][spinner] * k for k in colors[0]], [[0.04, 1][spinner] * k for k in colors[1]]]
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
    else:#elif variant == 3: # Axis of rotation is random
        theta = rng.random() * TAU
        phi = rng.random() * PI
    t = 0
    while (tt := time()) - start_time < duration:
        dt = tt - last_time
        last_time = tt
        new_coords = transform(tree.coordinates[:,0:3], z = -height, zr = -theta, xr = t, yr = PI/2 - phi)
        for i, coord in enumerate(new_coords):
            if abs(coord[2]) < width:
                if two_colors:
                    if coord[2] >= 0:
                        tree[i].set_color(colors[0])
                    else:
                        tree[i].set_color(colors[1])
                else:
                    tree[i].set_color(colors[0])
            else:
                if background:
                    if two_colors:
                        if coord[2] >= 0:
                            tree[i].set_color(colors[2])
                        else:
                            tree[i].set_color(colors[3])
                    else:
                        tree[i].set_color(colors[2])
                else:
                    tree[i].set_color(OFF)
        t += speed * dt
        tree.show()

# Makes spirals
def spirals(colors=None
            , variant = 1, spin_count = 2, z_speed = 1, spin_speed = -2, surface = False, offset = 0
            , skip_black = True, generate_instantly = False, generate_together = False, end_after_spirals = False
            , pre_clear = True, post_clear = False, spin_after_done = False
            , duration = np.inf, cycles = 1):
    if colors is None:
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    start_time = time()
    last_time = start_time
    colors = np.array(colors)
    if variant**2 != 1: # variant determines which way the spirals slope.  1 = positive slope, -1 = negative slope
        print("variant must be 1 or -1")
        return
    done = generate_instantly
    spiral_count = len(colors) # Number of spirals
    section_h = tree.z_range / spin_count # Works in sections of one spin each to make things simpler
    d_theta = -TAU / spiral_count # theta gives the initial angle for the current spiral, d_theta is the angle difference between each spiral
    spiral_h = section_h / spiral_count # Vertical height of each spiral
    spiral_dist_between_tops = spiral_count * spiral_h # Vertical distance between top of the same spiral at corresponding points 2π radians apart
    cycle, angle_offset, z = 0, 0, 0
    # Set spiral to first non-black spiral
    spiral = np.argmax(np.all(colors == OFF))
    # Precomputing some values because this function sometimes lags
    m1 = section_h / TAU
    m2 = -TAU / section_h
    m2sp1 = m2**2 + 1
    tree.flags = np.array([None, section_h*(tree.z // section_h)], dtype=object)
    np_spirals = np.array([[i] for i in range(spiral_count)])
    np_spirals = (np_spirals + 1)*d_theta
    while (t := time()) - start_time < duration:
        dt = t - last_time
        last_time = t
        if pre_clear or spin_speed != 0:
            tree.fill(OFF)
        angle = (tree.a + angle_offset + offset) % TAU
        m = ((tree.z % section_h - variant*angle*section_h/TAU) // spiral_h) % spiral_count
        m = m.astype(np.int32)
        draw_now = ((generate_instantly | done | (m < spiral))
                   & ((not generate_together) or done)
                   & ((not surface) | tree.s)
                   & (skip_black & ~np.all(colors[m] == BLACK, axis=1)))
        draw_now = np.where(draw_now)[0]
        for i in draw_now:
            tree[i].set_color(colors[m[i]])
        if not generate_instantly and not done:
            np_angle = (variant * (tree.a + angle_offset) - np_spirals) % TAU
            np_top_of_spiral = m1*np_angle + section_h * (tree.z // section_h)
            np_angle += TAU * (((tree.z - m1*np_angle) // section_h) + 1)
            np_spiral_edge = m2*np_angle + m2sp1*z
            for spi in range(*[[spiral, spiral + 1], [spiral_count]][generate_together]):
                condition = ((tree.z < np_spiral_edge[spi])
                             & (((tree.z <= np_top_of_spiral[spi])
                                 & (tree.z > np_top_of_spiral[spi] - spiral_h))
                                | ((tree.z <= np_top_of_spiral[spi] + spiral_dist_between_tops)
                                   & (tree.z > np_top_of_spiral[spi] + spiral_dist_between_tops - spiral_h)))
                             & ((not surface) | tree.s))
                condition = np.where(condition)[0]
                for i in condition:
                    tree[i].set_color(colors[m[i]])
        tree.show()
        if not spin_after_done or done: angle_offset = (angle_offset + spin_speed * dt) % TAU
        if generate_instantly or done:
            if end_after_spirals:
                if post_clear: tree.clear(update= False)
                return
            continue
        if z <= tree.z_range + spiral_h: z += z_speed * dt # Mid-stripe, increase z and continue
        else: # Stripe is complete
            z = 0 # Reset z
            if spiral < spiral_count: # If we aren't done
                spiral += 1 # Then move on to the next stripe
                while spiral < spiral_count and skip_black and np.array_equal(colors[spiral], OFF): # Option to skip black because it just keeps the pixels off
                    if spiral < spiral_count - 1: # Keep skipping as long as they're black
                        spiral += 1
                    else:
                        spiral += 1
                        break # Rest of spirals were black - jumps into below if statement to complete the cycle
            if spiral >= spiral_count or generate_together: # Not an else statement because above while loop can trigger this code too
                cycle += 1 # Otherwise start the next cycle
                if cycle >= cycles: # Unless that was the last cycle
                    done = True # In which case we're done drawing spirals and just spin
                    if end_after_spirals:
                        if post_clear: tree.clear(update= False)
                        return # Or done entirely if that flag was set
                else:
                    spiral = 0 # If that wasn't the last cycle, start the drawing process over

# Has a circle wander around the tree
def spotlight(colors = [WHITE, BLUE], duration = np.inf):
    start_time = time()
    last_time = start_time
    if colors is None:
        color1 = rng.integers(0, 256, 3)
        color2 = rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != np.ndarray:
            print("Must supply at least two colors")
            return
        color1, color2 = colors[0], colors[1]
    radius = 0.45 # Of the spotlight
    dz_max = 2.5
    d_theta_max = 4
    z = rng.uniform(0, 0.6 * tree.z_max) # Spotlight's initial z-coordinate
    dz = rng.uniform(-dz_max, dz_max) # units/second
    theta = rng.uniform(0, TAU) # Spotlight's initial angle around z-axis
    d_theta = rng.uniform(-d_theta_max, d_theta_max) # radians/second
    # m and b used to calculate point on tree's surface from z and theta
    m = tree.x_max / (tree[tree.sorted_x[-1]].z - tree[tree.sorted_z[-1]].z)
    b = -m * tree[tree.sorted_z[-2]].z
    while (t := time()) - start_time < duration:
        dt = t - last_time
        last_time = t
        z += dz * dt
        theta += d_theta * dt
        if z + radius > tree.z_max:dz = -abs(dz)
        if z - radius < 0: dz = abs(dz)
        point = [(m*z+b)*np.cos(theta), (m*z+b)*np.sin(theta)] + [z] # On or near surface of tree
        light = tree.s & (((tree.x - point[0])**2 + (tree.y - point[1])**2 + (tree.z - point[2])**2) < radius**2)
        bg = np.where(np.logical_not(light))[0]
        light = np.where(light)[0]
        for i in light:
            tree[i].set_color(color1)
        for i in bg:
            tree[i].set_color(color2)
        dz = min(dz_max, max(-dz_max, dz + rng.uniform(-.5, .5)))
        d_theta = min(d_theta_max, max(-d_theta_max, d_theta + rng.uniform(-2.2, 2.2)))
        tree.show()

# Sweeps colors around the tree
def sweep(colors = COLORS, speed = 5, clockwise = False, alternate = True, duration = np.inf):
    start_time = time()
    last_time = start_time
    pick_color = color_builder(colors)
    color = pick_color()
    new_color = pick_color()
    speed = abs(speed)
    angle = 0
    while (t := time()) - start_time < duration:
        dt = t - last_time
        last_time = t
        angle += speed * dt
        if angle >= TAU + speed: # Adding speed adds 1-second delay
            if alternate: clockwise = not clockwise
            angle = 0
            while not contrast(new_color, color): new_color = pick_color()
            color = new_color
        if clockwise:
            front = np.where(np.abs(tree.a - angle) <= speed*dt)[0]
        else:
            front = np.where(np.abs(TAU - tree.a - angle) <= speed*dt)[0]
        for i in front:
            tree[i].set_color(color)
        tree.show()

# Sweeps around the tree continuously and smoothly changing colors
def sweeper(colors = COLORS[1:], speed = 5, sequence = True, duration = np.inf):
    start_time = time()
    last_time = start_time
    if sequence:
        pick_color = lambda k = None: colors[((np.where(np.all(colors == k, axis = 1))[0][0] + 1) % len(colors))]
    else:
        pick_color = color_builder(colors)
    if sequence:
        old_color = colors[0]
        next_color = colors[1]
    else:
        old_color = pick_color()
        next_color = pick_color()
        while not contrast(next_color, old_color): next_color = pick_color()
    angles = tree.a
    if speed < 0:
        speed = abs(speed)
        angles = TAU - angles
    angle = 0
    while (t := time()) - start_time < duration:
        dt = t - last_time
        last_time = t
        angle += speed * dt
        if angle > TAU:
            angle = 0
            old_color = next_color
            if sequence:
                next_color = pick_color(old_color)
            else:
                while not contrast(next_color, old_color): next_color = pick_color()
        color = old_color + (angle/TAU)*(next_color - old_color)
        front = np.where(np.abs(angles - angle) <= speed*dt)[0]
        for i in front:
            tree[i].set_color(color)
        tree.show()

# Sets all LEDs randomly then lets their brightness vary
def twinkle(colors = TRADITIONAL_COLORS, intensity = 1.8, length = .3, p = 0.04, duration = np.inf):
    start_time = time()
    last_time = start_time
    colors = np.array(colors)
    factor = 255 / np.max(intensity * colors)
    if factor < 1:
        colors = (factor * colors).astype(np.uint8)
    set_all_random(colors)
    buffer = np.array(tree._pre_brightness_buffer)
    intensity -= 1
    tree.flags = np.full(tree.n, 0.0)
    while (t := time()) - start_time < duration:
        dt = t - last_time
        last_time = t
        # Negative flags are inactive and regular brightness
        # Randomly set lights to length to activate twinkle
        # Brightness increases, peaks, decreases, and hits regular again as flag decreases to 0 and below
        tree.flags -= dt
        tree.flags[((tree.flags <= 0) & (np.random.rand(tree.n) < p))] = length
        active_lights = (tree.flags > 0)
        f = np.full(tree.n, 1.0)
        f[active_lights] = (1 + intensity * (1 - np.abs(2*tree.flags[active_lights]/length - 1)))
        f = np.column_stack((f, f, f)).flatten()
        new_buffer = buffer * f
        tree.set_colors(new_buffer)
        tree.show()

# Has all LEDs let their color wander around at random
def wander(colors = COLORS, wander_time = 1, variance = None, duration = np.inf):
    start_time = time()
    last_time = start_time
    pick_color = color_builder(colors)
    if variance is None:
        variance = wander_time / 5
    # Start with colors the tree already has, for nice fade-in effect
    old_colors = np.array([pixel.color for pixel in tree])
    color_buffer = old_colors
    new_colors = np.array([pick_color() for _ in range(tree.n)])
    lengths = np.array([rng.uniform(wander_time - variance, wander_time + variance) for _ in range(tree.n)])
    # Add variance to the initial lengths so they aren't synchronized. This is done to avoid lag.
    lengths = lengths + rng.random(tree.n) * wander_time
    times = np.full(tree.n, time())
    while (t := time()) - start_time < duration:
        dt = t - last_time
        last_time = t
        elapsed_times = t - times
        expired_lights = elapsed_times > lengths
        if (expiredLen := len(np.where(expired_lights)[0])) > 0:
            old_colors[expired_lights] = color_buffer[expired_lights]
            new_colors_temp = [pick_color() for _ in range(expiredLen)]
            new_colors[expired_lights] = new_colors_temp
            times[expired_lights] = t - dt
            elapsed_times[expired_lights] = dt
            lengths[expired_lights] = [rng.uniform(wander_time - variance, wander_time + variance) for _ in range(expiredLen)]
        f = np.array([elapsed_times / lengths])
        color_buffer = old_colors + f.T * (new_colors - old_colors)
        tree.set_colors(color_buffer.flatten())
        tree.show()

# Draws spirals and winds them up
def winding_spirals(colors=None, max_spin_count = 4, d_spin = 3, d_offset = 1, duration = np.inf):
    if colors is None:
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    start_time = time()
    last_time = start_time
    variant = 1
    spin_count = 0.01
    offset = 0
    while (t := time()) - start_time < duration:
        dt = t - last_time
        last_time = t
        spirals(colors = colors, variant = variant, spin_count= spin_count, generate_instantly= True, offset = offset, end_after_spirals= True)
        spin_count += d_spin * dt
        offset += d_offset * dt
        if spin_count > max_spin_count:
            d_spin = -abs(d_spin)
            spin_count += d_spin * dt
        if spin_count <= 0.01:
            d_spin = abs(d_spin)
            spin_count = 0.01
            variant *= -1
            colors.reverse()

# Spirals out from the tree's z-axis, in rainbow colors
def z_spiral(twists = 8, speed = TAU, backwards = True, duration = np.inf, cycles = np.inf):
    start_time = time()
    last_time = start_time
    # Finds the angle of each light in the correct section of spiral - so going beyond TAU
    # Makes sense if you diagram it out: x-axis from 0 to 2PI, y-axis from 0 to tree.rMax, plot spiral
    # Fully simplified
    angles = tree.a + TAU * np.ceil(twists * tree.r / tree.r_max - tree.a / TAU)
    if backwards:
        angles = (TAU-tree.a) + TAU * np.ceil(twists * tree.r / tree.r_max - (TAU - tree.a) / TAU)
    # Use of the following 3 variables is mostly to make sure red definitely shows up
    # Not certain otherwise as Color is only red for very small and very large angles
    a_min = np.min(angles)
    a_max = np.max(angles)
    a_range = a_max - a_min
    # Color is intentionally basd on angle around spiral instead of radius, even though
    # the two are very similar and radius is way easier to calculate
    # This is because it creates a nice shimmer effect when run through the radial cycle after
    pick_color = lambda a: [255 * max(min( 3*abs(a/a_range - 0.5) - 0.5, 1), 0),
                       255 * max(min(-3*abs(a/a_range - 1/3) + 1.0, 1), 0),
                       255 * max(min(-3*abs(a/a_range - 2/3) + 1.0, 1), 0)]
    colors = [pick_color(a - a_min) for a in angles]
    tree.clear(update= False)
    angle = 0
    done = 0
    cycle = 0
    while cycle < cycles and (t := time()) - start_time < duration:
        dt = t - last_time
        last_time = t
        angle += dt*speed
        # Find lights between current and previous angle
        angle_diffs = angle - angles
        new_lights = np.where((angle_diffs <= dt*speed) & (angle_diffs > 0))[0]
        for i in new_lights:
            tree[i].set_color(colors[i])
        done += len(new_lights)
        tree.show()
        if done == tree.n:
            cycle += 1
            angle = 0
            done = 0
            if cycle != cycles:
                tree.clear(update= False)
