from pathlib import Path
from time import time, sleep
import numpy as np
import json
from PIL import Image

cwd = Path.cwd()
parent_path = cwd.parent.parent
TreePhotos_path = parent_path / 'TreePhotos'
Trees_path = parent_path / 'Trees'

# If True, analyze_images() will place a green square on each image where it found an LED.
# Will place a yellow square where it thinks an LED may be, but wasn't certain enough to commit.
MARK_IMAGES = False

image_coordinates = None
LED_COUNT = 0

# image_coordinates is pre-computed.Running analyze_images() will disregard
# the pre-computed version and make a new one.Holds the calculated 3D coordinates
# of each LED in each camera angle.
def load_image_coordinates():
    global image_coordinates, LED_COUNT
    with open(Trees_path / 'image_coordinates.json', 'r') as f:
        image_coordinates = json.load(f)
    LED_COUNT = len(image_coordinates[0])

# data will hold all our data related to the LED locating process.  
# data[i] will hold data for the i-th LED.
# data[i][0] will hold lists.
#    The first element of each list will hold a point calculated from one of the images.  
#    The second element of each list will hold a vector, pointing from the camera to that point.
#    These combined define a line that passes through the LED in 3D space.  
# data[i][1] will hold all the points on each line closest to each other line (See below).
data = []

# coordinates will hold the final calculation, intended for input into the LED control program
coordinates = []

def analyze_images():
    global image_coordinates, LED_COUNT
    start_time = time()
    # Will hold a list of coordinates for all LEDs from all positions
    # First index is the camera angle.  Second index is the LED.  Third index is the x,y,z coordinate.  
    image_coordinates = []
    # Get list of folders in path.  Should be 8 folders named 1-8.  
    print('Done with...', end = ' ') # Primitive progress bar
    import cv2
    for directory in TreePhotos_path.iterdir():
        # Will hold coordinates of all LEDs in this directory
        coordinates_temp = []
        for image in directory.iterdir():
            with Image.open(image) as im:
                img_size = im.size
                img_np = np.array(im)
            # For each pixel in the image, the below code sums up the 0-255 red channel values in the box
            # of size (2*size+1)x(2*size+1) centered on each pixel, then reports which has the highest value
            # So, it finds the pixel in the image with the most red in its immediate area
            size = 2
            kernel = np.ones((2*size + 1, 2*size + 1), np.float32)
            red_channel = img_np[:, :, 0].astype(np.float32)
            redness_sum = cv2.filter2D(red_channel, -1, kernel, borderType=cv2.BORDER_CONSTANT)
            brightest_value = np.max(redness_sum)
            y, x = np.unravel_index(np.argmax(redness_sum), redness_sum.shape)
            brightest = [int(brightest_value), int(x), int(y)]
            # Only accept the found point if it meets some brightness threshold.
            # Manually tuned.  
            if brightest[0] > 80 * (2*size + 1)**2:
                if MARK_IMAGES:
                    with Image.open(image) as im:
                        for x in range(brightest[1] - size, brightest[1] + size + 1):
                            for y in range(brightest[2] - size, brightest[2] + size + 1):
                                im.putpixel((x, y), (0, 255, 0))
                        im.save(image)
                # Half of the width of the image, used to adjust the coordinates below
                horizontalOffset = round(img_size[0] / 2)
                # Using im.size[1]-brightest[2] for z-coordinates adjusts so the z-coordinate is 0 at the bottom of
                # the image instead of the top, as is default
                # These all calculate a point in 3D space such that a line between the camera and the point will intersect the LED.
                # Imagine the picture as a plane perpendicular to the sight of the camera, with its bottom center pixel at the origin.
                # The LED is then given those 3D coordinates based on its position in that picture.  
                if directory.name == '1': # From positive x-axis
                    coordinates_temp.append([0, brightest[1] - horizontalOffset, img_size[1] - brightest[2]])
                elif directory.name == '2': # From quadrant 1
                    coordinates_temp.append([round(-(brightest[1] - horizontalOffset)/2**0.5, 5), round((brightest[1] - horizontalOffset)/2**0.5, 5), img_size[1] - brightest[2]])
                elif directory.name == '3': # From positive y-axis
                    coordinates_temp.append([-(brightest[1] - horizontalOffset), 0, img_size[1] - brightest[2]])
                elif directory.name == '4': # From quadrant 2
                    coordinates_temp.append([round(-(brightest[1] - horizontalOffset)/2**0.5, 5), round(-(brightest[1] - horizontalOffset)/2**0.5, 5), img_size[1] - brightest[2]])
                elif directory.name == '5': # From negative x-axis
                    coordinates_temp.append([0, -(brightest[1] - horizontalOffset), img_size[1] - brightest[2]])
                elif directory.name == '6': # From quadrant 3
                    coordinates_temp.append([round((brightest[1] - horizontalOffset)/2**0.5, 5), round(-(brightest[1] - horizontalOffset)/2**0.5, 5), img_size[1] - brightest[2]])
                elif directory.name == '7': # From negative y-axis
                    coordinates_temp.append([brightest[1] - horizontalOffset, 0, img_size[1] - brightest[2]])
                elif directory.name == '8': # From quadrant 4
                    coordinates_temp.append([round((brightest[1] - horizontalOffset)/2**0.5, 5), round((brightest[1] - horizontalOffset)/2**0.5, 5), img_size[1] - brightest[2]])
                else:
                    raise Exception(f'Unknown directory: {directory}')
            # Didn't find anything particularly red, assume LED was occluded and data is bad
            else:
                if MARK_IMAGES:
                    with Image.open(image) as im:
                        for x in range(brightest[1] - size, brightest[1] + size + 1):
                            for y in range(brightest[2] - size, brightest[2] + size + 1):
                                im.putpixel((x, y), (255, 255, 0))
                        im.save(image)
                # Can't just skip the coordinates or the index of everything after will be off by 1
                coordinates_temp.append(None)
            # So the user isn't left wondering how much longer is left...
            if int(image.name[0:4]) % 100 == 0:
                time_passed = int(time() - start_time)
                print(str(time_passed) + 's', image.relative_to(parent_path), end = ', ')
        # Just to get the newline character
        print()
        image_coordinates.append(coordinates_temp)
    Trees_path.parent.mkdir(parents=True, exist_ok=True)
    with open(Trees_path / 'image_coordinates.json', 'w') as f:
        json.dump(image_coordinates, f, indent = 4)
    LED_COUNT = len(image_coordinates[0])

