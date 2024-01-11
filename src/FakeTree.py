import pickle
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
trees_directory = os.path.join(parent_directory, "Trees")
coordinates_file = os.path.join(trees_directory, "coordinates.list")
plt.rcParams['toolbar'] = 'None'

# via https://stackoverflow.com/questions/45729092/make-interactive-matplotlib-window-not-pop-to-front-on-each-update-windows-7
# Used to stop window from always being on top
def mypause(interval):
    backend = plt.rcParams['backend']
    if backend in matplotlib.rcsetup.interactive_bk:
        figManager = matplotlib._pylab_helpers.Gcf.get_active()
        if figManager is not None:
            canvas = figManager.canvas
            if canvas.figure.stale:
                canvas.draw()
            canvas.start_event_loop(interval)
            return

D18 = 0

def neopixel_write(pin, buffer):
    return False

class NeoPixel:
    def __init__(self, pin, n, auto_write = False, pixel_order = "RGB"):
        # Load point coordinates from file
        try:
            with open(coordinates_file, "rb") as f:
                self.coordinates = np.array(pickle.load(f))
        except FileNotFoundError:
            rng = np.random.default_rng()
            self.coordinates = []
            while len(self.coordinates) < n:
                point = [rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(0, 4)]
                if point[0]**2 + point[1]**2 <= (1 - point[2]/4)**2:
                    self.coordinates.append(point)
        self.coordinates = np.array(self.coordinates)
        self.n = n
        self._bytes = 3*self.n
        self.pin = pin
        self._brightness = 1
        self.setup = False
        # Create figure
        width = 6
        height = width#np.max(self.coordinates[:, 2])/2 * width
        self.fig = plt.figure(figsize=(width, height), dpi=100)
        # Set title bar
        #self.fig.canvas.set_window_title("TreeLights")
        # I don't want any red to show, but it helps me size the window
        self.fig.set_facecolor('red')
        
        # Create subplot that will contain the points
        self.ax = self.fig.add_subplot(111, projection='3d', aspect='auto')
        self.ax.set_facecolor('lightgray')
        # Add the points, which have initial colors of all black
        self.colors = np.zeros_like(self.coordinates[:,:3])
        self.scatter = self.ax.scatter(self.coordinates[:,0]
                                       , self.coordinates[:,1]
                                       , self.coordinates[:,2]
                                       , c=self.colors)
        
        # Camera is parallel to the xy plane
        self.ax.elev = 0
        # Camera is pointing backward along the positive x-axis
        self.ax.azim = 0
        # Manually determined to be a good value
        self.ax.dist = 8.5
        
        # Adjust axis bounds
        self.ax.set_xlim3d(-1, 1)
        self.ax.set_ylim3d(-1, 1)
        self.ax.set_zlim3d(0, np.max(self.coordinates[:,2]))
        
        # Set aspect ratio
        self.ax.set_box_aspect((1, 1, np.max(self.coordinates[:,2]/2)))
        
        # Hide axes and gridlines
        self.ax.set_axis_off()
        self.ax.grid(False)
        self.cam = (self.ax.azim, self.ax.elev, self.ax.dist)
        
        # Let scrolling zoom in/out
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        
        # Adjust plot layout to remove bezels
        self.fig.tight_layout()
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        
        # Closer points larger, further points smaller
        self.update_point_sizes()
        
        # Draw the branches of the tree
        self.make_branches()
        
        # Draw the trunk of the tree
        self.ax.plot([0, 0], [0, 0], [0, 3.5], linewidth = 3, c='brown')
        
        # Show the plot - need `block=False` to not lock the thread
        plt.show(block=False)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        pass
    
    # Update the display with any changes to the point colors
    def _transmit(self, buffer):
        if self.setup == False:
            self.setup = True
            return True
        self.colors = np.frombuffer(buffer, dtype=np.uint8).reshape(-1, 3)/255
        if (self.ax.azim, self.ax.elev, self.ax.dist) != self.cam:
            self.cam = (self.ax.azim, self.ax.elev, self.ax.dist)
            self.update_point_sizes()
        self.scatter.set_facecolors(self.colors)
        plt.draw()
        mypause(0.00001)
    
    # Change a color without updating it on the display
    def update_colors(self, colors):
        colors = [[color[1], color[0], color[2]] for color in colors]
        self.colors = colors
    
    # Makes sure points closer to the camera are larger,
    # and points further from the camera are smaller
    def update_point_sizes(self):
        # Convert camera's position from spherical coordinates to rectangular
        x = self.ax.dist * np.cos(np.radians(self.ax.elev)) * np.cos(np.radians(self.ax.azim))
        y = self.ax.dist * np.cos(np.radians(self.ax.elev)) * np.sin(np.radians(self.ax.azim))
        z = self.ax.dist * np.sin(np.radians(self.ax.elev))
        camera_pos = (x, y, z)
        # Calculate distance from camera to each point the pythagorean way
        dists = np.sqrt(np.sum((self.coordinates[:,:3] - camera_pos)**2, axis=1))
        # Normalize distances to between -1 (far) and 1 (close)
        max_dist = np.max(dists)
        min_dist = np.min(dists)
        normalized_dists = 1 - 2 * (dists - min_dist) / (max_dist - min_dist)
        # Have sizes range from 1 to 21
        self.sizes = 25*normalized_dists+26
        # Actually change the sizes
        self.scatter.set_sizes(self.sizes)
        # This only gets called when self.show() is, so no need to draw
        # the update here
    
    # Draws tree-like branches
    def make_branches(self, num_branches=100):
        # Define the boundaries of the tree cone
        max_z = 3.5
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
        branchDirs = np.column_stack((zs, thetas))
        branch_points = []
        for branch in branchDirs:
            z = branch[0]
            theta = branch[1]
            r = np.random.uniform(min_r, max_r) * (1 - z / max_z)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            branch_points.append([x, y, z])
        # Get correct format for plotting lines in next loop
        branches = []
        for i in range(num_branches):
            branches.append([[0, branch_points[i][0]]
                             , [0, branch_points[i][1]]
                             , [branch_points[i][2], branch_points[i][2]-.1]])
        # Plot the branches as green lines
        for branch in branches:
            self.ax.plot(branch[0], branch[1], branch[2]
                         , linewidth=3, color='green')
    
    # Zoom in and out when scrolling
    def on_scroll(self, event):
        if event.button == 'up':
            self.ax.dist *= (1.0 / 1.1)
        elif event.button == 'down':
            self.ax.dist *= 1.1
        self.update_point_sizes()
        self.fig.canvas.draw_idle()
    
    # Class is iterable, iterates among the colors of the LEDs in order
    def __iter__(self):
        self.iter = 0
        return self
    def __next__(self):
        if self.iter < len(self.colors):
            result = np.round(255*self.colors[self.iter][:3])
            result = [int(result[1]), int(result[0]), int(result[2])]
            self.iter += 1
            return result
        else:
            raise StopIteration
    def __getitem__(self, key):
        result = np.round(255*self.colors[key][:3])
        result = [int(result[1]), int(result[0]), int(result[2])]
        return result
    def __setitem__(self, key, color):
        self.colors[key] = [color[1]/255, color[0]/255, color[2]/255]
