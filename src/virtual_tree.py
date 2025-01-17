import numpy as np
from grapher import Graph
import pygame
import threading
import time

D18 = 0

def neopixel_write(pin, buffer):
    # Just a randomly chosen number that lets the tree know this is, in fact, a virtual tree
    # Done in this odd way because it's also checking something against the real neopixel library
    return 25

class NeoPixel:
    def __init__(self, pin, n, auto_write = False, pixel_order = 'RGB'):
        # These are all used by the Tree class and so must be defined
        self.coordinates = np.array(self.coordinates)
        self.n = n
        self._bytes = 3*self.n
        self.pin = pin
        self._brightness = 1
        # This will get updated with new colors any time an effect sends a frame
        self.colors = np.zeros((1200, 3))
        # Used to try to match fps to real-life - otherwise it's far higher here
        fps_target = 22.8
        self.seconds_per_frame = 1 / fps_target
        # Generates a christmas tree and stores its branch positions here
        self.branches = None
        # Following is just used to set up the virtual tree window nicely and start its thread
        highest = np.max(self.coordinates[:, 2])
        midpoint = highest / 2
        width = 400
        height = width * midpoint
        self.virtual_tree = Graph(points = self.coordinates[:, :3], update_func = self.draw,
                                  perspective_point = [10, 0, midpoint], screen_width = 0.25,
                                  width = width, height = height, title = 'TreeLights')
        thread = threading.Thread(target = self.virtual_tree.run)
        thread.start()
        self.make_branches()

    def draw(self, points_projected):
        if points_projected:
            self.projected_branches = self.virtual_tree.project_points(self.branches)
            self.virtual_tree.points_projected = False
        self.virtual_tree.screen.fill((35, 35, 35))
        pygame.draw.line(self.virtual_tree.screen, (100, 0, 20), self.projected_branches[-4], self.projected_branches[-3], 8)
        pygame.draw.line(self.virtual_tree.screen, (255, 0, 0), self.projected_branches[-2], self.projected_branches[-1], 5)
        for i in range(len(self.projected_branches)//2 - 2):
            p1 = self.projected_branches[2*i]
            p2 = self.projected_branches[2*i+1]
            pygame.draw.line(self.virtual_tree.screen, (0, 64, 0), p1, p2, 3)
        if self.virtual_tree.draw_axes:
            pygame.draw.line(self.virtual_tree.screen, (0, 0, 0), self.axes[0], self.axes[1], 2)
            pygame.draw.line(self.virtual_tree.screen, (0, 0, 0), self.axes[2], self.axes[3], 2)
            pygame.draw.line(self.virtual_tree.screen, (0, 0, 0), self.axes[4], self.axes[5], 2)
        for i, point in enumerate(self.virtual_tree.projected_points):
            size = self.virtual_tree.sizes[i]
            if point[0] < -size or point[0] > self.virtual_tree.width + size or point[1] < -size or point[1] > self.virtual_tree.height + size:
                continue
            color = self.colors[i]
            pygame.draw.circle(self.virtual_tree.screen, color, point, size)
        pygame.display.flip()
    
    # Creates tree-like branches
    def make_branches(self, num_branches=300):
        # Define the boundaries of the tree cone
        max_z = np.max(self.coordinates[:, 2]) * 1.1
        min_z = 0
        # max_r and min_r are as factors of the radius of the idealized
        # tree cone based on max_z and min_z
        max_r = 1.5
        min_r = 1
        # z-values and theta-values are spaced perfectly evenly, then paired
        # randomly.  Combined with a large min_r value above, this helps
        # the tree look fuller with much fewer branches, allowing num_branches
        # to be smaller, reducing branch-related lag
        zs = np.linspace(min_z, max_z, num_branches)
        thetas = np.linspace(0, 2*np.pi, num_branches)
        np.random.shuffle(thetas)
        branch_dirs = np.column_stack((zs, thetas))
        self.branches = []
        for branch in branch_dirs:
            z = branch[0]
            theta = branch[1]
            r = np.random.uniform(min_r, max_r) * (1 - z / max_z)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            self.branches.append([0, 0, z])
            self.branches.append([x, y, z - 0.1])
        # Trunk
        self.branches.append([0, 0, 0])
        self.branches.append([0, 0, max_z])
        # Big red line at the positive x-axis, for orienting
        self.branches.append([0, 0, 0])
        self.branches.append([2, 0, 0])
        self.branches = np.array(self.branches)
        self.projected_branches = self.virtual_tree.project_points(self.branches)
    
    def _transmit(self, colors):
        self.colors = colors.reshape(1200, 3)
        time.sleep(self.seconds_per_frame)
    
    @property
    def brightness(self):
        # Always have the virtual tree at full brightness
        return 1
    
    def __len__(self):
        return self.n
