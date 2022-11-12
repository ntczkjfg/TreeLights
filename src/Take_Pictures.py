import board
import neopixel
from picamera import PiCamera
import os
from time import time, sleep

LED_COUNT = 800
LED_PIN = board.D18 # Pin 12 (Use 14 for ground)
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, auto_write = False)

camera = PiCamera()
camera.rotation = 270
camera.resolution = (601, 1001)

ON = (0, 0, 255) # Blue
OFF = (0, 0, 0)

PATH = "/home/pi/Desktop/TreeLights/TreePhotos/"

def next(i, j):
    pixels.fill(OFF)
    pixels[i] = ON
    pixels.show()
    pixels.show()
    print(str(j) + "/" + (str("00") + str(i))[-3:], end = ", ")

# Takes a picture of each LED in sequence.
# Does that 8 times in a row, for 8 different angles.
# Rotate tree 45° clockwise between each round of photos.
# In manual mode, pressing Enter takes a picture, while entering
# an apostrophe re-sends the light commands, to control for errors.
# Enter q in manual mode to change to automatic mode.  
def takePictures(savePhotos = False, manual = True):
    if savePhotos == False:
        print("Not saving photos")
    else:
        print("Saving photos")
    if manual:
        print("Manual controls enabled")
    camera.start_preview(alpha = 230)
    for j in range(1, 9):
        if savePhotos:
            os.mkdir(PATH + str(j))
        for i in range(LED_COUNT):
            try:
                if manual:
                    x = "'"
                    while x == "'":
                        next(i, j)
                        if x == "q":
                            manual = False
                            break
                else:
                    next(i, j)
                    sleep(.5)
                if savePhotos:
                    camera.capture(PATH + str(j) + "/" + (str("00") + str(i))[-3:] + ".jpg")
                sleep(0.1)
            except KeyboardInterrupt:
                camera.stop_preview()
                return
        print()
        if j < 8:
            x = input("Rotate the tree 45° clockwise and press enter...")
        else:
            print("Done.")
    camera.stop_preview()

# Retakes only specified pictures, for fixing errors in mass.
# Enter errors into "errors" variable as [j, i] lists from the above function.
# Press enter to take picture, or enter an apostrophe if an error is still present to re-send light commands
def fixErrors():
    camera.start_preview(alpha = 230)
    errors = []
    for error in errors:
        j = error[0]
        i = error[1]
        x = "'"
        try:
            while x == "'":
                next(i, j)
                x = input("...")
            camera.capture(PATH + str(j) + "/" + (str("00") + str(i))[-3:] + ".jpg")
            sleep(0.1)
        except KeyboardInterrupt:
            camera.stop_preview()
            return
    camera.stop_preview()
