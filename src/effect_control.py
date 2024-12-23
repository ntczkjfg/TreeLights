from common_variables import rng, tree, PI, TAU
from colors import *
import numpy as np
from dynamic_effects import (alternating_stripes, blink, bouncing_rainbow_ball, clock, cylinder,
                             cylon, fade, fade_restore, falling_colors, fire, pulsating_sphere, rain,
                             random_planes, snake, spinning_plane, spirals, spotlight, sweep,
                             sweeper, twinkle, wander, winding_spirals, z_spiral, gradient, night_sky)
from simple_effects import pizza, traffic_cone, random_fill, candy_corn, set_all, set_all_random
from time import time, sleep

# When the tree first receives power, lights sometimes turn on randomly - clear to fix
tree.clear()
tree.clear()

def fps(func, name):
    print(f"{name}: ", end = "")
    tree.frames = 0
    start_time = time()
    func()
    duration = time() - start_time
    print(f"{tree.frames} frame{'s' if tree.frames != 1 else ''} in {round(duration, 2)} seconds for {round(tree.frames/duration, 1)} fps{'*' if tree.frames == 1 else ''}")
    tree.clear(flags_only= True)

# Puts on a curated show of effects
def show(effects = None, duration = 30, insequence = False, start = 0):
    old_effect = 0
    effect = start
    cycles = 1
    effect_count = 34
    if effects is None:
        effects = [i for i in range(1, effect_count + 1)]
    if type(effects) == int:
        effects = [effects]
    while True:
        if insequence:
            effect += 1
            if effect > effect_count:
                effect = 1
        else:
            if len(effects) > 1:
                while effect == old_effect: effect = rng.choice(effects)
            else:
                effect = effects[0]
        old_effect = effect
        # cylinder
        if effect == 1:
            colors = [[[200, 30, 30], CYAN, PURPLE]
                      , [[0, 10, 90], [5, 90, 5], [70, 15, 15]]][rng.integers(0, 2)]
            stripe_count = rng.choice([2, 2, 2, 2, 3, 3, 3, 4, 4])
            spin_speed = rng.choice([-1, 1]) * rng.uniform(PI/4, PI)
            func = lambda: alternating_stripes(*colors, stripe_count= stripe_count, spin_speed= spin_speed, duration = duration)
            fps(func, "alternating_stripes")
        # blink
        elif effect == 2:
            colors = [TRADITIONAL_COLORS, COLORS, TREE_COLORS, None, rng.choice(COLORS)][rng.integers(5)]
            group_count = rng.integers(5, 15)
            if rng.random() < 0.3:
                group_count = rng.integers(50, 400)
            p = rng.uniform(0.5, 0.85)
            delay = rng.uniform(0.3, 0.7)
            func = lambda: blink(colors = colors, group_count= group_count, delay = delay, p = p, duration = duration)
            fps(func, "blink")
        # bouncingRainbowBall
        elif effect == 3:
            func = lambda: bouncing_rainbow_ball(duration =3 * duration)
            fps(func, "bouncingRainbowBall")
        # clock
        elif effect == 4:
            func = lambda: clock(duration = duration)
            fps(func, "clock")
        # cylinder
        elif effect == 5:
            colors = [COLORS, TRADITIONAL_COLORS, TREE_COLORS, None, TREE_COLORS_2, RAINBOW][rng.integers(6)]
            func = lambda: cylinder(colors = colors, duration = 3*duration)
            fps(func, "cylinder")
        # cylon
        elif effect == 6:
            variant = rng.integers(1, 5)
            color = RED if variant < 4 else COLORS
            func = lambda: cylon(color = color, duration = duration)
            fps(func, "cylon")
        # fade
        elif effect == 7:
            colors = [TRADITIONAL_COLORS, COLORS, TREE_COLORS, TREE_COLORS_2, None, rng.choice(COLORS)][rng.integers(6)]
            midline = rng.uniform(.3, .7) # This is also the maximum value of amplitude
            amplitude = min(rng.uniform(midline/2, 1.1*midline), midline) # Give it a 20% chance of maxing out
            speed = rng.uniform(1, 2.5)
            func = lambda: fade(colors = colors, midline = midline, amplitude = amplitude, speed = speed, duration = 2*duration)
            fps(func, "fade")
        # fadeRestore
        elif effect == 8:
            colors = [TRADITIONAL_COLORS, COLORS, TREE_COLORS, TREE_COLORS_2, None, rng.choice(COLORS)][rng.integers(5)]
            p = rng.uniform(.8, .98)
            halflife = rng.uniform(.1, .5)
            func = lambda: fade_restore(colors = colors, p = p, halflife = halflife, duration =2 * duration)
            fps(func, "fadeRestore")
        # fallingColors
        elif effect == 9:
            func = lambda: falling_colors(duration =3 * duration)
            fps(func, "fallingColors")
        # fire
        elif effect == 10:
            func = lambda: fire(duration = 3*duration)
            fps(func, "fire")
        # pulsatingSphere
        elif effect == 11:
            colors = [None, COLORS, RAINBOW][rng.integers(3)]
            d_r = rng.uniform(0.5, 0.9)
            d_h = rng.uniform(0.2, 0.4)
            func = lambda: pulsating_sphere(colors = colors, dr= d_r, dh= d_h, duration =3 * duration)
            fps(func, "pulsatingSphere")
        # rain
        elif effect == 12:
            variant = rng.integers(0, 6)
            if variant < 2: # Regular rain
                color = [CYAN, BLUE][variant]
                accumulation_speed = 0
                wind = rng.uniform(-6, 6)
                speed = rng.uniform(3, 9)
                do_fade = True
                name = "rain"
            elif variant < 3: # Like the matrix
                color = GREEN
                accumulation_speed = 0
                wind = 0
                speed = 3
                do_fade = True
                name = "matrixTrails"
            elif variant < 4:
                color = COLORS
                wind = rng.uniform(-5, 5)
                speed = rng.uniform(3, 9)
                do_fade = rng.choice([True, False])
                name = 'colorful_rain'
            else: # Accumulating snow
                color = WHITE
                accumulation_speed = 0.03
                wind = 0
                speed = 2
                do_fade = True
                name = "accumulatingSnow"
            drop_count = rng.integers(8, 14)
            func = lambda: rain(colors = color, drop_count= drop_count, accumulation_speed= accumulation_speed, wind = wind, speed = speed, do_fade= do_fade, duration =2 * duration)
            fps(func, name)
        # randomPlanes
        elif effect == 13:
            colors = [None, COLORS, RAINBOW][rng.integers(3)]
            func = lambda: random_planes(colors = colors, duration =3 * duration)
            fps(func, "randomPlanes")
        # snake
        elif effect == 14:
            if duration < 10:
                d = duration
            else:
                d = np.inf
            func = lambda: snake(duration = d, cycles = cycles)
            fps(func, "snake")
        # spinning_plane
        elif effect == 15:
            if rng.random() < 0.5:
                colors = [None, COLORS, RAINBOW, [WHITE, BLUE], [RED, GREEN], [CYAN, WHITE], [GREEN, BLUE], [BLUE, YELLOW], [YELLOW, PURPLE], [PURPLE, GREEN]][rng.integers(10)]
                speed = rng.uniform(2, 7)
                width = rng.uniform(0.1, 0.3)
                height = rng.choice([0, 0, tree.z_max / 2, tree.z_max / 2, tree.z_max / 2, tree.z_max / 2, tree.z_max / 2, tree.z_max])
                # Higher speeds are jarring at these heights
                if height == 0 or height == tree.z_max: speed = rng.uniform(2, 3.5)
                two_colors = rng.choice([True, False, False])
                background = rng.choice([True, True, False])
                spinner = False
                name = "spinning_plane"
            else:
                colors = [[WHITE, BLUE], [RED, GREEN], [CYAN, WHITE], [GREEN, BLUE], [BLUE, YELLOW], [YELLOW, PURPLE], [PURPLE, GREEN]][rng.integers(7)]
                if rng.random() < 0.2: colors[rng.integers(2)] = OFF
                speed = rng.uniform(2, 9)
                height, width = tree.z_mid, 0.15
                spinner, two_colors, background = True, False, False
                name = "spinner"
            variant = rng.choice([0, 0, 0, 1, 2, 2, 2, 3])
            func = lambda: spinning_plane(colors = colors, variant = variant, speed = speed, spinner= spinner
                                          , two_colors= two_colors, background= background, height = height
                                          , width = width, duration = duration)
            fps(func, name)
        # spirals
        elif effect == 16:
            variant = rng.integers(1, 4)
            spin_count = rng.uniform(1, 3)
            spin_speed = rng.choice([-1, 1]) * rng.uniform(1, 3)
            z_speed = rng.uniform(1, 2.5)
            spin_after_done = False
            surface = rng.choice([True, False])
            if variant == 1:
                c = [[WHITE, BLUE], [RED, GREEN], [CYAN, WHITE]
                     , [GREEN, BLUE], [BLUE, YELLOW], [YELLOW, PURPLE]
                     , [PURPLE, GREEN], [RED, BLUE], [GREEN, GREEN]
                     , [BLUE, BLUE]][rng.integers(10)]
                colors = [c[0], OFF, OFF, OFF, c[1], OFF, OFF, OFF]
                generate_together = True
            elif variant == 2:
                c = [[RED, WHITE, BLUE], [GREEN, WHITE, BLUE]][rng.integers(0, 2)]
                colors = [c[0], OFF, c[1], OFF, c[2], OFF]
                generate_together = False
            elif variant == 3:
                colors = [[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], [GREEN, RED], [BLUE, WHITE, CYAN, WHITE], [RED, WHITE, BLUE]][rng.integers(4)]
                spin_count = rng.uniform(1, 3)
                spin_after_done = True
                generate_together = False
            variant = rng.choice([-1, 1])
            func = lambda: spirals(colors = colors, variant = variant, spin_count= spin_count
                                   , z_speed= z_speed, spin_speed= spin_speed, surface= surface
                                   , generate_together= generate_together, spin_after_done= spin_after_done, duration =3 * duration)
            fps(func, "spirals")
        # spirals (not spinning)
        elif effect == 17:
            variant = rng.integers(1, 5)
            if variant == 1:
                colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
                spin_count = 2
            elif variant == 2:
                colors = [GREEN, RED]
                spin_count = 5
            elif variant == 3:
                colors = [BLUE, WHITE, CYAN, WHITE]
                spin_count = 2
            elif variant == 4:
                colors = [RED, WHITE, BLUE]
                spin_count = 2
            variant = rng.choice([-1, 1])
            func = lambda: spirals(colors = colors, spin_count= spin_count, variant = variant, spin_speed= 0
                                   , end_after_spirals= True, cycles = cycles, duration =3 * duration)
            fps(func, "spirals (not spinning)")
            sleep(duration/5)
        # spirals (barbershop pole)
        elif effect == 18:
            if rng.random() < 0.5: # Two spirals
                colors = [[RED, WHITE], [BLUE, GREEN], [RED, GREEN], [BLUE, WHITE]
                          , [GREEN, PURPLE], [CYAN, ORANGE], [ORANGE, BLUE], [YELLOW, PURPLE]][rng.integers(8)]
                spin_count = rng.uniform(1, 4)
            else: # More than two spirals
                colors = [[RED, OFF, OFF, OFF, OFF, GREEN, OFF, OFF, OFF, OFF], [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
                          , [BLUE, OFF, OFF, OFF, OFF, WHITE, OFF, OFF, OFF, OFF]][rng.integers(3)]
                spin_count = rng.uniform(1, 2)
            spin_speed = rng.choice([-1, 1]) * rng.uniform(.75, 3.75)
            variant = rng.choice([-1, 1])
            func = lambda: spirals(colors = colors, spin_speed= spin_speed, spin_count= spin_count
                                   , variant = variant, generate_instantly= True, duration =3 * duration)
            fps(func, "spirals (barbershop pole)")
        # spirals (rapid)
        elif effect == 19:
            start_time = time()
            while time() - start_time < 3*duration:
                if rng.random() < 0.5: # Two spirals
                    colors = [[RED, WHITE], [BLUE, GREEN], [RED, GREEN], [BLUE, WHITE]
                              , [GREEN, PURPLE], [CYAN, ORANGE], [ORANGE, BLUE], [YELLOW, PURPLE]][rng.integers(8)]
                    spin_count = rng.uniform(1, 4)
                else: # More than two spirals
                    c = [[WHITE, BLUE], [RED, GREEN], [CYAN, WHITE]
                         , [GREEN, BLUE], [BLUE, YELLOW], [YELLOW, PURPLE]
                         , [PURPLE, GREEN], [RED, BLUE], [GREEN, GREEN]
                         , [BLUE, BLUE]][rng.integers(10)]
                    colors = [[c[0], OFF, OFF, OFF, OFF, c[1], OFF, OFF, OFF, OFF], [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
                              , [c[1], OFF, OFF, OFF, OFF, c[0], OFF, OFF, OFF, OFF]][rng.integers(3)]
                    spin_count = rng.uniform(1, 3)
                spin_speed = rng.choice([-1, 1]) * rng.uniform(1.5, 3.5)
                variant = rng.choice([-1, 1])
                surface = rng.choice([True, False])
                func = lambda: spirals(colors = colors, spin_speed= spin_speed, spin_count= spin_count
                                       , variant = variant, surface= surface, generate_instantly= True, duration = 2)
                fps(func, "spirals (rapid)")
        # spotlight
        elif effect == 20:
            if rng.random() < 0.15:
                colors = [[RED, GREEN], [GREEN, BLUE], [BLUE, YELLOW], [YELLOW, PURPLE]
                          , [PURPLE, GREEN], [RED, BLUE], [GREEN, PURPLE]][rng.integers(7)]
            else:
                colors = [WHITE, BLUE]
            func = lambda: spotlight(colors = colors, duration = 3*duration)
            fps(func, "spotlight")
        # sweep
        elif effect == 21:
            colors = [None, COLORS, RAINBOW][rng.integers(3)]
            speed = rng.uniform(4, 7)
            clockwise = rng.choice([True, False])
            alternate = rng.choice([True, True, False])
            func = lambda: sweep(speed = speed, clockwise= clockwise, alternate= alternate, duration =3 * duration)
            fps(func, "sweep")
        # sweeper
        elif effect == 22:
            if rng.random() < 0.5:
                colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
                sequence = True
            else:
                colors = [None, COLORS, TRADITIONAL_COLORS, TREE_COLORS][rng.integers(4)]
                sequence = False
            speed = rng.choice([-1, 1]) * rng.uniform(4, 10)
            func = lambda: sweeper(colors = colors, speed = speed, sequence= sequence, duration =2 * duration)
            fps(func, "sweeper")
        # twinkle
        elif effect == 23:
            if rng.random() < 0.5:
                colors = [[100, 100, 100], [100, 100, 100], [0, 100, 0], [0, 0, 100], [0, 0, 100], [0, 100, 100], [50, 0, 100]][rng.integers(0, 7)]
            else:
                colors = [COLORS, TREE_COLORS, TREE_COLORS_2, RAINBOW, TRADITIONAL_COLORS, TRADITIONAL_COLORS, rng.choice(COLORS)][rng.integers(6)]
            if rng.random() < 0.5:
                intensity = rng.uniform(1.2, 2)
            else:
                intensity = rng.uniform(10, 20)
            func = lambda: twinkle(colors = colors, intensity = intensity, duration = 3*duration)
            fps(func, "twinkle")
        # wander
        elif effect == 24:
            colors = [None, COLORS, TREE_COLORS, TREE_COLORS_2, RAINBOW, TRADITIONAL_COLORS][rng.integers(6)]
            wander_time = rng.uniform(.5, 2)
            func = lambda: wander(colors = colors, wander_time= wander_time, duration =3 * duration)
            fps(func, "wander")
        # windingSpirals
        elif effect == 25:
            c = [[WHITE, BLUE], [RED, GREEN], [CYAN, WHITE]
                 , [GREEN, BLUE], [BLUE, YELLOW], [YELLOW, PURPLE]
                 , [PURPLE, GREEN], [RED, BLUE], [GREEN, GREEN]
                 , [BLUE, BLUE]][rng.integers(10)]
            colors = [[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
                      , [c[0], OFF, OFF, OFF, c[1], OFF, OFF, OFF]
                      , [c[1], OFF, OFF, OFF, c[0], OFF, OFF, OFF]
                      , [RED, GREEN], [BLUE, YELLOW], [BLACK, BLUE]][rng.integers(6)]
            max_spin_count = rng.uniform(3, 5)
            if len(colors) == 2:
                max_spin_count += rng.uniform(0, 4)
            d_spin = rng.choice([-1, 1]) * rng.uniform(2.5, 3.5)
            d_offset = max(rng.uniform(-1, 2), 0)
            func = lambda: winding_spirals(colors = colors, max_spin_count= max_spin_count, d_spin= d_spin, d_offset= d_offset, duration =2 * duration)
            fps(func, "windingSpirals")
        # zSpiral
        elif effect == 26:
            start_time = time()
            twists = rng.uniform(5, 9)
            spiral_speed = rng.uniform(PI, 3*TAU)
            cycle_speed = rng.uniform(300, 500)
            spiral_backwards = rng.choice([True, False])
            cycle_backwards = rng.choice([True, False])
            func = lambda: z_spiral(speed = spiral_speed, twists = twists, backwards = spiral_backwards, cycles = cycles)
            fps(func, "zSpiral")
            func = lambda: tree.cycle(variant = 4, speed = cycle_speed, backwards = cycle_backwards, duration = max(2*duration - (time() - start_time), 0.1))
            fps(func, "cycle")
        # gradient
        elif effect == 27:
            variant = rng.integers(10)
            if variant < 5:
                colors = [None, RAINBOW, [RED, GREEN, BLUE], [RED, BLUE, GREEN]][rng.integers(4)]
                variant = rng.choice([0, 1, 2, 3, 3, 4, 4, 5, 5])
                indices = None
            elif variant < 8:
                colors = [[RED, GREEN], [GREEN, BLUE], [BLUE, RED]
                      , [YELLOW, PURPLE], [CYAN, PINK], [GREEN, PURPLE]][rng.integers(6)]
                variant = 4
                indices = None
            else: # Random map
                colors = RAINBOW
                indices = rng.permutation(tree.n)
                variant = None
            backwards = rng.choice([True, False])
            softness = rng.integers(2, 5)
            normalize = rng.choice([True, False, False])
            speed = rng.integers(250, 350)
            func = lambda: gradient(colors = colors, softness = softness
                                    , normalize= normalize, variant = variant, indices = indices)
            fps(func, "gradient")
            func = lambda: tree.cycle(variant = variant, backwards = backwards
                                      , speed = speed, indices = indices, duration = 3*duration)
            fps(func, "cycle")
        # pizza
        elif effect == 28:
            func = lambda: pizza()
            fps(func, "pizza")
            sleep(duration)
        # traffic_cone
        elif effect == 29:
            func = lambda: traffic_cone()
            fps(func, "traffic_cone")
            sleep(duration)
        # random_fill
        elif effect == 30:
            variant = rng.integers(3)
            if variant == 0:
                colors = [None, COLORS, TREE_COLORS, TREE_COLORS_2, rng.choice(COLORS), TRADITIONAL_COLORS][rng.integers(6)]
                speed = rng.integers(75, 150)
                sequence = False
                empty = True
                name = "random_fill"
            elif variant == 1:
                colors = [[BLUE, WHITE], [RED, GREEN], [YELLOW, PURPLE], [WHITE, GREEN]
                          , [ORANGE, BLUE], [RED, RED, RED, WHITE, WHITE, WHITE, BLUE, BLUE]][rng.integers(6)]
                speed = rng.integers(200, 601)
                sequence = False
                empty = False
                name = "randomSet"
            else:
                if rng.random() < 0.7:
                    colors = rng.choice(COLORS)
                else:
                    colors = [COLORS, TRADITIONAL_COLORS, TREE_COLORS, TREE_COLORS_2, RAINBOW][rng.integers(5)]
                speed = rng.integers(50, 151)
                sequence = True
                empty = True
                name = "sequence"
            if duration < 10:
                d = 2*duration
            else:
                d = np.inf
            func = lambda: random_fill(colors = colors, speed = speed, sequence= sequence, empty= empty, cycles =2 * cycles, duration = d)
            fps(func, name)
        # set_all
        elif effect == 31:
            colors = [None, COLORS][rng.integers(2)]
            func = lambda: set_all(colors = colors)
            fps(func, "set_all")
            sleep(duration)
        # set_all_random
        elif effect == 32:
            colors = [None, COLORS, TREE_COLORS, TREE_COLORS_2, RAINBOW, TRADITIONAL_COLORS][rng.integers(6)]
            func = lambda: set_all_random(colors = colors)
            fps(func, "set_all_random")
            sleep(duration)
        # nightSky
        elif effect == 33:
            func = lambda: night_sky(duration = duration)
            fps(func, "nightSky")
        # candy corn
        elif effect == 34:
            func = lambda: candy_corn()
            fps(func, "candy_corn")
            sleep(duration)
            
# Puts on a curated show of effects, using only effects that don't require an accurate light tree mapping
def unmapped_show(duration = 30):
    show(effects = [2, 7, 8, 23, 24, 27, 30, 31, 32, 33], duration = duration)


if __name__ == "__main__":
    try:
        show()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
