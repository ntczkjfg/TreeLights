import board
import neopixel
from picamera import PiCamera
import os
from time import time, sleep

LED_COUNT = 750
LED_PIN = board.D18 # Pin 12 (Use 14 for ground)
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, auto_write = False)

camera = PiCamera()
camera.rotation = 270
camera.resolution = (601, 1001)

ON = (0, 0, 255) # Blue
OFF = (0, 0, 0)

PATH = "/home/pi/Desktop/TreeLights/TreePhotos/"

# Takes a picture of each LED in sequence.
# Does that 8 times in a row, for 8 different angles.
# Rotate tree 45° clockwise between each round of photos.
# In manual mode, pressing Enter takes a picture, while entering
# an apostrophe re-sends the light commands, to control for errors.  
def takePictures(takePictures = False, manual = True):
    if takePictures == False:
        print("Not taking pictures")
    if manual:
        print("Manual controls enabled")
    camera.start_preview(alpha = 230)
    for j in range(1, 9):
        if takePictures:
            os.mkdir(PATH + str(j))
        for i in range(LED_COUNT):
            if manual:
                x = "'"
                while x == "'":
                    pixels.fill(OFF)
                    pixels[i] = ON
                    pixels.show()
                    try:
                        x = input(str(j) + "/" + (str("00") + str(i))[-3:] + "...")
                    except KeyboardInterrupt:
                        camera.stop_preview()
                        return
            else:
                pixels.fill(OFF)
                pixels[i] = ON
                pixels.show()
                print(str(j) + "/" + (str("00") + str(i))[-3:], end = ", ")
                sleep(.5)
            if takePictures:
                camera.capture(PATH + str(j) + "/" + (str("00") + str(i))[-3:] + ".jpg")
            sleep(0.1)
        print()
        if j < 8:
            x = input("Rotate the tree 45° clockwise and press enter...")
        else:
            print("Done.")
    camera.stop_preview()

# Retakes only specified pictures, for fixing errors in mass.
# Enter errors into "errors" variable as [j, i] lists from the above function.
# Manual mode only.  
def fixErrors():
    camera.start_preview(alpha = 230)
    errors = []
    for error in errors:
        j = error[0]
        i = error[1]
        x = "'"
        while x == "'":
            pixels.fill(OFF)
            pixels[i] = ON
            pixels.show()
            try:
                x = input(str(j) + "/" + (str("00") + str(i))[-3:] + "...")
            except KeyboardInterrupt:
                camera.stop_preview()
                return
        camera.capture(PATH + str(j) + "/" + (str("00") + str(i))[-3:] + ".jpg")
        sleep(0.1)
    camera.stop_preview()
