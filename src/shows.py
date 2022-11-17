from Common_Variables import rng, tree
from LED_Control import *
from StaticEffects import *
from Colors import *
from time import sleep


# Puts on a curated show of effects
def show(setEffect = None):
    oldEffect = 0
    effect = 0
    while True:
        while effect == oldEffect: effect = rng.integers(1, 28, 1)[0]
        oldEffect = effect
        if setEffect != None: effect = setEffect
        if effect == 1: # cylinder
            cylinder(duration = 90)
        elif effect == 2: # cylon
            variant = rng.integers(1, 5, 1)[0]
            color = RED if variant < 4 else COLORS
            cylon(color = color, duration = 60)
        elif effect == 3: # fallingColors
            fallingColors(duration = 90)
        elif effect == 4: # bouncingRainbowBall
            bouncingRainbowBall(duration = 90)
        elif effect == 5: # pulsatingSphere
            pulsatingSphere(duration = 90)
        elif effect == 6: # randomFill
            randomFill(cycles = 1)
        elif effect == 7: # randomPlanes
            randomPlanes(duration = 90)
        elif effect == 8: # sequence
            sequence(cycles = 1)
            sleep(5)
        elif effect == 9: # snake
            snake(cycles = 1)
        elif effect == 10: # spinningPlane (spinner variant)
            colors = list(rng.choice([[WHITE, BLUE], [RED, GREEN], [CYAN, WHITE], [GREEN, BLUE]]))
            variant = rng.integers(1, 5, 1)[0]
            spinningPlane(colors = colors, variant = 0, SPINNER = True, duration = 50)
        elif effect == 11: # spinningPlane
            variant = rng.choice([0, 0, 0, 1, 2, 2, 2, 3])
            speed = 0.1 + 0.25 * rng.random()
            width = 0.1 + 0.2 * rng.random()
            height = rng.choice([0, 0, 0, tree.zMax / 2, tree.zMax / 2, tree.zMax / 2, tree.zMax / 2, tree.zMax / 2, tree.zMax])
            twoColors = rng.choice([True, False, False])
            background = rng.choice([True, False, False])
            spinningPlane(variant = variant, speed = speed
                          , width = width, height = height
                          , twoColors = twoColors, background = background
                          , duration = 90)
        elif effect == 12: # spirals
            variant = rng.integers(1, 5, 1)[0]
            if variant == 1: spirals(spinSpeed = 0, ENDAFTERSPIRALS = True, cycles = 1)
            elif variant == 2: spirals(colors = [GREEN, RED], spinCount = 5, spinSpeed = 0, ENDAFTERSPIRALS = True, cycles = 1)
            elif variant == 3: spirals(colors = [BLUE, WHITE, CYAN, WHITE], spinSpeed = 0, ENDAFTERSPIRALS = True, cycles = 1)
            elif variant == 4: spirals(colors = [RED, WHITE, BLUE], spinSpeed = 0, ENDAFTERSPIRALS = True, cycles = 1)
            sleep(5)
        elif effect == 13: # spotlight
            spotlight(duration = 90)
        elif effect == 14: # stripedFill
            stripedFill(duration = 50)
        elif effect == 15: # twinkle
            variant = rng.integers(0, 3, 1)[0]
            intensity = rng.choice(5)
            if variant == 0:
                color = list(rng.choice([[50, 50, 50], [50, 50, 50], [50, 0, 0], [0, 0, 50], [0, 0, 50], [50, 0, 50], [0, 25, 50]]))
                twinkle(variant = variant, color = color, intensity = intensity, duration = 90)
            else:
                twinkle(variant = variant, intensity = intensity, duration = 90)
        elif effect == 16: # wander
            wander(duration = 90)
        elif effect == 17: # zSpiral
            zSpiral(cycles = 1)
            sleep(10)
        elif effect == 18: # gradient
            gradient(duration = 90)
        elif effect == 19: # rainbow
            rainbow(duration = 90)
        elif effect == 20: # setAll
            setAll()
            sleep(10)
        elif effect == 21: # setAllRandom
            variant = rng.integers(1, 3, 1)[0]
            if variant == 1:
                setAllRandom()
                sleep(10)
            elif variant == 2:
                setAllRandom(continuous = True, duration = 60)
        elif effect == 22: # sweep
            sweep(duration = 90)
        elif effect == 23: # radialGradient
            colors = list(rng.choice([[RED, GREEN], [GREEN, BLUE], [BLUE, RED]]))
            radialGradient(colors = colors, duration = 90)
        elif effect == 24: # spirals (barbershop style)
            variant = rng.integers(1, 3, 1)[0]
            if variant == 1:
                colors = [[RED, WHITE], [BLUE, GREEN], [RED, GREEN], [BLUE, WHITE]
                          , [GREEN, PURPLE], [CYAN, ORANGE], [ORANGE, BLUE], [YELLOW, PURPLE]][rng.integers(0, 8, 1)[0]]
                spinCount = rng.choice([1, 2, 3, 4])
            elif variant == 2:
                colors = [[RED, OFF, OFF, OFF, OFF, GREEN, OFF, OFF, OFF, OFF], [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
                          , [BLUE, OFF, OFF, OFF, OFF, WHITE, OFF, OFF, OFF, OFF]][rng.integers(0, 3, 1)[0]]
                spinCount = rng.choice([1, 2])
            spinSpeed = (0.1 + rng.random()*0.2)*rng.choice([-1, 1])
            variant = rng.choice([-1, 1])
            spirals(colors = colors, spinSpeed = spinSpeed, spinCount = spinCount, variant = variant, GENERATEINSTANTLY = True, duration = 3)
        elif effect == 25: # pizza
            pizza()
            sleep(10)
        elif effect == 26: # rain
            color = list(rng.choice([GREEN, CYAN, CYAN, BLUE, BLUE]))
            rain(color = color, duration = 90)
        elif effect == 27: # fire
            fire(duration = 90)

# Shows off short versions of most effects
def quickShow():
    sleep(5) # Get your camera ready
    print("cylinder")
    cylinder(duration = 10)
    print("cylon")
    color = list(rng.choice([RED, RED, RED, COLORS]))
    cylon(color = color, duration = 10)
    print("spirals")
    spirals(colors = [BLUE, WHITE, CYAN, WHITE], GENERATEINSTANTLY = True, cycles = 1)
    print("fallingColors")
    fallingColors(duration = 30)
    print("bouncingRainbowBall")
    bouncingRainbowBall(duration = 15)
    print("pulsatingSphere")
    pulsatingSphere(duration = 20)
    print("randomFill")
    randomFill(cycles = 1)
    print("spirals")
    spirals(colors = [GREEN, RED], spinCount = 5, cycles = 1)
    print("randomPlanes")
    randomPlanes(duration = 15)
    print("sequence")
    sequence(cycles = 1)
    print("rain")
    rain(color = CYAN, duration = 8)
    print("snake")
    snake(cycles = 1)
    print("spinningPlane")
    colors = list(rng.choice([[WHITE, BLUE], [RED, GREEN], [CYAN, WHITE], [GREEN, BLUE]]))
    spinningPlane(colors = colors, SPINNER = True, duration = 10)
    print("spinningPlane")
    for i in range(5):
        variant = rng.choice([0, 0, 0, 1, 2, 2, 2, 3])
        speed = 0.1 + 0.25 * rng.random()
        width = 0.1 + 0.2 * rng.random()
        height = rng.choice([0, 0, 0, tree.zMax / 2, tree.zMax / 2, tree.zMax / 2, tree.zMax / 2, tree.zMax / 2, tree.zMax])
        twoColors = rng.choice([True, False, False])
        background = rng.choice([True, False, False])
        spinningPlane(variant = variant, speed = speed
                      , width = width, height = height
                      , twoColors = twoColors, background = background
                      , duration = 4)
    print("spirals")
    spirals(cycles = 1)
    print("setAllRandom")
    setAllRandom(continuous = True, duration = 10)
    print("sweep")
    sweep(duration = 10)
    print("spotlight")
    spotlight(duration = 15)
    print("stripedFill")
    stripedFill(duration = 8)
    print("twinkle")
    color = list(rng.choice([[50, 50, 50], [50, 50, 50], [50, 0, 0], [0, 0, 50], [0, 0, 50], [50, 0, 50], [0, 25, 50]]))
    intensity = rng.choice(5)
    twinkle(variant = 0, color = color, intensity = intensity, duration = 90)
    print("wander")
    wander(duration = 6)
    print("zSpiral")
    zSpiral(cycles = 1)
    print("gradient")
    gradient(duration = 8)
    print("spirals")
    spirals(colors = [RED, WHITE, BLUE], cycles = 1)
    print("rainbow")
    rainbow(duration = 10)
    print("rain")
    rain(color = BLUE, duration = 8)
    print("setAll")
    setAll()
    sleep(3)
    print("setAllRandom")
    setAllRandom()
    sleep(8)
    print("twinkle")
    intensity = rng.choice(5)
    twinkle(variant = 1, intensity = intensity, duration = 90)
    print("radialGradient")
    colors = list(rng.choice([[RED, GREEN], [GREEN, BLUE], [BLUE, RED]]))
    radialGradient(colors = colors, duration = 15)
    print("spirals")
    for i in range(5):
        variant = rng.integers(1, 3, 1)[0]
        if variant == 1:
            colors = list(rng.choice([[RED, WHITE], [BLUE, GREEN], [RED, GREEN], [BLUE, WHITE], [GREEN, PURPLE], [CYAN, ORANGE], [ORANGE, BLUE], [YELLOW, PURPLE]]))
            spinCount = rng.choice([1, 2, 3, 4])
        elif variant == 2:
            colors = list(rng.choice([[RED, OFF, OFF, OFF, OFF, GREEN, OFF, OFF, OFF, OFF], [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
                                      , [BLUE, OFF, OFF, OFF, OFF, WHITE, OFF, OFF, OFF, OFF]]))
            spinCount = rng.choice([1, 2])
        spinSpeed = (0.1 + rng.random()*0.2)*rng.choice([-1, 1])
        variant = rng.choice([-1, 1])
        spirals(colors = colors, spinSpeed = spinSpeed, spinCount = spinCount, variant = variant, GENERATEINSTANTLY = True, duration = 4)
    print("pizza")
    pizza()
    sleep(5)
    print("twinkle")
    intensity = rng.choice(5)
    twinkle(variant = 2, intensity = intensity, duration = 90)
    print("rain")
    rain(color = GREEN, duration = 8)
    print("fire")
    fire(duration = 8)
#show()