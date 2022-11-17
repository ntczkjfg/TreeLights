from Common_Variables import rng, tree
from Colors import *
from Dynamic_Effects import *
from Simple_Effects import *
from time import sleep


# Puts on a curated show of effects
def show(setEffect = None):
    oldEffect = 0
    effect = 0
    while True:
        while effect == oldEffect: effect = rng.integers(1, 29)
        oldEffect = effect
        if setEffect != None: effect = setEffect
        # cylinder
        if effect == 1:
            cylinder(duration = 90)
        # cylon
        elif effect == 2:
            variant = rng.integers(1, 5)
            color = RED if variant < 4 else COLORS
            cylon(color = color, duration = 60)
        # fallingColors
        elif effect == 3:
            fallingColors(duration = 90)
        # bouncingRainbowBall
        elif effect == 4:
            bouncingRainbowBall(duration = 90)
        # pulsatingSphere
        elif effect == 5:
            pulsatingSphere(duration = 90)
        # randomFill
        elif effect == 6:
            randomFill(cycles = 1)
        # randomPlanes
        elif effect == 7:
            randomPlanes(duration = 90)
        # sequence
        elif effect == 8:
            sequence(cycles = 1)
            sleep(5)
        # snake
        elif effect == 9:
            snake(cycles = 1)
        # spinningPlane
        elif effect == 10:
            variant = rng.choice([0, 0, 0, 1, 2, 2, 2, 3])
            speed = 0.1 + 0.25 * rng.random()
            width = 0.1 + 0.2 * rng.random()
            height = rng.choice([0, 0, 0, tree.zMax / 2, tree.zMax / 2, tree.zMax / 2, tree.zMax / 2, tree.zMax / 2, tree.zMax])
            TWOCOLORS = rng.choice([True, False, False])
            BACKGROUND = rng.choice([True, False, False])
            spinningPlane(variant = variant, speed = speed
                          , width = width, height = height
                          , TWOCOLORS = TWOCOLORS, BACKGROUND = BACKGROUND
                          , duration = 90)
        # spinningPlane (spinner variant)
        elif effect == 11:
            colors = [[WHITE, BLUE], [RED, GREEN], [CYAN, WHITE], [GREEN, BLUE], [BLUE, YELLOW]][rng.integers(0, 5)]
            variant = rng.integers(0, 4)
            spinningPlane(colors = colors, variant = variant, SPINNER = True, duration = 50)
        # spirals
        elif effect == 12:
            variant = rng.integers(1, 2)
            if variant == 1:
                c = [[RED, BLUE], [GREEN, BLUE], [BLUE, YELLOW], [GREEN, GREEN], [BLUE, BLUE]][rng.integers(0, 5)]
                colors = [c[0], OFF, OFF, OFF, c[1], OFF, OFF, OFF]
                variant = rng.choice([-1, 1])
                spinCount = rng.choice([1, 2])
                spinSpeed = (0.05 + 0.2*rng.random())*rng.choice([-1, 1])
                spirals(colors = colors, variant = variant, spinCount = spinCount, spinSpeed = spinSpeed, SURFACE = True, GENERATETOGETHER = True, duration = 90)
            elif variant == 2: pass
            elif variant == 3: pass
            elif variant == 4: pass
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
            spirals(colors = colors, spinCount = 2, spinSpeed = 0, ENDAFTERSPIRALS = True, cycles = 1)
            sleep(5)
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
            spinSpeed = (0.1 + 0.2*rng.random()) * rng.choice([-1, 1])
            variant = rng.choice([-1, 1])
            spirals(colors = colors, spinSpeed = spinSpeed, spinCount = spinCount, variant = variant, GENERATEINSTANTLY = True, duration = 90)
        # spotlight
        elif effect == 15:
            spotlight(duration = 90)
        # stripedFill
        elif effect == 16:
            stripedFill(duration = 50)
        # twinkle
        elif effect == 17:
            variant = rng.integers(0, 3)
            intensity = rng.choice(5)
            if variant == 0:
                color = [[50, 50, 50], [50, 50, 50], [50, 0, 0], [0, 0, 50], [0, 0, 50], [50, 0, 50], [0, 25, 50]][rng.integers(0, 7)]
                twinkle(variant = variant, color = color, intensity = intensity, duration = 90)
            else:
                twinkle(variant = variant, intensity = intensity, duration = 90)
        # wander
        elif effect == 18:
            wander(duration = 90)
        # zSpiral
        elif effect == 19:
            zSpiral(cycles = 1)
            sleep(10)
        # gradient
        elif effect == 20:
            gradient(duration = 90)
        # rainbow
        elif effect == 21:
            rainbow(duration = 90)
        # setAll
        elif effect == 22:
            setAll()
            sleep(10)
        # setAllRandom
        elif effect == 23:
            variant = rng.integers(1, 3)
            if variant == 1:
                setAllRandom()
                sleep(10)
            elif variant == 2:
                setAllRandom(continuous = True, duration = 60)
        # sweep
        elif effect == 24:
            sweep(duration = 90)
        # radialGradient
        elif effect == 25:
            colors = [[RED, GREEN], [GREEN, BLUE], [BLUE, RED]][rng.integers(0, 3)]
            radialGradient(colors = colors, duration = 90)
        # pizza
        elif effect == 26:
            pizza()
            sleep(10)
        # rain
        elif effect == 27:
            variant = rng.integers(0, 3)
            if variant < 2:
                color = [CYAN, BLUE][variant]
                speed = 0.15 + 0.4*rng.random()
                wind = -0.3 + 0.6*rng.random()
            elif variant == 3: # Like the matrix
                color = GREEN
                speed = 0.15
                wind = 0
            rain(color = color, speed = speed, wind = wind, duration = 90)
        # fire
        elif effect == 28:
            fire(duration = 90)

