import os
from time import time, sleep
import numpy as np
import pickle
from PIL import Image



PATH = "C:/Users/User/Desktop/TreePhotos/"

# If True, analyzeImages() will place a green square on each image where it found an LED.
# Will place a yellow square where it thinks an LED may be, but wasn't certain enough to commit.
MARK_IMAGES = True

# imageCoordinates is pre-computed.  Running analyzeImages() will disregard
# the pre-computed version and make a new one.  Takes several hours to run.  Holds the calculated 3D coordinates
# of each LED in each camera angle.
with open("/home/pi/Desktop/TreeLights/TreePhotos/imageCoordinates.pickle", "rb") as f:
    imageCoordinates = pickle.load(f)

LED_COUNT = len(imageCoordinates[0])

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

def analyzeImages():
    global imageCoordinates
    startTime = time()
    # Will hold a list of coordinates for all LEDs from all positions
    # First index is the camera angle.  Second index is the LED.  Third index is the x,y,z coordinate.  
    imageCoordinates = []
    # Get list of folders in PATH.  Should be 8 folders named 1-8.  
    dirList = os.listdir(PATH)
    print("Done with...", end = " ") # Primitive progress bar
    for directory in dirList:
        # Get list of images in directory.  Should be LED_COUNT of them from 000.jpg to [LED_COUNT-1].jpg.
        imgList = os.listdir(PATH + directory)
        # Will hold coordinates of all LEDs in this directory
        coordinatesTemp = []
        for image in imgList:
            with Image.open(PATH + directory + "/" + image) as im:
                img = im.load()
                # Tracks brightest pixel found so far:  [brightness, x, y]
                brightest = [0, 0, 0]
                # Checks all pixels in a 2*size+1 square centered on x, y.  Should size it to roughly approximate
                # the typical smallest LED size at whatever image resolution you used.  
                # ranges below avoid the edges of the image where the size of the box would leave the image bounds
                size = 2
                for x in range(size, im.size[0] - size):
                    # range below was calculated manually to exclude regions of the image where the LEDs will never appear.
                    # Replace with just range(size, im.size[1] - size) if you're using a different image set and don't want to exclude
                    # your own regions similarly.  This is just done for speed improvements.  
                    for y in range(int(max(-2.7748*x + 727, size, 2.79762*x - 973.57)), im.size[1] - size):
                        # The LEDs light up pure blue, but we check for red because the LED itself is bright enough to
                        # show up as white to the camera, helping prevent false positives by objects lit up bright blue
                        # by the LED itself
                        redness = 0
                        for i in range(x-size, x+size+1):
                            for j in range(y-size, y+size+1):
                                redness += img[i, j][0]
                        redness = redness / (2*size + 1)**2
                        if redness > brightest[0]:
                            brightest = [redness, x, y]
                # Only accept the found point if it meets some brightness threshold.
                # Manually tuned.  
                if brightest[0] > 80:
                    if MARK_IMAGES:
                        for x in range(brightest[1] - size, brightest[1] + size + 1):
                            for y in range(brightest[2] - size, brightest[2] + size + 1):
                                im.putpixel((x, y), (0, 255, 0))
                        im.save(PATH + directory + "/" + image)
                    # Half of the width of the image, used to adjust the coordinates below
                    horizontalOffset = round(im.size[0]/2)
                    # Using im.size[1]-brightest[2] for z-coordinates adjusts so the z-coordinate is 0 at the bottom of
                    # the image instead of the top, as is default
                    # These all calculate a point in 3D space such that a line between the camera and the point will intersect the LED.
                    # Imagine the picture as a plane perpendicular to the sight of the camera, with its bottom center pixel at the origin.
                    # The LED is then given those 3D coordinates based on its position in that picture.  
                    if directory == "1": # From positive x-axis
                        coordinatesTemp.append([0, brightest[1] - horizontalOffset, im.size[1] - brightest[2]])
                    elif directory == "2": # From quadrant 1
                        coordinatesTemp.append([round(-(brightest[1] - horizontalOffset)/2**0.5, 5), round((brightest[1] - horizontalOffset)/2**0.5, 5), im.size[1] - brightest[2]])
                    elif directory == "3": # From positive y-axis
                        coordinatesTemp.append([-(brightest[1] - horizontalOffset), 0, im.size[1] - brightest[2]])
                    elif directory == "4": # From quadrant 2
                        coordinatesTemp.append([round(-(brightest[1] - horizontalOffset)/2**0.5, 5), round(-(brightest[1] - horizontalOffset)/2**0.5, 5), im.size[1] - brightest[2]])
                    elif directory == "5": # From negative x-axis
                        coordinatesTemp.append([0, -(brightest[1] - horizontalOffset), im.size[1] - brightest[2]])
                    elif directory == "6": # From quadrant 3
                        coordinatesTemp.append([round((brightest[1] - horizontalOffset)/2**0.5, 5), round(-(brightest[1] - horizontalOffset)/2**0.5, 5), im.size[1] - brightest[2]])
                    elif directory == "7": # From negative y-axis
                        coordinatesTemp.append([brightest[1] - horizontalOffset, 0, im.size[1] - brightest[2]])
                    elif directory == "8": # From quadrant 4
                        coordinatesTemp.append([round((brightest[1] - horizontalOffset)/2**0.5, 5), round((brightest[1] - horizontalOffset)/2**0.5, 5), im.size[1] - brightest[2]])
                # Didn't find anything particularly red, assume LED was occluded and data is bad
                else:
                    if MARK_IMAGES:
                        for x in range(brightest[1] - size, brightest[1] + size + 1):
                            for y in range(brightest[2] - size, brightest[2] + size + 1):
                                im.putpixel((x, y), (255, 255, 0))
                        im.save(PATH + directory + "/" + image)
                    # Can't just skip the coordinates or the index of everything after will be off by 1
                    coordinatesTemp.append(None)
            # So the user isn't left wondering how much longer is left...
            if int(image[0:3]) % 100 == 0:
                timePassed = int(time() - startTime)
                print(str(timePassed) + "s", directory + "/" + image, end = ", ")
        # Just to get the newline character
        print()
        imageCoordinates.append(coordinatesTemp)
    print(imageCoordinates)
    LED_COUNT = len(imageCoordinates[0])

