import numpy as np
from time import sleep, time
import platform
if platform.system() == "Windows":
    from FakeTree import FakeTree as neopixel
    import FakeTree as board
elif platform.system() == "Linux":
    import board
    from neopixel import NeoPixel as neopixel
else:
    print("Unknown operating system.", platform.system())

LED_PIN = board.D18

class Tree:
    """The Tree object.  Primary functions:  fill(), clear(), show(), setBrightness(), cycle().
        self.[i] returns the color of the i-th LED and can also be used to set said color."""
    
    def __init__(self, coordinates):
        self.LEDs = neopixel(LED_PIN, len(coordinates), auto_write = False)
        self.LED_COUNT = len(coordinates)
        self.brightness = 1 # ∈(0, 1]
        self.xMin = 1000
        self.xMax = 0
        self.yMin = 1000
        self.yMax = 0
        self.zMin = 1000
        self.zMax = 0
        self.rMin = 1000
        self.rMax = 0
        self.aMin = 1000
        self.aMax = 0
        self.pixels = []
        self.coordinates = []
        totalDist = 0
        for i, coordinate in enumerate(coordinates):
            if coordinate[0] == 0:
                # Because pixel angle is calculated with arctan, which divides by x
                coordinate[0] = 0.0001
            if i != 0:
                totalDist += ((coordinates[i][0] - coordinates[i-1][0])**2 +
                              (coordinates[i][1] - coordinates[i-1][1])**2 +
                              (coordinates[i][2] - coordinates[i-1][2])**2)**0.5
            self.pixels.append(Pixel(tree = self, index = i, coordinate = np.array(coordinate)))
            self.coordinates.append(coordinate)
            if self.pixels[i].x < self.xMin: self.xMin = self.pixels[i].x
            if self.pixels[i].y < self.yMin: self.yMin = self.pixels[i].y
            if self.pixels[i].z < self.zMin: self.zMin = self.pixels[i].z
            if self.pixels[i].r < self.rMin: self.rMin = self.pixels[i].r
            if self.pixels[i].a < self.aMin: self.aMin = self.pixels[i].a
            if self.pixels[i].x > self.xMax: self.xMax = self.pixels[i].x
            if self.pixels[i].y > self.yMax: self.yMax = self.pixels[i].y
            if self.pixels[i].z > self.zMax: self.zMax = self.pixels[i].z
            if self.pixels[i].r > self.rMax: self.rMax = self.pixels[i].r
            if self.pixels[i].a > self.aMax: self.aMax = self.pixels[i].a
        self.x = np.array([pixel.x for pixel in self])
        self.y = np.array([pixel.y for pixel in self])
        self.z = np.array([pixel.z for pixel in self])
        self.a = np.array([pixel.a for pixel in self])
        self.r = np.array([pixel.r for pixel in self])
        avgDist = totalDist / (self.LED_COUNT - 1)
        self.xRange = self.xMax - self.xMin
        self.yRange = self.yMax - self.yMin
        self.zRange = self.zMax - self.zMin
        
        # Used when recording effects to CSV
        self.frame = 0
        self.startTime = 0
        
        # Lists of LED indices sorted in various ways, plus determine surface LEDs
        self.sortedI = [i for i in range(self.LED_COUNT)] # Sorted by Index
        self.sortedX = sorted(self.sortedI, key = lambda i: self.pixels[i].x) # Sorted by x-coordinate
        self.sortedY = sorted(self.sortedI, key = lambda i: self.pixels[i].y) # Sorted by y-coordinate
        self.sortedZ = sorted(self.sortedI, key = lambda i: self.pixels[i].z) # Sorted by z-coordinate
        self.sortedA = sorted(self.sortedI, key = lambda i: self.pixels[i].a) # Sorted by angle (angle of 0 is along positive x-axis)
        self.sortedR = sorted(self.sortedI, key = lambda i: self.pixels[i].r) # Sorted by radius
        self.indices = [self.sortedI, self.sortedX, self.sortedY, self.sortedZ, self.sortedA, self.sortedR]
        # Following four variables are used to identify LEDs that are on the surface of the tree
        # Assumes tree is conical - calculates linear equation for radius based on z-coordinate
        # Tries to account for outliers
        maxR = self[self.sortedR[-self.LED_COUNT // 10]].r
        maxZ = self[self.sortedZ[-8]].z
        m = -maxR / maxZ
        b = maxR
        for i in range(self.LED_COUNT):
            for pixel in self: # This loop identifies neighbors to each pixel - very slow because of nested for loops
                if pixel.index != i: # Don't count an LED as its own neighbor
                    if abs(pixel.index - i) == 1: # Automatically count neighbors on the string
                        self[i].neighbors.append(pixel.index)
                        continue
                    d = ((self[i].x - pixel.x)**2 + (self[i].y - pixel.y)**2 + (self[i].z - pixel.z)**2)**0.5
                    if d <= avgDist:
                        self[i].neighbors.append(pixel.index)
            # Might as well set these now
            self.pixels[self.sortedX[i]].xIndex = i
            self.pixels[self.sortedY[i]].yindex = i
            self.pixels[self.sortedZ[i]].zIndex = i
            self.pixels[self.sortedA[i]].aIndex = i
            self.pixels[self.sortedR[i]].rIndex = i
            if self.pixels[i].r > (m * self.pixels[i].z + b) - 0.05:
                self.pixels[i].surface = True
        self.s = np.array([pixel.surface for pixel in self])
    
    # This function exists because pickling the tree fails with a RecursionError exception if the neighbors
    # are stored as Pixels - so they're stored as indices, pickled, then changed to Pixels
    def finishNeighbors(self):
        for pixel in self:
            for i in range(len(pixel.neighbors)):
                pixel.neighbors[i] = self[pixel.neighbors[i]]
    
    def cycle(self, variant = 0, backwards = False, step = 10, duration = 99999):
        startTime = time()
        if step == 0: return
        if step < 0:
            step *= -1
            backwards = not backwards
        index = self.indices[variant]
        if backwards:
            a = -1
            b = 1
        else:
            a = 1
            b = 0
        while time() - startTime < duration:
            first = [self.pixels[index[a*(i+b)]].color for i in range(step)]
            for i in range(self.LED_COUNT - step):
                self.pixels[index[a*(i+b)]].setColor(self.pixels[index[a*(i + step + b)]].color)
            for i in range(step):
                self.pixels[index[a*(-(step - i) + b)]].setColor(first[i])
            self.show()
    
    def fade(self, factor = 0.5):
        for pixel in self:
            pixel.setColor([factor * pixel.color[0],
                            factor * pixel.color[1],
                            factor * pixel.color[2]])
    
    """Accepts a value from 0 to 1"""
    def setBrightness(self, brightness):
        if brightness > 0 and brightness <= 1:
            self.brightness = brightness
            for pixel in self:
                pixel.setColor(pixel.color)
            self.show()
        else:
            raise ValueError
    
    def fill(self, color):
        for pixel in self.pixels:
            pixel.setColor(color)
    
    def clear(self, UPDATE = True, FLAGSONLY = False):
        for pixel in self.pixels:
            pixel.flag = 0
            if FLAGSONLY: continue
            pixel.setColor([0, 0, 0])
        if UPDATE and not FLAGSONLY: self.show()
    
    def show(self, record = False, maxFrames = 1000000):
        self.LEDs.show()
        if record and self.frame < maxFrames:
            import inspect
            name = inspect.stack()[1].function
            name = "forMatt"
            self.recordToCSV(name)
    
    def recordToCSV(self, name):
        PATH = "/home/pi/Desktop/TreeLights/CSVs/"
        if self.frame == 0: # New file
            self.startTime = round(time(), 3)
            with open(PATH + "template.csv", "r") as f:
                template = f.read()
            with open(PATH + name + ".csv", "w") as f:
                f.write(template)
        if self.frame % 100 == 0:
            print(self.frame, "frames in", time() - self.startTime, "seconds.")
        data = str(self.frame) + ","
        for i in range(self.LED_COUNT):
            # Accessing colors directly from self.LEDs because accessing from Pixel object
            # doesn't account for brightness, plus values from here are already ints
            data += str(self.LEDs[i][1]) + "," # R
            data += str(self.LEDs[i][0]) + "," # G
            data += str(self.LEDs[i][2]) + "," # B
        with open(PATH + name + ".csv", "a") as f:
            f.write(data[:-1] + "\n") # Remove last comma, add linefeed
        self.frame += 1
    
    def __repr__(self):
        return str(self.pixels)
    
    def __str__(self):
        return "Tree object with " + str(self.LED_COUNT) + " LEDs."
    
    def __len__(self):
        return self.LED_COUNT
    
    def __getitem__(self, key):
        return self.pixels[key]
    
    def __setitem__(self, key, color):
        self.pixels[key].setColor(color)
    
    def __iter__(self):
        self.iter = 0
        return self
    
    def __next__(self):
        if self.iter < self.LED_COUNT:
            result = self.pixels[self.iter]
            self.iter += 1
            return result
        else:
            raise StopIteration

class Pixel():
    """Description"""
    
    def __init__(self, tree, index, coordinate):
        self.tree = tree
        self.index = index
        self.i = self.index
        self.coordinate = coordinate
        self.coord = self.coordinate
        self.c = self.coordinate
        self.x = self.coordinate[0]
        self.y = self.coordinate[1]
        self.z = self.coordinate[2]
        self.a = np.arctan(self.y/self.x)# Angles between -π/2 and π/2
        if self.x < 0: self.a += np.pi # Angles between -π/2 and 3π/2
        self.a = self.a % (2*np.pi) # Angles between 0 and 2π
        self.r = (self.x**2 + self.y**2)**0.5
        self.color = [0, 0, 0]
        self.xIndex = -1
        self.yIndex = -1
        self.zIndex = -1
        self.aIndex = -1
        self.rIndex = -1
        self.surface = False
        self.flag = 0
        self.neighbors = []
    
    def setColor(self, color):
        self.color = color
        self.tree.LEDs[self.index] = [self.tree.brightness * k for k in color]
    
    def __repr__(self):
        return str([self.index, self.coordinate, self.color])
    