# Shows off short versions of most effects
def quickShow(setEffect = None):
    effect = 1
    while True:
        # cylinder
        if effect == 1:
            cylinder(duration = 9)
        # cylon
        elif effect == 2:
            for i in range(2):
                cylon(color = [RED, COLORS][i], duration = 4.5)
        # fallingColors
        elif effect == 3:
            fallingColors(duration = 9)
        # bouncingRainbowBall
        elif effect == 4:
            bouncingRainbowBall(duration = 9)
        # pulsatingSphere
        elif effect == 5:
            pulsatingSphere(duration = 9)
        # randomFill
        elif effect == 6:
            randomFill(cycles = 1)
        # randomPlanes
        elif effect == 7:
            randomPlanes(duration = 9)
        # sequence
        elif effect == 8:
            sequence(cycles = 1)
            sleep(1)
        # snake
        elif effect == 9:
            snake(cycles = 1)
        # spinningPlane
        elif effect == 10:
            for i in range(5):
                variant = [0, 0, 1, 2, 3][i]
                speed = 0.1 + 0.25 * rng.random()
                width = 0.1 + 0.2 * rng.random()
                height = [tree.zMax/2, 0, tree.zMax, tree.zMax/2, tree.zMax/2][i]
                TWOCOLORS = rng.choice([True, False])
                BACKGROUND = rng.choice([True, False])
                spinningPlane(variant = variant, speed = speed
                              , width = width, height = height
                              , TWOCOLORS = TWOCOLORS, BACKGROUND = BACKGROUND
                              , duration = 4)
        # spinningPlane (spinner variant)
        elif effect == 11:
            for i in range(4):
                colors = [[WHITE, BLUE], [RED, GREEN], [GREEN, BLUE], [BLUE, YELLOW]][i]
                variant = i
                spinningPlane(colors = colors, variant = variant, SPINNER = True, duration = 4)
        # spirals
        elif effect == 12:
            variant = 1
            if variant == 1:
                c = [[RED, BLUE], [GREEN, BLUE], [BLUE, YELLOW], [GREEN, GREEN], [BLUE, BLUE]][rng.integers(0, 5)]
                colors = [c[0], OFF, OFF, OFF, c[1], OFF, OFF, OFF]
                variant = rng.choice([-1, 1])
                spinCount = rng.choice([1, 2])
                spinSpeed = (0.05 + 0.2*rng.random())*rng.choice([-1, 1])
                spirals(colors = colors, variant = variant, spinCount = spinCount, spinSpeed = spinSpeed, SURFACE = True, GENERATETOGETHER = True, duration = 9)
            elif variant == 2: pass
            elif variant == 3: pass
            elif variant == 4: pass
        # spirals (Not spinning)
        elif effect == 13:
            for variant in range(1, 5):
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
                spirals(colors = colors, spinCount = 2, spinSpeed = 0, ENDAFTERSPIRALS = True, cycles = 1)
                sleep(0.5)
        # spirals (barbershop style)
        elif effect == 14:
            for i in range(10):
                variant = rng.integers(1, 3)
                if variant == 1: # Two spirals
                    colors = [[RED, WHITE], [BLUE, GREEN], [RED, GREEN], [BLUE, WHITE]
                              , [GREEN, PURPLE], [CYAN, ORANGE], [ORANGE, BLUE], [YELLOW, PURPLE]][rng.integers(0, 8)]
                    spinCount = rng.choice([1, 2, 3, 4])
                elif variant == 2: # More than two spirals
                    colors = [[RED, OFF, OFF, OFF, OFF, GREEN, OFF, OFF, OFF, OFF], [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
                              , [BLUE, OFF, OFF, OFF, OFF, WHITE, OFF, OFF, OFF, OFF]][rng.integers(0, 3)]
                    spinCount = rng.choice([1, 2])
                spinSpeed = (0.1 + 0.2*rng.random()) * rng.choice([-1, 1])
                variant = rng.choice([-1, 1])
                spirals(colors = colors, spinSpeed = spinSpeed, spinCount = spinCount, variant = variant, GENERATEINSTANTLY = True, duration = 3)
        # spotlight
        elif effect == 15:
            spotlight(duration = 9)
        # stripedFill
        elif effect == 16:
            stripedFill(duration = 7)
        # twinkle
        elif effect == 17:
            for i in range(3):
                variant = i
                intensity = rng.integers(2, 5)
                if variant == 0:
                    for j in range(5):
                        color = [[50, 50, 50], [50, 0, 0], [0, 0, 50], [50, 0, 50], [0, 25, 50]][j]
                        twinkle(variant = variant, color = color, intensity = intensity, duration = 4)
                else:
                    twinkle(variant = variant, intensity = intensity, duration = 7)
        # wander
        elif effect == 18:
            wander(duration = 9)
        # zSpiral
        elif effect == 19:
            zSpiral(cycles = 1)
            sleep(2)
        # gradient
        elif effect == 20:
            for i in range(3, 5):
                gradient(variant = i, duration = 4.5)
        # rainbow
        elif effect == 21:
            for i in range(2, 5):
                rainbow(variant = i, duration = 4)
        # setAll
        elif effect == 22:
            setAll()
            sleep(3)
        # setAllRandom
        elif effect == 23:
            for variant in range(1, 3):
                if variant == 1:
                    setAllRandom()
                    sleep(3)
                elif variant == 2:
                    setAllRandom(continuous = True, duration = 6)
        # sweep
        elif effect == 24:
            sweep(duration = 9)
        # radialGradient
        elif effect == 25:
            for i in range(3):
                colors = [[RED, GREEN], [GREEN, BLUE], [BLUE, RED]][i]
                radialGradient(colors = colors, duration = 5)
        # pizza
        elif effect == 26:
            pizza()
            sleep(5)
        # rain
        elif effect == 27:
            for variant in range(3):
                if variant < 2:
                    color = [CYAN, BLUE][variant]
                    speed = 0.15 + 0.4*rng.random()
                    wind = -0.3 + 0.6*rng.random()
                elif variant == 3: # Like the matrix
                    color = GREEN
                    speed = 0.15
                    wind = 0
                rain(color = color, speed = speed, wind = wind, duration = 90)
        # fire
        elif effect == 28:
            fire(duration = 90)
        effect += 1

if __name__ == "__main__":
    pass
    show()
