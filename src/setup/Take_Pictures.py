from pathlib import Path
from time import sleep
from io import BytesIO

import numpy as np
from PIL import Image
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

# Just opens up the camera preview and turns on the tree, so you can make sure it's in frame correctly
def calibrate(dark = False):
    if dark:
        pixels.fill(OFF)
    else:
        pixels.fill(ON)
    pixels.show()
    camera.start_preview(alpha = 200)
    input('Press enter to end calibration...')
    pixels.fill(OFF)
    pixels.show()
    camera.stop_preview()

# Turns on LED with index i
def light_up(i, sleep_dur = 0.3):
    # Set all pixels to OFF, then turn on the selected pixel and show
    pixels.fill(OFF)
    pixels[i] = ON
    pixels.show()
    sleep(sleep_dur)
    # Check for errors - sometimes other LEDs activate, or the wrong color activates
    # Retries up to 5 times until no errors are detected
    max_retries = 5
    for _ in range(max_retries):
        if check_for_error():
            print('*', end = '')
            pixels.show()
            sleep(sleep_dur)
        else:
            break

# Checks for errors - namely, pixels which are lit up in either red or green instead of blue, which is a common error type due to poor connectivity
# Returns True if any such pixels are found, False otherwise
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
    threshold_low = 15
    red_pixels = (r > threshold_high) & (g < threshold_low) & (b < threshold_low)
    green_pixels = (g > threshold_high) & (r < threshold_low) & (b < threshold_low)
    if red_pixels.any() or green_pixels.any():
        return True
    return False

# Saves the current camera view to file
def save_photo(name):
    save_path = str(path / (name + '.jpeg'))
    camera.capture(save_path, format='jpeg')

# Takes a photo of each LED in sequence.
# Does that 8 times in a row, for 8 different angles.
# Rotate tree 45° clockwise between each round of photos.
# In manual mode, pressing Enter takes a photo, while entering
# an apostrophe re-sends the light commands, to control for errors.
# Enter q in manual mode to change to automatic mode.  
def take_photos(save_photos = False,
                manual = False,
                show_preview = True,
                j_start = 1):
    if save_photos:
        print('Saving photos')
    else:
        print('Not saving photos')
    if manual:
        print('Manual controls enabled')
    try:
        if show_preview:
            camera.start_preview(alpha = 200)
        for j in range(j_start, 9):
            if save_photos:
                # Create the directory for this rotation
                path_j = path / str(j)
                path_j.mkdir(parents = True, exist_ok = True)
            print('Taking photos... ', end = '')
            for i in range(LED_COUNT):
                if manual:
                    x = "'"
                    while x == "'":
                        light_up(i, sleep_dur = 0)
                        x = input("Enter to take photo, q to quit, ' to retry: ")
                        if x == 'q':
                            manual = False
                            break
                else:
                    light_up(i)
                if save_photos:
                    name = f'{j}/' + ('000' + str(i))[-4:]
                    save_photo(name)
                    print(name, end = ', ')
            print('done!')
            if j < 8:
                input('Rotate the tree 45° clockwise and press enter...')
            else:
                print('Done.')
    except KeyboardInterrupt:
        print('\nQuitting')
        return
    finally:
        if show_preview:
            camera.stop_preview()

# Retakes only specified photos, for fixing errors in mass.
# Enter errors into "errors" variable as [j, i] lists from the above function.
# Press enter to take photo, or enter an apostrophe if an error is still present to re-send light commands
def fix_errors():
    try:
        camera.start_preview(alpha = 200)
        errors = []
        for error in errors:
            j, i = error
            x = "'"
            while x == "'":
                light_up(i, sleep_dur = 0)
                x = input("Press Enter to take photo, or ' to retry the the light")
            name = f'{j}/' + ('000' + str(i))[-4:]
            save_photo(name)
            print(name, end = ', ')
            sleep(0.1)
    finally:
        camera.stop_preview()
