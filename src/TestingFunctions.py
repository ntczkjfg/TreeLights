# Has each light blink out its index number in binary
def binary(SLEEP = 1, backwards = False):
    maxLength = len(bin(tree.LED_COUNT - 1)[2:])
    binaryReps = [(maxLength * "0" + bin(i)[2:])[-maxLength:] for i in range(tree.LED_COUNT)]
    if backwards: binaryReps = [rep[::-1] for rep in binaryReps]
    for d in range(maxLength):
        for i in range(tree.LED_COUNT):
            if binaryReps[i][d] == "0":
                tree[i] = RED
            else:
                tree[i] = GREEN
        tree.show()
        sleep(SLEEP)
        tree.clear()
        sleep(SLEEP)

# Turns on lights one-by-one in the cardinal directions
def cardinalTest(colors = None):
    if colors == None:
        Color = lambda: rng.integers(0, 256, 3)
    else:
        if type(colors[0]) != list:
            colors = [colors]
        Color = lambda: rng.choice(colors)
    while True:
        color = Color()
        tree.clear()
        for i in tree.sortedX:
            tree[i] = color
            tree.show()
        sleep(1)
        color = Color()
        tree.clear()
        for i in tree.sortedY:
            tree[i] = color
            tree.show()
        sleep(1)
        color = Color()
        tree.clear()
        for i in tree.sortedZ:
            tree[i] = color
            tree.show()
        sleep(1)

# Sequentially shows all LEDs and their "connected" neighbors
def connectivityTest():
    totalConnections = 0
    loneLEDs = 0
    poorlyConnected = 0
    for pixel in tree:
        connections = len(pixel.neighbors)
        totalConnections += connections
        pixel.setColor(GREEN)
        if connections < 4:
            poorlyConnected += 1
            pixel.setColor(YELLOW)
        if connections == 2:
            loneLEDs += 1
            pixel.setColor(RED)
    print(totalConnections, "connections among", tree.LED_COUNT, "with", loneLEDs, "neighborless LEDs and", poorlyConnected,
          "poorly connected LEDs, and an average of", totalConnections/tree.LED_COUNT, "connections per LED")
    tree.show()
    input()
    while True:
        for pixel in tree:
            tree.clear(False)
            pixel.setColor(RED)
            for neighbor in pixel.neighbors:
                neighbor.setColor(GREEN)
            tree.show()
            input()

# Continuously updates all LEDs with a color - useful when stringing the tree
def continuousUpdate(color = WHITE):
    if color is not None: tree.fill(color)
    while True:
        tree.show()

# Lights up thin planar slices of the tree in cardinal directions
def planarTest():
    sections = 20
    zRange = tree.zRange / sections
    xRange = tree.xRange / sections
    yRange = tree.yRange / sections
    for z in np.linspace(tree.zMin, tree.zMax, sections + 1):
        continue
        tree.clear(False)
        for pixel in tree:
            if pixel.coordinate[2] >= z and pixel.coordinate[2] <= z + zRange:
                pixel.setColor(WHITE)
        tree.show()
        print("Showing z from", round(z, 5), "to", round(z + zRange, 5))
        input()
    for x in np.linspace(tree.xMin, tree.xMax, sections + 1):
        tree.clear(False)
        for pixel in tree:
            if pixel.coordinate[0] >= x and pixel.coordinate[0] <= x + xRange:
                pixel.setColor(WHITE)
        tree.show()
        print("Showing x from", round(x, 5), "to", round(x + xRange, 5))
        input()
    for y in np.linspace(tree.yMin, tree.yMax, sections + 1):
        continue
        tree.clear(False)
        for pixel in tree:
            if pixel.coordinate[1] >= y and pixel.coordinate[1] <= y + yRange:
                pixel.setColor(WHITE)
        tree.show()
        print("Showing y from", round(y, 5), "to", round(y + yRange, 5))
        input()
    tree.clear()

# Illuminates the interior and surface LEDs on the tree in different colors
def surfaceTest(interior = BLUE, surface = RED):
    setAll(interior)
    for pixel in tree:
        if pixel.surface: pixel.setColor(surface)
    tree.show()