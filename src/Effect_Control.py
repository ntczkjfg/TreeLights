from Common_Variables import rng, tree, PI, TAU
from Colors import *
from Dynamic_Effects import *
from Simple_Effects import *
from time import sleep

# When the tree first receives power, some lights turn on randomly - clear to fix
tree.clear()
tree.clear()

# Puts on a curated show of effects
def show(setEffect = None, duration = 30, QUICK = False):
    if QUICK:
        quickShow()
        return
    oldEffect = 0
    effect = 0
    cycles = 1
    while True:
        while effect == oldEffect: effect = rng.integers(1, 34)
        oldEffect = effect
        if setEffect != None: effect = setEffect
        print("Effect", effect)
        # cylinder
        if effect == 1:
            cylinder(duration = 3*duration)
        # cylon
        elif effect == 2:
            variant = rng.integers(1, 5)
            color = RED if variant < 4 else COLORS
            cylon(color = color, duration = duration)
        # fallingColors
        elif effect == 3:
            fallingColors(duration = 3*duration)
        # bouncingRainbowBall
        elif effect == 4:
            bouncingRainbowBall(duration = 3*duration)
        # pulsatingSphere
        elif effect == 5:
            dR = 0.025 + 0.02 * rng.random()
            dH = 0.01 + 0.01 * rng.random()
            pulsatingSphere(dR = dR, dH = dH, duration = 3*duration)
        # randomFill
        elif effect == 6:
            randomFill(cycles = cycles)
        # randomPlanes
        elif effect == 7:
            randomPlanes(duration = 3*duration)
        # sequence
        elif effect == 8:
            speed = rng.integers(1, 4)
            sequence(cycles = cycles, speed = speed)
        # snake
        elif effect == 9:
            snake(cycles = cycles)
        # spinningPlane
        elif effect == 10:
            variant = rng.choice([0, 0, 0, 1, 2, 2, 2, 3])
            speed = 0.1 + 0.25 * rng.random()
            width = 0.1 + 0.2 * rng.random()
            height = rng.choice([0, 0, 0, tree.zMax / 2, tree.zMax / 2, tree.zMax / 2, tree.zMax / 2, tree.zMax / 2, tree.zMax])
            if height == 0 or height == tree.zMax: speed = 0.1 + 0.1 * rng.random()
            TWOCOLORS = rng.choice([True, False, False])
            BACKGROUND = rng.choice([True, False, False])
            spinningPlane(variant = variant, speed = speed
                          , width = width, height = height
                          , TWOCOLORS = TWOCOLORS, BACKGROUND = BACKGROUND
                          , duration = 3*duration)
        # spinningPlane (spinner variant)
        elif effect == 11:
            colors = [[WHITE, BLUE], [RED, GREEN], [CYAN, WHITE], [GREEN, BLUE], [BLUE, YELLOW], [YELLOW, PURPLE], [PURPLE, GREEN]][rng.integers(0, 7)]
            if rng.random() < 0.2: colors[1] = OFF
            variant = rng.integers(0, 4)
            speed = 0.1 + 0.35 * rng.random()
            spinningPlane(colors = colors, variant = variant, speed = speed, SPINNER = True, duration = duration)
        # spirals
        elif effect == 12:
            variant = rng.integers(1, 4)
            spinCount = rng.choice([1, 2, 3])
            spinSpeed = (1 + 2*rng.random()) * rng.choice([-1, 1])
            zSpeed = 1 + 1.5 * rng.random()
            SPINAFTERDONE = False
            SURFACE = rng.choice([True, False])
            if variant == 1:
                c = [[RED, BLUE], [GREEN, BLUE], [BLUE, YELLOW], [GREEN, GREEN], [BLUE, BLUE]][rng.integers(0, 5)]
                colors = [c[0], OFF, OFF, OFF, c[1], OFF, OFF, OFF]
                GENERATETOGETHER = True
            elif variant == 2:
                c = [[RED, WHITE, BLUE], [GREEN, WHITE, BLUE]][rng.integers(0, 2)]
                colors = [c[0], OFF, c[1], OFF, c[2], OFF]
                GENERATETOGETHER = False
            elif variant == 3:
                colors = [[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], [GREEN, RED], [BLUE, WHITE, CYAN, WHITE], [RED, WHITE, BLUE]][rng.integers(0, 4)]
                spinCount = rng.integers(1, 4)
                SPINAFTERDONE = True
                GENERATETOGETHER = False
            variant = rng.choice([-1, 1])
            spirals(colors = colors, variant = variant, spinCount = spinCount
                    , zSpeed = zSpeed, spinSpeed = spinSpeed,
                    SURFACE = SURFACE, GENERATETOGETHER = GENERATETOGETHER, SPINAFTERDONE = SPINAFTERDONE, duration = 3*duration)
        # spirals (Not spinning)
        elif effect == 13:
            variant = rng.integers(1, 5)
            if variant == 1:
                colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
                spinCount = 2
            elif variant == 2:
                colors = [GREEN, RED]
                spinCount = 5
            elif variant == 3:
                colors = [BLUE, WHITE, CYAN, WHITE]
                spinCount = 2
            elif variant == 4:
                colors = [RED, WHITE, BLUE]
                spinCount = 2
            variant = rng.choice([-1, 1])
            spirals(colors = colors, spinCount = 2, variant = variant, spinSpeed = 0
                    , ENDAFTERSPIRALS = True, cycles = cycles, duration = 3*duration)
            sleep(duration/5)
        # spirals (barbershop style)
        elif effect == 14:
            variant = rng.integers(1, 3)
            if variant == 1: # Two spirals
                colors = [[RED, WHITE], [BLUE, GREEN], [RED, GREEN], [BLUE, WHITE]
                          , [GREEN, PURPLE], [CYAN, ORANGE], [ORANGE, BLUE], [YELLOW, PURPLE]][rng.integers(0, 8)]
                spinCount = rng.choice([1, 2, 3, 4])
            elif variant == 2: # More than two spirals
                colors = [[RED, OFF, OFF, OFF, OFF, GREEN, OFF, OFF, OFF, OFF], [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
                          , [BLUE, OFF, OFF, OFF, OFF, WHITE, OFF, OFF, OFF, OFF]][rng.integers(0, 3)]
                spinCount = rng.choice([1, 2])
            spinSpeed = (.75 + 3*rng.random()) * rng.choice([-1, 1])
            variant = rng.choice([-1, 1])
            spirals(colors = colors, spinSpeed = spinSpeed, spinCount = spinCount, variant = variant, GENERATEINSTANTLY = True, duration = 3*duration)
        elif effect == 31:
            startTime = time()
            while time() - startTime < 3*duration:
                variant = rng.integers(1, 3)
                if variant == 1: # Two spirals
                    colors = [[RED, WHITE], [BLUE, GREEN], [RED, GREEN], [BLUE, WHITE]
                              , [GREEN, PURPLE], [CYAN, ORANGE], [ORANGE, BLUE], [YELLOW, PURPLE]][rng.integers(0, 8)]
                    spinCount = rng.integers(1, 5)
                elif variant == 2: # More than two spirals
                    colors = [[RED, OFF, OFF, OFF, OFF, GREEN, OFF, OFF, OFF, OFF], [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
                              , [BLUE, OFF, OFF, OFF, OFF, WHITE, OFF, OFF, OFF, OFF]][rng.integers(0, 3)]
                    spinCount = rng.integers(1, 4)
                spinSpeed = (1.5 + 2*rng.random()) * rng.choice([-1, 1])
                variant = rng.choice([-1, 1])
                SURFACE = rng.choice([True, False])
                spirals(colors = colors, spinSpeed = spinSpeed, spinCount = spinCount, variant = variant
                        , SURFACE = SURFACE, GENERATEINSTANTLY = True, duration = 2)
        # spotlight
        elif effect == 15:
            spotlight(duration = 3*duration)
        # alternatingStripes
        elif effect == 16:
            colors = [[[200, 30, 30], CYAN, PURPLE], [[0, 10, 90], [5, 90, 5], [70, 15, 15]]][rng.integers(0, 2)]
            stripeCount = rng.choice([2, 2, 2, 2, 3, 3, 3, 4, 4])
            spinSpeed = rng.choice([-1, 1]) * (PI/4 + rng.random() * 3*PI/4)
            alternatingStripes(*colors, stripeCount = stripeCount, spinSpeed = spinSpeed, duration = duration)
        # twinkle
        elif effect == 17:
            if rng.random() < 0.5:
                colors = [[100, 100, 100], [100, 100, 100], [100, 0, 0], [0, 0, 100], [0, 0, 100], [100, 0, 100], [0, 50, 100]][rng.integers(0, 7)]
            else:
                colors = [COLORS, TREECOLORS, TRADITIONALCOLORS, TRADITIONALCOLORS][rng.integers(0, 4)]
            intensity = rng.choice(5)
            twinkle(colors = colors, intensity = intensity, duration = 3*duration)
        # wander
        elif effect == 18:
            colors = [None, COLORS, TREECOLORS, TRADITIONALCOLORS, TRADITIONALCOLORS][rng.integers(0, 5)]
            slowness = 10 + rng.integers(0, 16)
            wander(colors = colors, slowness = slowness, duration = 3*duration)
        # zSpiral
        elif effect == 19:
            startTime = time()
            speed = int(20 + 20 * rng.random())
            backwards = rng.choice([True, False])
            zSpiral(cycles = cycles)
            tree.cycle(variant = 5, step = speed, backwards = backwards, duration = 2*duration - (time() - startTime))
        # gradient
        elif effect == 20:
            colors = [None, COLORS][rng.integers(0, 2)]
            gradient(colors = colors, duration = 3*duration)
        # rainbow
        elif effect == 21:
            rainbow(duration = 3*duration)
        # setAll
        elif effect == 22:
            setAll()
            sleep(duration)
        # setAllRandom
        elif effect == 23:
            variant = rng.integers(1, 4)
            colors = [None, COLORS, TREECOLORS, TRADITIONALCOLORS, TRADITIONALCOLORS][rng.integers(0, 5)]
            if variant == 1:
                speed = 0
                setAllRandom(colors = colors)
                sleep(duration)
                continue
            elif variant == 2:
                speed = rng.integers(1, 5)
            elif variant == 3:
                speed = rng.integers(50, 100)
                colors = [[BLUE, WHITE], [RED, GREEN], [YELLOW, PURPLE], [WHITE, GREEN]
                          , [ORANGE, BLUE], [RED, RED, RED, WHITE, WHITE, WHITE, BLUE, BLUE]][rng.integers(0, 6)]
            setAllRandom(colors = colors, speed = speed, duration = duration)
        # sweep
        elif effect == 24:
            sections = rng.integers(20, 41)
            CLOCKWISE = [True, False][rng.integers(0, 2)]
            ALTERNATE = [True, False][rng.integers(0, 2)]
            sweep(sections = sections, CLOCKWISE = CLOCKWISE, ALTERNATE = ALTERNATE, duration = 3*duration)
        # radialGradient
        elif effect == 25:
            colors = [[RED, GREEN], [GREEN, BLUE], [BLUE, RED], [YELLOW, PURPLE], [CYAN, PINK], [GREEN, PURPLE]][rng.integers(0, 6)]
            radialGradient(colors = colors, duration = 3*duration)
        # pizza
        elif effect == 26:
            pizza()
            sleep(duration)
        # rain
        elif effect == 27:
            variant = rng.integers(0, 3)
            if variant < 2:
                color = [CYAN, BLUE][variant]
                speed = 0.15 + 0.4*rng.random()
                wind = -0.3 + 0.6*rng.random()
            elif variant == 2: # Like the matrix
                color = GREEN
                speed = 0.15
                wind = 0
            dropCount = 8 + rng.integers(0, 6)
            rain(color = color, speed = speed, wind = wind, dropCount = dropCount, duration = 3*duration)
        # fire
        elif effect == 28:
            fire(duration = 3*duration)
        # clock
        elif effect == 29:
            clock(duration = duration)
        # rain (accumulating snow variant)
        elif effect == 30:
            rain(color = WHITE, dropCount = 11, accumulationSpeed = 0.0025, wind = 0, speed = 0.1, duration = 3*duration)
        # fade
        elif effect == 32:
            colors = [TRADITIONALCOLORS, COLORS, TREECOLORS, None, COLORS[rng.integers(len(COLORS))]][rng.integers(5)]
            midline = .3 + .4*rng.random() # .3 to .7, this is also the maximum value of amplitude
            amplitude = min(1.2*midline*max(.6*midline, rng.random()), midline) # Give it a 20% chance of maxing out
            speed = rng.integers(1, 3) + 0.5 * rng.random()
            fade(colors = colors, midline = midline, amplitude = amplitude, speed = speed, duration = 2*duration)
        # blink
        elif effect == 33:
            colors = [TRADITIONALCOLORS, COLORS, TREECOLORS, None, COLORS[rng.integers(len(COLORS))]][rng.integers(5)]
            groups = rng.integers(5, 15)
            p = 0.5 + 0.35 * rng.random()
            slowness = 0.3 + rng.random()
            blink(colors = colors, groups = groups, slowness = slowness, p = p, duration = duration)

# Puts on a curated show of effects, using only effects that don't require an accurate light tree mapping
def unmappedShow(setEffect = None, duration = 90, QUICK = False):
    if QUICK:
        quickShow()
        return
    oldEffect = 0
    effect = 0
    cycles = 1
    while True:
        while effect == oldEffect: effect = rng.integers(1, 9)
        oldEffect = effect
        if setEffect != None: effect = setEffect
        print("Effect", effect)
        # randomFill
        if effect == 1:
            randomFill(cycles = cycles)
        # sequence
        elif effect == 2:
            speed = rng.integers(1, 4)
            sequence(cycles = cycles, speed = speed)
        # twinkle
        elif effect == 3:
            if rng.random() < 0.5:
                colors = [[100, 100, 100], [100, 100, 100], [100, 0, 0], [0, 0, 100], [0, 0, 100], [100, 0, 100], [0, 50, 100]][rng.integers(0, 7)]
            else:
                colors = [COLORS, TREECOLORS, TRADITIONALCOLORS, TRADITIONALCOLORS][rng.integers(0, 4)]
            intensity = rng.choice(5)
            twinkle(colors = colors, intensity = intensity, duration = 3*duration)
        # wander
        elif effect == 4:
            colors = [None, COLORS, TREECOLORS, TRADITIONALCOLORS, TRADITIONALCOLORS][rng.integers(0, 5)]
            slowness = 10 + rng.integers(0, 16)
            wander(colors = colors, slowness = slowness, duration = 3*duration)
        # setAll
        elif effect == 5:
            setAll()
            sleep(duration)
        # setAllRandom
        elif effect == 6:
            variant = rng.integers(1, 4)
            colors = [None, COLORS, TREECOLORS, TRADITIONALCOLORS, TRADITIONALCOLORS][rng.integers(0, 5)]
            if variant == 1:
                speed = 0
                setAllRandom(colors = colors)
                sleep(duration)
                continue
            elif variant == 2:
                speed = rng.integers(1, 5)
            elif variant == 3:
                speed = rng.integers(50, 100)
                colors = [[BLUE, WHITE], [RED, GREEN], [YELLOW, PURPLE], [WHITE, GREEN]
                          , [ORANGE, BLUE], [RED, RED, RED, WHITE, WHITE, WHITE, BLUE, BLUE]][rng.integers(0, 6)]
            setAllRandom(colors = colors, speed = speed, duration = duration)
        # fade
        elif effect == 7:
            colors = [TRADITIONALCOLORS, COLORS, TREECOLORS, None, COLORS[rng.integers(len(COLORS))]][rng.integers(5)]
            divisions = rng.integers(5, 12)
            midline = divisions // 2 + rng.choice([-1, 1])
            amplitude = min(midline, divisions - midline) * min(rng.random() + 0.3, 1) * rng.choice([-1, 1])
            speed = rng.integers(1, 3) + 0.5 * rng.random()
            fade(colors = colors, divisions = divisions, midline = midline, amplitude = amplitude, speed = speed, duration = 2*duration)
        # blink
        elif effect == 8:
            colors = [TRADITIONALCOLORS, COLORS, TREECOLORS, None, COLORS[rng.integers(len(COLORS))]][rng.integers(5)]
            groups = rng.integers(5, 15)
            p = 0.5 + 0.35 * rng.random()
            slowness = 0.3 + rng.random()
            blink(colors = colors, groups = groups, slowness = slowness, p = p, duration = duration)


if __name__ == "__main__":
    pass
    tree[0].a = 0
    show()