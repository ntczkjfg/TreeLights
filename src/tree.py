from time import time
import platform

import numpy as np

if platform.system() == 'Windows':
    import virtual_tree as neopixel
    import virtual_tree as board
    from virtual_tree import neopixel_write
elif platform.system() == 'Linux':
    import board
    import neopixel
    from new_neopixel_write import neopixel_write
else:
    raise Exception(f'Unknown operating system: {platform.system()}')

LED_PIN = board.D18

class Tree(neopixel.NeoPixel):
    '''The Tree object.  Primary functions:  fill(), clear(), show(), setBrightness(), cycle().
        self.[i] returns the color of the i-th LED and can also be used to set said color.'''
    
    def __init__(self, coordinates):
        # Set this now so super class has access to it
        # Relevant if running on Windows, using FakeTree class
        self.coordinates = coordinates
        super().__init__(LED_PIN, len(coordinates), auto_write = False, pixel_order = 'RGB')
        self._pre_brightness_buffer = np.zeros(self._bytes, dtype=np.uint8)
        self.flags = np.full(self.n, None, dtype=object)
        self.pixels = []
        polar_coordinates = []
        for i, coordinate in enumerate(coordinates):
            self.pixels.append(Pixel(tree = self, index = i, coordinate = np.array(coordinate)))
            polar_coordinates.append([self.pixels[i].r, self.pixels[i].a])
        self.coordinates = np.column_stack((self.coordinates, polar_coordinates))
        total_dist = np.sum(np.sqrt(np.sum((self.coordinates[1:,:3] - self.coordinates[:-1,:3])**2, axis=1)))
        self.x = self.coordinates[:,0]
        self.y = self.coordinates[:,1]
        self.z = self.coordinates[:,2]
        self.r = self.coordinates[:,3]
        self.a = self.coordinates[:,4]
        self.i = np.arange(self.n)
        self.x_min = np.min(self.x)
        self.y_min = np.min(self.y)
        self.z_min = np.min(self.z)
        self.r_min = np.min(self.r)
        self.a_min = np.min(self.a)
        self.x_max = np.max(self.x)
        self.y_max = np.max(self.y)
        self.z_max = np.max(self.z)
        self.r_max = np.max(self.r)
        self.a_max = np.max(self.a)
        self.x_range = self.x_max - self.x_min
        self.y_range = self.y_max - self.y_min
        self.z_range = self.z_max - self.z_min
        self.r_range = self.r_max - self.r_min
        self.a_range = self.a_max - self.a_min
        self.x_mid = self.x_min + 0.5 * self.x_range
        self.y_mid = self.y_min + 0.5 * self.y_range
        self.z_mid = self.z_min + 0.5 * self.z_range
        self.r_mid = self.r_min + 0.5 * self.r_range
        self.a_mid = self.a_min + 0.5 * self.a_range
        
        # Used when recording effects to CSV
        self.frame = 0
        self.start_time = 0
        
        # Used to calculate fps
        self.frames = 0
        
        # Lists of LED indices sorted in various ways, plus determine surface LEDs
        self.sorted_i = np.arange(self.n) # Sorted by Index
        self.sorted_x = np.argsort(self.coordinates[:, 0]) # Sorted by x-coordinate
        self.sorted_y = np.argsort(self.coordinates[:, 1]) # Sorted by y-coordinate
        self.sorted_z = np.argsort(self.coordinates[:, 2]) # Sorted by z-coordinate
        self.sorted_r = np.argsort(self.coordinates[:, 3]) # Sorted by radius
        self.sorted_a = np.argsort(self.coordinates[:, 4]) # Sorted by angle (angle of 0 is along positive x-axis)
        self.indices = np.array([self.sorted_i, self.sorted_x, self.sorted_y, self.sorted_z, self.sorted_r, self.sorted_a])
        # Following four variables are used to identify LEDs that are on the surface of the tree
        # Assumes tree is conical - calculates linear equation for radius based on z-coordinate
        # Tries to account for outliers
        max_r = self[self.sorted_r[-self.n // 10]].r
        max_z = self[self.sorted_z[-8]].z
        m = -max_r / max_z
        b = max_r
        self.s = (self.r + 0.1) > (m*self.z + b - 0.05)
        coords_squared = np.sum(self.coordinates[:,:3]**2, axis = 1, keepdims = True)
        avg_dist = total_dist / (self.n - 1)
        dists = (coords_squared + coords_squared.T - 2*np.dot(self.coordinates[:, :3], self.coordinates[:, :3].T)) < avg_dist**2
        for i in range(self.n):
            neighbors = list(set(np.where(dists[i])[0].tolist()).union({i-1, i+1}).difference({-1, i, self.n}))
            self[i].neighbors = neighbors
        # neopixel_write is optimized from adafruit neopixel library, but new function may be hardware-specific
        # returns True if initialization succeeds, False otherwise
        # Falls back to hardware-agnostic version if it fails
        self.NEW_NEOPIXEL_WRITE = neopixel_write(self.pin, self._buffer)
        if self.NEW_NEOPIXEL_WRITE == 25:
            self.VIRTUAL_TREE = True
            self.NEW_NEOPIXEL_WRITE = False
        else:
            self.VIRTUAL_TREE = False
    
    def cycle(self, indices = None, variant = 0, backwards = False, speed = 400, duration = 99999):
        start_time = time()
        last_time = start_time
        if speed == 0: return
        if speed < 0:
            speed *= -1
            backwards = not backwards
        if indices is None:
            indices = self.indices[variant]
        if backwards:
            a = -1
            b = 1
        else:
            a = 1
            b = 0
        while (t := time()) - start_time < duration:
            dt = t - last_time
            last_time = t
            first_count = min(int(speed * dt), self.n)
            if first_count == 0:
                last_time = t - dt
                continue
            first = [self.pixels[indices[a*(i+b)]].color for i in range(first_count)]
            for i in range(self.n - first_count):
                self.pixels[indices[a*(i+b)]].set_color(self.pixels[indices[a * (i + first_count + b)]].color)
            for i in range(first_count):
                self.pixels[indices[a*(-(first_count - i) + b)]].set_color(first[i])
            self.show()
    
    def fade(self, halflife = 0.25, dt = .05):
        f = 0.5**(dt/halflife)
        self._buffer = np.multiply(self._pre_brightness_buffer, f).astype(np.uint8)
    
    def fill(self, color):
        self._buffer = np.tile(color, self.n).astype(np.uint8)
    
    def clear(self, update = True, flags_only = False):
        self.flags = np.full(self.n, None, dtype=object)
        if not flags_only:
            self._buffer = np.zeros(self._bytes, dtype=np.uint8)
        if update and not flags_only: self.show()
    
    @property
    def _buffer(self):
        return (self._pre_brightness_buffer*self.brightness).astype(np.uint8)
    
    @_buffer.setter
    def _buffer(self, buffer):
        if len(buffer) != self._bytes:
            raise ValueError
        self._pre_brightness_buffer = np.array(buffer, dtype=np.uint8)
    
    def show(self, record = False, max_frames = 100000):
        if self.NEW_NEOPIXEL_WRITE:
            neopixel_write(self.pin, self._buffer)
        else:
            if self.VIRTUAL_TREE:
                self._transmit(self._buffer)
            else:
                self._transmit(bytearray(self._buffer.tobytes()))
        # neopixel_write is optimized for my tree (increases fps by about 50%), but may be hardware-specific
        # If initialization fails this falls back to self._transmit which should work for any supported hardware
        self.frames += 1
        if record and self.frame < max_frames:
            name = 'forMatt'
            self.record_to_csv(name)
    
    def record_to_csv(self, name):
        path = '/home/pi/Desktop/TreeLights/CSVs/'
        if self.frame == 0: # New file
            self.start_time = round(time(), 3)
            with open(path + 'template.csv', 'r') as f:
                template = f.read()
            with open(path + name + '.csv', 'w') as f:
                f.write(template)
        if self.frame % 100 == 0:
            print(self.frame, 'frames in', time() - self.start_time, 'seconds.')
        data = str(self.frame) + ','
        for i in range(self.n):
            data += str(self._buffer[3*i]) + ',' # R
            data += str(self._buffer[3*i+1]) + ',' # G
            data += str(self._buffer[3*i+2]) + ',' # B
        with open(path + name + '.csv', 'a') as f:
            f.write(data[:-1] + '\n') # Remove last comma, add linefeed
        self.frame += 1
    
    def __repr__(self):
        return str(self.pixels)
    
    def __getitem__(self, key):
        return self.pixels[key]
    
    def __setitem__(self, index, color):
        if index < 0:
            index += self.n
        if index >= self.n or index < 0:
            raise IndexError
        self._pre_brightness_buffer[3*index:3*index+3] = color

    def __iter__(self):
        return iter(self.pixels)
    
    def set_colors(self, buffer):
        if len(buffer) != self._bytes:
            raise ValueError
        self._buffer = np.array(buffer, dtype=np.uint8)
    
    @neopixel.NeoPixel.brightness.setter
    def brightness(self, value):
        value = min(max(value, 0.0), 1.0)
        change = value - self._brightness
        if -0.001 < change < 0.001:
            return
        self._brightness = value
        self.show()

class Pixel:
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
        self.neighbors = []
    
    @property
    def flag(self): return self.tree.flags[self.i]
    @flag.setter
    def flag(self, value): self.tree.flags[self.i] = value
    @property
    def color(self): return self.tree._pre_brightness_buffer[3*self.i:3*self.i + 3]
    @color.setter
    def color(self, color): self.set_color(color)
    @property
    def x(self): return self.coordinate[0]
    @property
    def y(self): return self.coordinate[1]
    @property
    def z(self): return self.coordinate[2]
    @property
    def surface(self): return self.tree.s[self.i]
    
    def set_color(self, color):
        self.tree[self.i] = color
    
    def __repr__(self):
        return str([self.index, self.coordinate, self.color])