# Takes data in 'image_coordinates' from analyze_images() (or pre-computed) and populates 'data' with appropriate points
# in appropriate orders with appropriate vectors from camera to point
# cameraDist and cameraHeight should be given in units of pixels.  
def calc_coords_and_vectors(cameraDist, cameraHeight):
    global data
    data = [[[], [], []] for i in range(LED_COUNT)]
    # Camera moves counterclockwise in 45-degree increments
    camera = np.array([[cameraDist, 0, cameraHeight] # Positive x-axis
              , [.7071*cameraDist, .7071*cameraDist, cameraHeight] # Quadrant 1
              , [0, cameraDist, cameraHeight] # Positive y-axis
              , [-.7071*cameraDist, .7071*cameraDist, cameraHeight] # Quadrant 2
              , [-cameraDist, 0, cameraHeight] # Negative x-axis
              , [-.7071*cameraDist, -.7071*cameraDist, cameraHeight] # Quadrant 3
              , [0, -cameraDist, cameraHeight] # Negative y-axis
              , [.7071*cameraDist, -.7071*cameraDist, cameraHeight]]) # Quadrant 4
    for i in range(LED_COUNT):
        for j in range(len(image_coordinates)):
            if image_coordinates[j][i] == None:
                continue
            # Appends a point and a vector from the camera to the point
            data[i][0].append([image_coordinates[j][i]
                               , list(np.array(image_coordinates[j][i]) - camera[j])])

# Each LED had up to eight lines defined by the eight images that were
# taken of it, given by the vector equation v(t) = p + t*d, where p is the
# point calculated from an image, and d is the calculated vector from the
# camera to that point.  This function calculates the point on each of these
# lines closest to each of the other lines, for up to 56 points total.
# These points are stored in a list and put in data[i][1].  
def calc_nearest_points():
    for LED in data:
        # Holds the points for the i-th LED
        iPoints = []
        for j in range(len(LED[0])): # First line
            for k in range(j+1, len(LED[0])): # Second line
                # Following uses the formula on this page:
                # https://en.wikipedia.org/wiki/Skew_lines#Distance
                p1 = np.array(LED[0][j][0])
                p2 = np.array(LED[0][k][0])
                d1 = np.array(LED[0][j][1])
                d2 = np.array(LED[0][k][1])
                n = np.cross(d1, d2)
                n1 = np.cross(d1, n)
                n2 = np.cross(d2, n)
                # If the below dot product == 0 the lines are parallel so we can calculate no valid point
                # Does actually happen in practice sometimes
                if np.dot(d1, n2) != 0:
                    c1 = p1 + d1 * np.dot(p2 - p1, n2)/np.dot(d1, n2)
                    c2 = p2 + d2 * np.dot(p1 - p2, n1)/np.dot(d2, n1)
                    iPoints.append(list(c1))
                    iPoints.append(list(c2))
        LED[1] = iPoints

