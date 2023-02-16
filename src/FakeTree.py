import pickle
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['toolbar'] = 'None'
D18 = 0
class FakeTree:
    def __init__(self, pin, LED_COUNT, auto_write = False):
        with open(r"C:\Users\User\My Stuff\GitHub\TreeLights\Trees\coordinates.list", "rb") as f:
            self.coords = np.array(pickle.load(f))
        # Initial colors are all just black
        self.colors = np.zeros_like(self.coords)
        
        # Create figure / axis, add points to axis, set their colors
        width = 3
        height = np.max(self.coords[:, 2])/2 * width
        self.fig = plt.figure(figsize=(width, height), dpi=100)
        self.fig.set_facecolor('red')
        self.ax = self.fig.add_subplot(111, projection='3d', aspect='auto')
        self.ax.set_position([0, 0, width, height])
        self.ax.set_facecolor('lightgray')
        self.ax.set_position([0.5, 0.5, 0.9, 0.9])
        self.scatter = self.ax.scatter(self.coords[:,0], self.coords[:,1], self.coords[:,2], c=self.colors)

        # Camera is parallel to the xy plane
        self.ax.elev = 0
        # Camera is pointing backward along the positive x-axis
        self.ax.azim = 0
        self.ax.dist = 6
        # Adjust axis bounds
        self.ax.set_xlim3d(-1, 1)
        self.ax.set_ylim3d(-1, 1)
        self.ax.set_zlim3d(0, np.max(self.coords[:,2]))
        # Set aspect ratio
        self.ax.set_box_aspect((1, 1, 1.75))
        # Hide axes and gridlines
        self.ax.set_axis_off()
        self.ax.grid(False)

        # Adjust plot layout
        self.fig.tight_layout()
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        # Show the plot - need `block=False` to not lock the thread
        plt.show(block=False)

    def show(self):
        self.scatter.set_facecolors(self.colors)
        plt.pause(0.01)
    
    def update_colors(self, colors):
        colors = [[color[1], color[0], color[2]] for color in colors]
        self.colors = colors

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
