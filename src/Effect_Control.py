from Common_Variables import rng, tree, PI, TAU
from Colors import *
from Dynamic_Effects import *
from Simple_Effects import *
from time import sleep

# When the tree first receives power, lights sometimes turn on randomly - clear to fix
tree.clear()
tree.clear()

def fps(func, name):
    print(f"{name}: ", end = "")
    tree.frames = 0
    startTime = time()
    func()
    duration = time() - startTime
    print(f"{tree.frames} frame{'s' if tree.frames != 1 else ''} in {round(duration, 2)} seconds for {round(tree.frames/duration, 1)} fps")
    tree.clear(FLAGSONLY = True)

# Puts on a curated show of effects
def show(setEffect = None, duration = 30, insequence = False, start = 0):
    oldEffect = 0
    effect = start
    cycles = 1
    effectCount = 32
    while True:
        if setEffect:
            if type(setEffect) == int:
                effect = setEffect
            else:
                while effect == oldEffect: effect = rng.choice(setEffect)
        elif insequence:
            effect += 1
            if effect > effectCount:
                effect = 1
        else:
            while effect == oldEffect: effect = 1 + rng.integers(effectCount)
        oldEffect = effect
        # cylinder
        if effect == 1:
            colors = [[[200, 30, 30], CYAN, PURPLE]
                      , [[0, 10, 90], [5, 90, 5], [70, 15, 15]]][rng.integers(0, 2)]
            stripeCount = rng.choice([2, 2, 2, 2, 3, 3, 3, 4, 4])
            spinSpeed = rng.choice([-1, 1]) * rng.uniform(PI/4, PI)
            func = lambda: alternatingStripes(*colors, stripeCount = stripeCount, spinSpeed = spinSpeed, duration = duration)
            fps(func, "alternatingStripes")
        # blink
        elif effect == 2:
            colors = [TRADITIONALCOLORS, COLORS, TREECOLORS, None, rng.choice(COLORS)][rng.integers(5)]
            groupCount = rng.integers(5, 15)
            if rng.random() < 0.3:
                groupCount = rng.integers(50, 400)
            p = rng.uniform(0.5, 0.85)
            delay = rng.uniform(0.3, 0.7)
            func = lambda: blink(colors = colors, groupCount = groupCount, delay = delay, p = p, duration = duration)
            fps(func, "blink")
        # bouncingRainbowBall
        elif effect == 3:
            func = lambda: bouncingRainbowBall(duration = 3*duration)
            fps(func, "bouncingRainbowBall")
        # clock
        elif effect == 4:
            func = lambda: clock(duration = duration)
            fps(func, "clock")
        # cylinder
        elif effect == 5:
            colors = [COLORS, TRADITIONALCOLORS, TREECOLORS, None, TREECOLORS2, RAINBOW][rng.integers(6)]
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
            colors = [TRADITIONALCOLORS, COLORS, TREECOLORS, TREECOLORS2, None, rng.choice(COLORS)][rng.integers(6)]
            midline = rng.uniform(.3, .7) # This is also the maximum value of amplitude
            amplitude = min(rng.uniform(midline/2, 1.1*midline), midline) # Give it a 20% chance of maxing out
            speed = rng.uniform(1, 2.5)
            func = lambda: fade(colors = colors, midline = midline, amplitude = amplitude, speed = speed, duration = 2*duration)
            fps(func, "fade")
        # fadeRestore
        elif effect == 8:
            colors = [TRADITIONALCOLORS, COLORS, TREECOLORS, TREECOLORS2, None, rng.choice(COLORS)][rng.integers(5)]
            p = rng.uniform(.8, .98)
            halflife = rng.uniform(.1, .5)
            func = lambda: fadeRestore(colors = colors, p = p, halflife = halflife, duration = 2*duration)
            fps(func, "fadeRestore")
        # fallingColors
        elif effect == 9:
            func = lambda: fallingColors(duration = 3*duration)
            fps(func, "fallingColors")
        # fire
        elif effect == 10:
            func = lambda: fire(duration = 3*duration)
            fps(func, "fire")
        # pulsatingSphere
        elif effect == 11:
            colors = [None, COLORS, RAINBOW][rng.integers(3)]
            dR = rng.uniform(0.5, 0.9)
            dH = rng.uniform(0.2, 0.4)
            func = lambda: pulsatingSphere(colors = colors, dR = dR, dH = dH, duration = 3*duration)
            fps(func, "pulsatingSphere")
        # rain
        elif effect == 12:
            variant = rng.integers(0, 5)
            if variant < 2: # Regular rain
                color = [CYAN, BLUE][variant]
                accumulationSpeed = 0
                wind = rng.uniform(-6, 6)
                speed = rng.uniform(3, 9)
                name = "rain"
            elif variant < 3: # Like the matrix
                color = GREEN
                accumulationSpeed = 0
                wind = 0
                speed = 3
                name = "matrixTrails"
            else: # Accumulating snow
                color = WHITE
                accumulationSpeed = 0.03
                wind = 0
                speed = 2
                name = "accumulatingSnow"
            dropCount = rng.integers(8, 14)
            func = lambda: rain(color = color, dropCount = dropCount, accumulationSpeed = accumulationSpeed, wind = wind, speed = speed, duration = 2*duration)
            fps(func, name)
        # randomPlanes
        elif effect == 13:
            colors = [None, COLORS, RAINBOW][rng.integers(3)]
            func = lambda: randomPlanes(colors = colors, duration = 3*duration)
            fps(func, "randomPlanes")
        # snake
        elif effect == 14:
            func = lambda: snake(duration = 3*duration, cycles = cycles)
            fps(func, "snake")
        # spinningPlane
        elif effect == 15:
            if rng.random() < 0.5:
                colors = [None, COLORS, RAINBOW, [WHITE, BLUE], [RED, GREEN], [CYAN, WHITE], [GREEN, BLUE], [BLUE, YELLOW], [YELLOW, PURPLE], [PURPLE, GREEN]][rng.integers(10)]
                speed = rng.uniform(2, 7)
                width = rng.uniform(0.1, 0.3)
                height = rng.choice([0, 0, tree.zMax / 2, tree.zMax / 2, tree.zMax / 2, tree.zMax / 2, tree.zMax / 2, tree.zMax])
                # Higher speeds are jarring at these heights
                if height == 0 or height == tree.zMax: speed = rng.uniform(2, 3.5)
                TWOCOLORS = rng.choice([True, False, False])
                BACKGROUND = rng.choice([True, True, False])
                SPINNER = False
                name = "spinningPlane"
            else:
                colors = [[WHITE, BLUE], [RED, GREEN], [CYAN, WHITE], [GREEN, BLUE], [BLUE, YELLOW], [YELLOW, PURPLE], [PURPLE, GREEN]][rng.integers(7)]
                if rng.random() < 0.2: colors[rng.integers(2)] = OFF
                speed = rng.uniform(2, 9)
                height, width = tree.zMid, 0.15
                SPINNER, TWOCOLORS, BACKGROUND = True, False, False
                name = "spinner"
            variant = rng.choice([0, 0, 0, 1, 2, 2, 2, 3])
            func = lambda: spinningPlane(colors = colors, variant = variant, speed = speed, SPINNER = SPINNER
                                         , TWOCOLORS = TWOCOLORS, BACKGROUND = BACKGROUND, height = height
                                         , width = width, duration = duration)
            fps(func, name)
        # spirals
        elif effect == 16:
            variant = rng.integers(1, 4)
            spinCount = rng.uniform(1, 3)
            spinSpeed = rng.choice([-1, 1]) * rng.uniform(1, 3)
            zSpeed = rng.uniform(1, 2.5)
            SPINAFTERDONE = False
            SURFACE = rng.choice([True, False])
            if variant == 1:
                c = [[WHITE, BLUE], [RED, GREEN], [CYAN, WHITE]
                     , [GREEN, BLUE], [BLUE, YELLOW], [YELLOW, PURPLE]
                     , [PURPLE, GREEN], [RED, BLUE], [GREEN, GREEN]
                     , [BLUE, BLUE]][rng.integers(10)]
                colors = [c[0], OFF, OFF, OFF, c[1], OFF, OFF, OFF]
                GENERATETOGETHER = True
            elif variant == 2:
                c = [[RED, WHITE, BLUE], [GREEN, WHITE, BLUE]][rng.integers(0, 2)]
                colors = [c[0], OFF, c[1], OFF, c[2], OFF]
                GENERATETOGETHER = False
            elif variant == 3:
                colors = [[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], [GREEN, RED], [BLUE, WHITE, CYAN, WHITE], [RED, WHITE, BLUE]][rng.integers(4)]
                spinCount = rng.uniform(1, 3)
                SPINAFTERDONE = True
                GENERATETOGETHER = False
            variant = rng.choice([-1, 1])
            func = lambda: spirals(colors = colors, variant = variant, spinCount = spinCount
                    , zSpeed = zSpeed, spinSpeed = spinSpeed, SURFACE = SURFACE
                    , GENERATETOGETHER = GENERATETOGETHER, SPINAFTERDONE = SPINAFTERDONE, duration = 3*duration)
            fps(func, "spirals")
        # spirals (not spinning)
        elif effect == 17:
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
            func = lambda: spirals(colors = colors, spinCount = spinCount, variant = variant, spinSpeed = 0
                    , ENDAFTERSPIRALS = True, cycles = cycles, duration = 3*duration)
            fps(func, "spirals (not spinning)")
            sleep(duration/5)
        # spirals (barbershop pole)
        elif effect == 18:
            if rng.random() < 0.5: # Two spirals
                colors = [[RED, WHITE], [BLUE, GREEN], [RED, GREEN], [BLUE, WHITE]
                          , [GREEN, PURPLE], [CYAN, ORANGE], [ORANGE, BLUE], [YELLOW, PURPLE]][rng.integers(8)]
                spinCount = rng.uniform(1, 4)
            else: # More than two spirals
                colors = [[RED, OFF, OFF, OFF, OFF, GREEN, OFF, OFF, OFF, OFF], [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
                          , [BLUE, OFF, OFF, OFF, OFF, WHITE, OFF, OFF, OFF, OFF]][rng.integers(3)]
                spinCount = rng.uniform(1, 2)
            spinSpeed = rng.choice([-1, 1]) * rng.uniform(.75, 3.75)
            variant = rng.choice([-1, 1])
            func = lambda: spirals(colors = colors, spinSpeed = spinSpeed, spinCount = spinCount
                    , variant = variant, GENERATEINSTANTLY = True, duration = 3*duration)
            fps(func, "spirals (barbershop pole)")
        # spirals (rapid)
        elif effect == 19:
            startTime = time()
            while time() - startTime < 3*duration:
                if rng.random() < 0.5: # Two spirals
                    colors = [[RED, WHITE], [BLUE, GREEN], [RED, GREEN], [BLUE, WHITE]
                              , [GREEN, PURPLE], [CYAN, ORANGE], [ORANGE, BLUE], [YELLOW, PURPLE]][rng.integers(8)]
                    spinCount = rng.uniform(1, 4)
                else: # More than two spirals
                    c = [[WHITE, BLUE], [RED, GREEN], [CYAN, WHITE]
                         , [GREEN, BLUE], [BLUE, YELLOW], [YELLOW, PURPLE]
                         , [PURPLE, GREEN], [RED, BLUE], [GREEN, GREEN]
                         , [BLUE, BLUE]][rng.integers(10)]
                    colors = [[c[0], OFF, OFF, OFF, OFF, c[1], OFF, OFF, OFF, OFF], [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
                              , [c[1], OFF, OFF, OFF, OFF, c[0], OFF, OFF, OFF, OFF]][rng.integers(3)]
                    spinCount = rng.uniform(1, 3)
                spinSpeed = rng.choice([-1, 1]) * rng.uniform(1.5, 3.5)
                variant = rng.choice([-1, 1])
                SURFACE = rng.choice([True, False])
                func = lambda: spirals(colors = colors, spinSpeed = spinSpeed, spinCount = spinCount
                        , variant = variant, SURFACE = SURFACE, GENERATEINSTANTLY = True, duration = 2)
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
            CLOCKWISE = rng.choice([True, False])
            ALTERNATE = rng.choice([True, True, False])
            func = lambda: sweep(speed = speed, CLOCKWISE = CLOCKWISE, ALTERNATE = ALTERNATE, duration = 3*duration)
            fps(func, "sweep")
        # sweeper
        elif effect == 22:
            if rng.random() < 0.5:
                colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
                SEQUENCE = True
            else:
                colors = [None, COLORS, TRADITIONALCOLORS, TREECOLORS][rng.integers(4)]
                SEQUENCE = False
            speed = rng.choice([-1, 1]) * rng.uniform(4, 10)
            func = lambda: sweeper(colors = colors, speed = speed, SEQUENCE = SEQUENCE, duration = 2*duration)
            fps(func, "sweeper")
        # twinkle
        elif effect == 23:
            if rng.random() < 0.5:
                colors = [[100, 100, 100], [100, 100, 100], [0, 100, 0], [0, 0, 100], [0, 0, 100], [0, 100, 100], [50, 0, 100]][rng.integers(0, 7)]
            else:
                colors = [COLORS, TREECOLORS, TREECOLORS2, RAINBOW, TRADITIONALCOLORS, TRADITIONALCOLORS, rng.choice(COLORS)][rng.integers(6)]
            if rng.random() < 0.5:
                intensity = rng.uniform(1.2, 2)
            else:
                intensity = rng.uniform(10, 20)
            func = lambda: twinkle(colors = colors, intensity = intensity, duration = 3*duration)
            fps(func, "twinkle")
        # wander
        elif effect == 24:
            colors = [None, COLORS, TREECOLORS, TREECOLORS2, RAINBOW, TRADITIONALCOLORS][rng.integers(6)]
            wanderTime = rng.uniform(.5, 2)
            func = lambda: wander(colors = colors, wanderTime = wanderTime, duration = 3*duration)
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
            maxSpinCount = rng.uniform(3, 5)
            if len(colors) == 2:
                maxSpinCount += rng.uniform(0, 4)
            dSpin = rng.choice([-1, 1]) * rng.uniform(2.5, 3.5)
            dOffset = max(rng.uniform(-1, 2), 0)
            func = lambda: windingSpirals(colors = colors, maxSpinCount = maxSpinCount, dSpin = dSpin, dOffset = dOffset, duration = 2*duration)
            fps(func, "windingSpirals")
        # zSpiral
        elif effect == 26:
            startTime = time()
            twists = rng.uniform(5, 9)
            spiralSpeed = rng.uniform(PI, 3*TAU)
            cycleSpeed = rng.uniform(300, 500)
            spiralBackwards = rng.choice([True, False])
            cycleBackwards = rng.choice([True, False])
            func = lambda: zSpiral(speed = spiralSpeed, twists = twists, backwards = spiralBackwards, cycles = cycles)
            fps(func, "zSpiral")
            func = lambda: tree.cycle(variant = 4, speed = cycleSpeed, backwards = cycleBackwards, duration = max(2*duration - (time() - startTime), 0.1))
            fps(func, "cycle")
        # gradient
        elif effect == 27:
            variant = rng.integers(10)
            if variant < 5:
                colors = [None, RAINBOW][rng.integers(2)]
                variant = rng.choice([0, 1, 2, 3, 3, 4, 4, 5, 5])
                indices = None
            elif variant < 8:
                colors = [[RED, GREEN, RED], [GREEN, BLUE, GREEN], [BLUE, RED, BLUE]
                      , [YELLOW, PURPLE, YELLOW], [CYAN, PINK, CYAN], [GREEN, PURPLE, GREEN]][rng.integers(6)]
                variant = 4
                indices = None
            else: # Random map
                colors = RAINBOW
                indices = rng.permutation(tree.n)
                variant = None
            backwards = rng.choice([True, False])
            speed = rng.integers(250, 350)
            func = lambda: gradient(colors = colors, variant = variant, indices = indices)
            fps(func, "gradient")
            func = lambda: tree.cycle(variant = variant, backwards = backwards, speed = speed, indices = indices, duration = 3*duration)
            fps(func, "cycle")
        # pizza
        elif effect == 28:
            func = lambda: pizza()
            fps(func, "pizza")
            sleep(duration)
        # trafficCone
        elif effect == 29:
            func = lambda: trafficCone()
            fps(func, "trafficCone")
            sleep(duration)
        # randomFill
        elif effect == 30:
            variant = rng.integers(3)
            if variant == 0:
                colors = [None, COLORS, TREECOLORS, TREECOLORS2, rng.choice(COLORS), TRADITIONALCOLORS][rng.integers(6)]
                speed = rng.integers(75, 150)
                SEQUENCE = False
                c = 2*cycles
                EMPTY = True
                name = "randomFill"
            elif variant == 1:
                colors = [[BLUE, WHITE], [RED, GREEN], [YELLOW, PURPLE], [WHITE, GREEN]
                          , [ORANGE, BLUE], [RED, RED, RED, WHITE, WHITE, WHITE, BLUE, BLUE]][rng.integers(6)]
                speed = rng.integers(200, 601)
                SEQUENCE = False
                c = np.inf
                EMPTY = False
                name = "randomSet"
            else:
                if rng.random() < 0.7:
                    colors = rng.choice(COLORS)
                else:
                    colors = [COLORS, TRADITIONALCOLORS, TREECOLORS, TREECOLORS2, RAINBOW][rng.integers(5)]
                speed = rng.integers(50, 151)
                SEQUENCE = True
                c = 2*cycles
                EMPTY = True
                name = "sequence"
            func = lambda: randomFill(colors = colors, speed = speed, SEQUENCE = SEQUENCE, EMPTY = EMPTY, cycles = c, duration = 2*duration)
            fps(func, name)
        # setAll
        elif effect == 31:
            colors = [None, COLORS][rng.integers(2)]
            func = lambda: setAll(colors = colors)
            fps(func, "setAll")
            sleep(duration)
        # setAllRandom
        elif effect == 32:
            colors = [None, COLORS, TREECOLORS, TREECOLORS2, RAINBOW, TRADITIONALCOLORS][rng.integers(6)]
            func = lambda: setAllRandom(colors = colors)
            fps(func, "setAllRandom")
            sleep(duration)
            
# Puts on a curated show of effects, using only effects that don't require an accurate light tree mapping
def unmappedShow(duration = 90):
    show(setEffect = [2, 7, 8, 23, 24, 27, 30, 31, 32], duration = duration)


if __name__ == "__main__":
    try:
        show()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
