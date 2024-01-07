import numpy as np
from time import sleep, time
import platform
if platform.system() == "Windows":
    from FakeTree import FakeTree as neopixel
    import FakeTree as board
elif platform.system() == "Linux":
    import board
    import neopixel
else:
    print("Unknown operating system.", platform.system())

LED_PIN = board.D18

class Tree(neopixel.NeoPixel):
    """The Tree object.  Primary functions:  fill(), clear(), show(), setBrightness(), cycle().
        self.[i] returns the color of the i-th LED and can also be used to set said color."""
    
    def __init__(self, coordinates):
        super().__init__(LED_PIN, len(coordinates), auto_write = False, pixel_order = "RGB")
        self._pre_brightness_buffer = np.zeros(self._bytes, dtype=np.uint8)
        self._post_brightness_buffer = None
        self.flags = np.full(self.n, None, dtype=object)
        self.pixels = []
        self.coordinates = []
        for i, coordinate in enumerate(coordinates):
            self.pixels.append(Pixel(tree = self, index = i, coordinate = np.array(coordinate)))
            self.coordinates.append([self.pixels[i].r, self.pixels[i].a])
        self.coordinates = np.column_stack((coordinates, self.coordinates))
        totalDist = np.sum(np.sqrt(np.sum((self.coordinates[1:,:3] - self.coordinates[:-1,:3])**2, axis=1)))
        self.x = self.coordinates[:,0]
        self.y = self.coordinates[:,1]
        self.z = self.coordinates[:,2]
        self.r = self.coordinates[:,3]
        self.a = self.coordinates[:,4]
        self.xMin = np.min(self.x)
        self.yMin = np.min(self.y)
        self.zMin = np.min(self.z)
        self.rMin = np.min(self.r)
        self.aMin = np.min(self.a)
        self.xMax = np.max(self.x)
        self.yMax = np.max(self.y)
        self.zMax = np.max(self.z)
        self.rMax = np.max(self.r)
        self.aMax = np.max(self.a)
        avgDist = totalDist / (self.n - 1)
        self.xRange = self.xMax - self.xMin
        self.yRange = self.yMax - self.yMin
        self.zRange = self.zMax - self.zMin
        self.rRange = self.rMax - self.rMin
        self.aRange = self.aMax - self.aMin
        
        # Used when recording effects to CSV
        self.frame = 0
        self.startTime = 0
        
        # Used to calculate fps
        self.frames = 0
        
        # Lists of LED indices sorted in various ways, plus determine surface LEDs
        self.sortedI = np.arange(self.n) # Sorted by Index
        self.sortedX = np.argsort(self.coordinates[:,0]) # Sorted by x-coordinate
        self.sortedY = np.argsort(self.coordinates[:,1]) # Sorted by y-coordinate
        self.sortedZ = np.argsort(self.coordinates[:,2]) # Sorted by z-coordinate
        self.sortedR = np.argsort(self.coordinates[:,3]) # Sorted by radius
        self.sortedA = np.argsort(self.coordinates[:,4]) # Sorted by angle (angle of 0 is along positive x-axis)
        self.indices = np.array([self.sortedI, self.sortedX, self.sortedY, self.sortedZ, self.sortedR, self.sortedA])
        # Following four variables are used to identify LEDs that are on the surface of the tree
        # Assumes tree is conical - calculates linear equation for radius based on z-coordinate
        # Tries to account for outliers
        maxR = self[self.sortedR[-self.n // 10]].r
        maxZ = self[self.sortedZ[-8]].z
        m = -maxR / maxZ
        b = maxR
        surface = self.r > (m*self.z + b - 0.05)
        for i in range(self.n):
            dists = np.sqrt((self[i].x - self.x)**2 + (self[i].y - self.y)**2 + (self[i].z - self.z)**2)
            neighbors = list(set(np.where(dists < avgDist)[0].tolist()).union({i-1, i+1}).difference({-1, i, self.n}))
            self[i].neighbors = neighbors
            if surface[i]:
                self.pixels[i].surface = True
        self.s = surface
    
    def cycle(self, index = None, variant = 0, backwards = False, speed = 400, duration = 99999):
        startTime = time()
        lastTime = startTime
        if speed == 0: return
        if speed < 0:
            speed *= -1
            backwards = not backwards
        if index is None:
            index = self.indices[variant]
        if backwards:
            a = -1
            b = 1
        else:
            a = 1
            b = 0
        frames = 0
        while time() - startTime < duration:
            dt = time() - lastTime
            lastTime = time()
            firstCount = int(speed * dt)
            first = [self.pixels[index[a*(i+b)]].color for i in range(firstCount)]
            for i in range(self.n - firstCount):
                self.pixels[index[a*(i+b)]].setColor(self.pixels[index[a*(i + firstCount + b)]].color)
            for i in range(firstCount):
                self.pixels[index[a*(-(firstCount - i) + b)]].setColor(first[i])
            self.show()
            frames += 1
        duration = round(time() - startTime, 2)
        print("cycle:", frames, "frames in", duration, "seconds for", round(frames/duration, 1), "fps")
    def fade(self, halflife = 0.25, dt = .05):
        f = 0.5**(dt/halflife)
        self._brightness_buffer = np.multiply(self._pre_brightness_buffer, f).astype(np.uint8)
    
    def fill(self, color):
        self._brightness_buffer = np.tile(color, self.n).astype(np.uint8)
    
    def clear(self, UPDATE = True, FLAGSONLY = False):
        self.flags = np.full(self.n, None, dtype=object)
        if not FLAGSONLY:
            self._brightness_buffer = np.zeros(self._bytes, dtype=np.uint8)
        if UPDATE and not FLAGSONLY: self.show()
    
    @property
    def _brightness_buffer(self):
        if self._post_brightness_buffer is not None:
            return self._post_brightness_buffer
        return self._pre_brightness_buffer
    
    @_brightness_buffer.setter
    def _brightness_buffer(self, buffer):
        if len(buffer) != self._bytes:
            raise ValueError
        self._pre_brightness_buffer = np.array(buffer, dtype=np.uint8)
        if self._post_brightness_buffer is not None:
            self._post_brightness_buffer = np.multiply(self._pre_brightness_buffer, self._brightness).astype(np.uint8)
    
    def show(self, record = False, maxFrames = 1000000):
        self._transmit(bytearray(self._brightness_buffer.tobytes()))
        self.frames += 1
        if record and self.frame < maxFrames:
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
        for i in range(self.n):
            data += str(self._brightness_buffer[3*i]) + "," # R
            data += str(self._brightness_buffer[3*i+1]) + "," # G
            data += str(self._brightness_buffer[3*i+2]) + "," # B
        with open(PATH + name + ".csv", "a") as f:
            f.write(data[:-1] + "\n") # Remove last comma, add linefeed
        self.frame += 1
    
    def __repr__(self):
        return str(self.pixels)
    
    def __str__(self):
        return "Tree object with " + str(self.n) + " LEDs."
    
    def __getitem__(self, key):
        return self.pixels[key]
    
    def __setitem__(self, index, color):
        if index < 0:
            index += self.n
        if index >= self.n or index < 0:
            raise IndexError
        self._pre_brightness_buffer[3*index:3*index+3] = color
        if self._post_brightness_buffer is not None:
            self._post_brightness_buffer = np.multiply(self._pre_brightness_buffer, self._brightness).astype(np.uint8)
    
    def setAll(self, buffer):
        if len(buffer) != self._bytes:
            raise ValueError
        self._brightness_buffer = np.array(buffer, dtype=np.uint8)
    
    @neopixel.NeoPixel.brightness.setter
    def brightness(self, value: float):
        value = min(max(value, 0.0), 1.0)
        change = value - self._brightness
        if -0.001 < change < 0.001:
            return
        self._brightness = value
        if self._brightness >= 0.999:
            self._post_brightness_buffer = None
            self.show()
            return
        self._post_brightness_buffer = np.multiply(self._pre_brightness_buffer, self._brightness).astype(np.uint8)
        self.show()

class Pixel():
    def __init__(self, tree, index, coordinate):
        self.tree = tree
        self.index = index
        self.i = self.index
        self.coordinate = coordinate
        if self.x == 0:
            if self.y > 0:
                self.a = np.pi/2
            elif self.y < 0:
                self.a = 3*np.pi/2
            else:
                self.a = 0
        else:
            self.a = np.arctan(self.y/self.x)# Angles between -π/2 and π/2
            if self.x < 0: self.a += np.pi # Angles between -π/2 and 3π/2
        self.a = self.a % (2*np.pi) # Angles between 0 and 2π
        self.r = (self.x**2 + self.y**2)**0.5
        self.surface = False
        self.neighbors = []
    
    @property
    def flag(self): return self.tree.flags[self.i]
    @flag.setter
    def flag(self, value): self.tree.flags[self.i] = value
    @property
    def color(self): return self.tree._pre_brightness_buffer[3*self.i:3*self.i + 3]
    @color.setter
    def color(self, color): self.setColor(color)
    @property
    def x(self): return self.coordinate[0]
    @property
    def y(self): return self.coordinate[1]
    @property
    def z(self): return self.coordinate[2]
    
    def setColor(self, color):
        self.tree[self.i] = color
    
    def __repr__(self):
        return str([self.index, self.coordinate, self.color])