from time import time
from pathlib import Path

import numpy as np

from common_variables import rng, tree
from colors import *

# Builds a Color selector function, something lots of effects use
def color_builder(colors = COLORS):
    if colors is None: # No color provided, return random colors
        pick_color = lambda: rng.integers(0, 256, 3)
    else:
        colors = np.array(colors) # Make numpy array
        if colors.ndim == 1: # It's just one color
            pick_color = lambda: colors
        else: # It's an array of colors
            pick_color = lambda: rng.choice(colors)
    return pick_color

def contrast(color1, color2):
    if np.array_equal(color1, BLACK) or np.array_equal(color2, BLACK):
        if not np.array_equal(color1, color2):
            return True
        return False
    # Normalizing the colors to roughly equal brightness (Since brightness differences don't show up well in the tree)
    c1brightness = np.sum(color1)
    c2brightness = np.sum(color2)
    color1 = np.array(color1, dtype=np.float64)
    color2 = np.array(color2, dtype=np.float64)
    color1 = 100 * color1 / c1brightness
    color2 = 100 * color2 / c2brightness
    hue_difference = np.sum(np.abs(color1-color2))#abs(color1[0] - color2[0]) + abs(color1[1] - color2[1]) + abs(color1[2] - color2[2])
    # 40 determined manually as good compromise
    # Not perfect but keeps most good combos while removing the worst of the worst
    return hue_difference >= 40

def contrast_color(old_color, pick_color):
    new_color = pick_color()
    while not contrast(old_color, new_color): new_color = pick_color()
    return new_color

# Runs about 30 fps
def run_from_csv(name, m = None):
    if m is None:
        m = [i for i in range(tree.led_count)]
    path = '/home/pi/Desktop/TreeLights/CSVs/'
    frames = []
    with open(path + name + '.csv', 'r') as f:
        time0 = time()
        file = f.read().split('\n')
        file.pop(0) # First line is column headers, not used
        file.pop(-1) # File ends on a linebreak so final element is empty
        for frame_raw in file:
            frame = []
            frame_raw = frame_raw.split(',')
            for i in range(1, len(frame_raw), 3): # First element is frame number, not used.
                color = [int(frame_raw[i+1]), # Subsequent elements are R, G, B values for each
                         int(frame_raw[i]), # LED in sequence, which are loaded here in G R B order
                         int(frame_raw[i+2])]
                frame.append(color)
            frames.append(frame)
        print(time() - time0, 'seconds to process', len(file), 'frames at', len(file) / (time() - time0), 'fps.')
    while True:
        time1 = time()
        for frame in frames:
            for i in range(min(tree.led_count, len(frame))):
                try:
                    tree[m[i]] = frame[i]
                except IndexError:
                    print(i)
                    raise Exception
            tree.show()
        print(len(frames), 'frames in', round(time()-time1, 3), 'seconds')
        break

# Translates a point or array of points by x, y, and z, then rotates clockwise by zr,
# yr, and xr radians around each axis, in that order
def transform(points, x = 0, y = 0, z = 0, xr = 0, yr = 0, zr = 0):
    if x != 0 or y != 0 or z != 0:
        points = points + [x, y, z]
    # Note: @ operator is matrix multiplication operator
    if zr != 0:
        z_matrix = [[np.cos(zr), -np.sin(zr), 0], [np.sin(zr), np.cos(zr), 0], [0, 0, 1]]
        points = points @ z_matrix
    if yr != 0:
        y_matrix = [[np.cos(yr), 0, np.sin(yr)], [0, 1, 0], [-np.sin(yr), 0, np.cos(yr)]]
        points = points @ y_matrix
    if xr != 0:
        x_matrix = [[1, 0, 0], [0, np.cos(xr), -np.sin(xr)], [0, np.sin(xr), np.cos(xr)]]
        points = points @ x_matrix
    return points

# Related to mapping other trees to my tree
# Needs better documentation, possible rewrite
def find_tree_neighbors(distances = None, m_tree=None):
    if not m_tree:
        return None
    if distances is None:
        distances = []
        for mPixel in m_tree:
            dists = []
            for pixel in tree:
                dists.append(((mPixel.x - pixel.x)**2 + (mPixel.y - pixel.y)**2 + (mPixel.z - pixel.z)**2)**0.5)
            distances.append(dists)
    new_map = [dists.index(min(dists)) for dists in distances]
    i_counts = []
    for i in range(tree.led_count):
        i_counts.append(new_map.count(i))
    redo = False
    for i in range(len(i_counts)):
        if i_counts[i] > 1 and i != new_map[0]:
            redo = True
            reps = [new_map.index(i)]
            for j in range(1, i_counts[i]):
                reps.append(new_map.index(i, reps[-1] + 1))
            dists = [distances[k][i] for k in reps]
            del reps[dists.index(min(dists))]
            for k in reps:
                distances[k][i] = 1000000
    if redo:
        return find_tree_neighbors(distances)
    return new_map

