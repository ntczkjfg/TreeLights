import numpy as np

# Simply pre-defined GRB colors, plus lists of colors that work well together

__all__ = ['RED', 'ORANGE', 'YELLOW', 'GREEN', 'AQUA', 'CYAN', 'BLUE', 'PURPLE', 'PINK',
           'WHITE', 'BLACK', 'ON', 'OFF', 'DIM',
           'COLORS', 'TREE_COLORS', 'TRADITIONAL_COLORS', 'TREE_COLORS_2', 'RAINBOW']

RED = np.array([255, 0, 0])
ORANGE = np.array([255, 50, 0])
YELLOW = np.array([255, 200, 0])
GREEN = np.array([0, 255, 0])
AQUA = np.array([40, 238, 95])
CYAN = np.array([0, 255, 255])
BLUE = np.array([0, 0, 255])
PURPLE = np.array([128, 0, 255])
PINK = np.array([255, 20, 100])

WHITE = np.array([128, 128, 128])
BLACK = np.array([0, 0, 0])
ON = np.array([255, 255, 255])
OFF = np.array([0, 0, 0])
DIM = np.array([6, 6, 6])

COLORS = np.array([WHITE, RED, ORANGE, YELLOW, GREEN, AQUA, CYAN, BLUE, PURPLE, PINK])
TREE_COLORS = np.array([RED, RED, GREEN, GREEN, YELLOW, BLUE])
TRADITIONAL_COLORS = np.array([RED, ORANGE, PINK, BLUE, GREEN])
TREE_COLORS_2 = np.array([PINK, PINK, RED, GREEN, GREEN, YELLOW, BLUE / 2])
RAINBOW = np.array([RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK])