from pathlib import Path
from time import sleep
from io import BytesIO

import numpy as np
import board
import neopixel
from picamera import PiCamera

LED_COUNT = 1200
LED_PIN = board.D18 # Pin 12 (Use 14 for ground)
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, auto_write = False)

camera = PiCamera()
camera.rotation = 270
camera.resolution = (601, 1001)

ON = (0, 0, 255) # Blue
OFF = (0, 0, 0)

path = Path('/home/pi/Desktop/TreeLights/TreePhotos/')

def light_up(i, sleep_dur = 0.5):
    pixels.fill(OFF)
    pixels[i] = ON
    pixels.show()
    sleep(sleep_dur)
    max_retries = 5
    for _ in range(max_retries):
        if check_for_error():
            pixels.show()
            sleep(sleep_dur)
        else:
            break

def check_for_error():
    stream = BytesIO()
    camera.capture(stream, format='jpeg')
    stream.seek(0)
    image = Image.open(stream)
    image = np.array(image)
    r = image[:, :, 0]
    g = image[:, :, 1]
    b = image[:, :, 2]
    threshold_high = 50
    threshold_low = 10
    red_pixels = (r > threshold_high) & (g < threshold_low) & (b < threshold_low)
    green_pixels = (g > threshold_high) & (r < threshold_low) & (b < threshold_low)
    if red_pixels.any() or green_pixels.any():
        return True
    return False

def save_photo(i, j):
    save_path = path / str(j) / ('00' + str(i))[-3:] + '.jpeg'
    camera.capture(save_path, format='jpeg')

def calibrate(dark = False):
    if dark:
        pixels.fill(OFF)
    else:
        pixels.fill(ON)
    pixels.show()
    camera.start_preview(alpha = 230)
    input('Press enter to end calibration...')
    pixels.fill(OFF)
    pixels.show()
    camera.stop_preview()

# Takes a picture of each LED in sequence.
# Does that 8 times in a row, for 8 different angles.
# Rotate tree 45° clockwise between each round of photos.
# In manual mode, pressing Enter takes a picture, while entering
# an apostrophe re-sends the light commands, to control for errors.
# Enter q in manual mode to change to automatic mode.  
def take_pictures(save_photos = False, manual = False, preview = True):
    if save_photos == False:
        print('Not saving photos')
    else:
        print('Saving photos')
    if manual:
        print('Manual controls enabled')
    try:
        if preview:
            camera.start_preview(alpha = 230)
        for j in range(1, 9):
            if savePhotos:
                path_j = path / str(j)
                path_j.mkdir(parents = True)
            for i in range(LED_COUNT):
                if manual:
                    x = "'"
                    while x == "'":
                        light_up(i, sleep_dur = 0)
                        if x == 'q':
                            manual = False
                            break
                else:
                    light_up(i)
                if save_photos:
                    save_photo(i, j)
                sleep(0.1)
            print()
            if j < 8:
                x = input('Rotate the tree 45° clockwise and press enter...')
            else:
                print('Done.')
    finally:
        if preview:
            camera.stop_preview()

# Retakes only specified pictures, for fixing errors in mass.
# Enter errors into "errors" variable as [j, i] lists from the above function.
# Press enter to take picture, or enter an apostrophe if an error is still present to re-send light commands
def fix_errors():
    try:
        camera.start_preview(alpha = 230)
        errors = []
        for error in errors:
            j = error[0]
            i = error[1]
            x = "'"
            while x == "'":
                light_up(i, sleep_dur = 0)
                x = input("Press Enter to take picture, or ' to retry the the light")
            save_photo(i, j)
            sleep(0.1)
    finally:
        camera.stop_preview()