# Runs a CSV show - B list is map from Matt's tree to my tree
B = [371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 371, 372, 226, 387, 373, 206, 374, 293, 379, 294, 292, 295, 376, 375, 377, 227, 378, 224, 367, 370, 228, 296, 230, 368, 29, 31, 600, 398, 199, 391, 289, 200, 201, 399, 395, 390, 299, 1, 225, 297, 203, 202, 392, 298, 500, 393, 396, 389, 96, 388, 397, 394, 98, 16, 300, 11, 400, 0, 322, 321, 318, 101, 5, 97, 20, 316, 12, 15, 315, 317, 313, 592, 591, 590, 304, 303, 305, 589, 306, 307, 588, 326, 309, 308, 311, 586, 314, 312, 725, 265, 310, 585, 724, 264, 587, 584, 271, 327, 262, 726, 261, 266, 583, 263, 582, 267, 332, 721, 681, 684, 409, 575, 330, 48, 46, 38, 37, 105, 192, 45, 39, 41, 407, 719, 57, 92, 106, 47, 49, 277, 276, 268, 578, 259, 581, 676, 728, 260, 7, 729, 343, 270, 363, 253, 579, 730, 248, 245, 731, 247, 246, 338, 269, 249, 341, 732, 739, 340, 673, 668, 242, 734, 339, 738, 733, 672, 748, 736, 667, 665, 241, 663, 735, 664, 362, 449, 237, 238, 365, 235, 222, 232, 233, 9, 223, 448, 240, 239, 662, 221, 220, 234, 661, 236, 445, 361, 231, 366, 208, 213, 51, 356, 655, 211, 656, 283, 357, 358, 360, 209, 670, 658, 218, 212, 659, 749, 219, 660, 747, 737, 216, 359, 210, 444, 443, 554, 442, 284, 441, 457, 510, 437, 438, 355, 154, 433, 626, 552, 653, 625, 353, 354, 352, 351, 281, 558, 624, 555, 347, 217, 346, 657, 745, 666, 254, 742, 744, 348, 572, 279, 335, 334, 256, 278, 740, 746, 743, 243, 741, 675, 257, 336, 674, 244, 252, 337, 250, 577, 258, 251, 727, 677, 580, 273, 576, 722, 678, 723, 679, 275, 680, 274, 195, 613, 102, 325, 329, 405, 194, 324, 404, 702, 402, 614, 704, 701, 615, 603, 607, 403, 612, 499, 44, 93, 418, 189, 181, 497, 288, 498, 502, 501, 386, 290, 204, 503, 205, 385, 504, 291, 384, 381, 382, 509, 454, 453, 507, 506, 455, 505, 440, 380, 207, 383, 508, 287, 439, 496, 187, 285, 456, 286, 186, 458, 495, 182, 512, 185, 184, 494, 163, 515, 628, 110, 71, 491, 111, 517, 492, 644, 645, 518, 643, 516, 493, 183, 629, 513, 630, 162, 511, 627, 460, 514, 164, 463, 145, 489, 521, 526, 144, 542, 479, 134, 128, 132, 135, 142, 136, 139, 138, 137, 478, 480, 131, 528, 529, 487, 648, 647, 486, 176, 636, 420, 415, 413, 618, 706, 417, 567, 410, 408, 695, 568, 156, 687, 157, 67, 79, 562, 564, 649, 428, 143, 126, 547, 477, 476, 545, 544, 543, 520, 539, 548, 549, 468, 429, 430, 118, 148, 650, 171, 170, 561, 560, 557, 553, 169, 652, 651, 80, 432, 147, 68, 551, 550, 435, 434, 167, 436, 654, 459, 166, 153, 461, 165, 462, 70, 69, 120, 525, 464]
def csv_show():
    tree.clear()
    for csv in Path('/home/pi/Desktop/TreeLights/CSVs/').iterdir():
        tree.clear()
        input('Press enter to play ' + csv)
        try:
            run_from_csv(csv[:-4], B)
        except KeyboardInterrupt:
            pass
    tree.clear()
    print('Done')