# Takes data in 'imageCoordinates' from analyzeImages() (Or pre-computed) and populates 'data' with appropriate points
# in appropriate orders with appropriate vectors from camera to point
# cameraDist and cameraHeight should be given in units of pixels.  
def calcCoordsAndVectors(cameraDist, cameraHeight):
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
        for j in range(len(imageCoordinates)):
            if imageCoordinates[j][i] == None:
                continue
            # Appends a point and a vector from the camera to the point
            data[i][0].append([imageCoordinates[j][i]
                               , list(np.array(imageCoordinates[j][i]) - camera[j])])

# Each LED had up to eight lines defined by the eight images that were
# taken of it, given by the vector equation v(t) = p + t*d, where p is the
# point calculated from an image, and d is the calculated vector from the
# camera to that point.  This function calculates the point on each of these
# lines closest to each of the other lines, for up to 56 points total.
# These points are stored in a list and put in data[i][1].  
def calcNearestPoints():
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
def calcAveragePoints():
    # Hold the index of any LED which had either 0 or 1 usable images, from which a 3D position cannot
    # be calculated.  These will instead be calculated by interpolating the position of its neighbors.  
    errorLEDs = []
    for i, LED in enumerate(data):
        # Happens if the LED is only clearly visible in 0 or 1 images
        # Add to errorLEDs so we know to interpolate its position later
        if LED[1] == []:
            print("Not enough data for", i)
            errorLEDs.append(i)
            coordinates.append(np.array([0, 0, 0]))
            continue
        point = [0, 0, 0]
        for j in range(3): # x, y, and z coordinates
            total = 0
            for k in range(len(LED[1])):
                total += LED[1][k][j]
            point[j] = total/len(LED[1])
        coordinates.append(np.array(point))
    # Interpolate LEDs which didn't have enough data to calculate a position
    # Gives up if there's more than one error in a row, will be fixed later in findErrors() anyways
    for i in errorLEDs:
        print("Interpolating", i)
        if i-1 not in errorLEDs and i+1 not in errorLEDs:
            coordinates[i] = (coordinates[i-1] + coordinates[i+1])/2

# Calculates the average distance between consecutive LEDs.
# If two consecutive LEDs are more than double this average distance, it's assumed
# there's an error.  
def findErrors(first = True):
    if not first:
        print("Second findErrors")
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
        print("Fixing", i)
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
            findErrors(False)

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
    pixelsPerInch = 16.85 # Manually calculated, as are below two values
    cameraDist = 50 * pixelsPerInch
    cameraHeight = 31.25 * pixelsPerInch
    calcCoordsAndVectors(cameraDist, cameraHeight)
    calcNearestPoints()
    calcAveragePoints()
    findErrors()
    normalize()
    coordinates = [[round(coord, 5) for coord in coordinate] for coordinate in coordinates]
    print(coordinates)

#analyzeImages()
#calc()