# Now we average the points calculated for each LED in the above code
# and take this as our final coordinates.
def calc_average_points():
    # Hold the index of any LED which had either 0 or 1 usable images, from which a 3D position cannot
    # be calculated.  These will instead be calculated by interpolating the position of its neighbors.  
    error_LEDs = []
    for i, LED in enumerate(data):
        # Happens if the LED is only clearly visible in 0 or 1 images
        # Add to error_LEDs so we know to interpolate its position later
        if LED[1] == []:
            print('Not enough data for', i)
            error_LEDs.append(i)
            coordinates.append(np.array([0, 0, 0]))
            continue
        point = [0, 0, 0]
        for j in range(3): # x, y, and z coordinates
            total = 0
            for k in range(len(LED[1])):
                total += LED[1][k][j]
            point[j] = total / len(LED[1])
        coordinates.append(np.array(point))
    # Interpolate LEDs which didn't have enough data to calculate a position
    # Gives up if there's more than one error in a row, will be fixed later in find_errors() anyways
    for i in error_LEDs:
        print('Interpolating', i)
        if i-1 not in error_LEDs and i+1 not in error_LEDs:
            coordinates[i] = (coordinates[i-1] + coordinates[i+1])/2

# Calculates the average distance between consecutive LEDs.
# If two consecutive LEDs are more than double this average distance, it's assumed
# there's an error.  
def find_errors(first = True):
    if not first:
        print('Second find_errors')
    totalDistance = 0
    for i in range(LED_COUNT - 1):
        totalDistance += np.linalg.norm(coordinates[i] - coordinates[i+1])
    avgDistance = totalDistance / (LED_COUNT - 1)
    
    goodVals = [0]
    for i in range(1, LED_COUNT - 1):
        distLeft = np.linalg.norm(coordinates[i] - coordinates[i-1])
        distRight = np.linalg.norm(coordinates[i] - coordinates[i+1])
        if (distLeft > 2*avgDistance or distLeft == 0) and (distRight > 2*avgDistance or distRight == 0):
            # Make an exception for every 50th LED because the connection
            # between strands is longer.  
            if (i+1) % 50 == 0 and distLeft != 0 and distRight != 0:
                goodVals.append(i)
                continue
        else:
            goodVals.append(i)
    for i in range(LED_COUNT - 1):
        if i in goodVals:
            continue
        print('Fixing', i)
        # a will be the last good index, b will be the next good index
        # We will then interpolate all bad LEDs between a and b.  
        # If two LEDs appear consecutively, it's fairly likely only the
        # second one is actually in error
        a = i - 1
        for j in range(i+1, LED_COUNT):
            if j in goodVals:
                b = j
                break
        badGaps = b - a
        baDist = coordinates[b] - coordinates[a]
        for j in range(a + 1, b):
            coordinates[j] = coordinates[a] + baDist*(j-a)/badGaps
            goodVals.append(j)
        if first:
            find_errors(False)

# Normalize coordinates to GIFT format:  x- and y-values are limited from -1 to 1, and
# z-values start at 0 and go as high as they need to at the same scale as the x- and y-values
def normalize():
    maxDist = 0
    minZ = 1000
    for coordinate in coordinates:
        dist = max(coordinate[0], -coordinate[0], coordinate[1], -coordinate[1])
        if dist > maxDist: maxDist = dist
        if coordinate[2] < minZ: minZ = coordinate[2]
    # Taking the ceiling so no points ever end up on the wrong side of -1 or 1 by rounding
    maxDist = np.ceil(maxDist)
    for i in range(len(coordinates)):
        coordinates[i] = (coordinates[i] - np.array([0, 0, minZ])) / maxDist

# Calculate everything.  Does not analyze images.  
def calc():
    global coordinates
    load_image_coordinates()
    pixelsPerInch = 11.9 # Manually calculated, as are below two values
    cameraDist = 72 * pixelsPerInch
    cameraHeight = 31.25 * pixelsPerInch
    calc_coords_and_vectors(cameraDist, cameraHeight)
    calc_nearest_points()
    calc_average_points()
    find_errors()
    normalize()
    coordinates = [[round(coord, 5) for coord in coordinate] for coordinate in coordinates]
    Trees_path.parent.mkdir(parents = True, exist_ok = True)
    with open(Trees_path / 'coordinates.list', 'w') as f:
        json.dump(coordinates, f, indent=4)

analyze_images()
calc()
