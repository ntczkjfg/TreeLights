# This is taken from the adafruit neopixel library and modified to run faster
# Increases framerate of the tree from about 20 fps to about 30 fps
# Major changes were removing the sleep statement and only initializing _led_strip once instead of once per frame

"""BCM283x NeoPixel Driver Class"""
import _rpi_ws281x as ws
import numpy as np

# LED configuration.
# pylint: disable=redefined-outer-name,too-many-branches,too-many-statements
# pylint: disable=global-statement,protected-access
LED_CHANNEL = 0
LED_FREQ_HZ = 800000  # Frequency of the LED signal.  We only support 800KHz
LED_DMA_NUM = 10  # DMA channel to use, can be 0-14.
LED_BRIGHTNESS = 255  # We manage the brightness in the neopixel library
LED_INVERT = 0  # We don't support inverted logic
LED_STRIP = None  # We manage the color order within the neopixel library

# a 'static' object that we will use to manage our PWM DMA channel
# we only support one LED strip per raspi
_led_strip = None
channel = None
_buf = None


def neopixel_write(gpio, buf):
    """NeoPixel Writing Function"""
    global _led_strip  # we'll have one strip we init if its not at first
    global channel
    global _buf
    
    if _led_strip is None:
        print("Initializing LEDs... ", end = "")
        # Create a ws2811_t structure from the LED configuration.
        # Note that this structure will be created on the heap so you
        # need to be careful that you delete its memory by calling
        # delete_ws2811_t when it's not needed.
        _led_strip = ws.new_ws2811_t()

        # Initialize all channels to off
        for channum in range(2):
            channel = ws.ws2811_channel_get(_led_strip, channum)
            ws.ws2811_channel_t_count_set(channel, 0)
            ws.ws2811_channel_t_gpionum_set(channel, 0)
            ws.ws2811_channel_t_invert_set(channel, 0)
            ws.ws2811_channel_t_brightness_set(channel, 0)

        channel = ws.ws2811_channel_get(_led_strip, LED_CHANNEL)

        # Initialize the channel in use
        LED_STRIP = ws.WS2811_STRIP_RGB
        count = len(buf) // 3

        ws.ws2811_channel_t_count_set(
            channel, count
        )  # we manage 4 vs 3 bytes in the library
        ws.ws2811_channel_t_gpionum_set(channel, gpio._pin.id)
        ws.ws2811_channel_t_invert_set(channel, LED_INVERT)
        ws.ws2811_channel_t_brightness_set(channel, LED_BRIGHTNESS)
        ws.ws2811_channel_t_strip_type_set(channel, LED_STRIP)

        # Initialize the controller
        ws.ws2811_t_freq_set(_led_strip, LED_FREQ_HZ)
        ws.ws2811_t_dmanum_set(_led_strip, LED_DMA_NUM)

        resp = ws.ws2811_init(_led_strip)
        if resp != ws.WS2811_SUCCESS:
            if resp == -5:
                raise RuntimeError(
                    "NeoPixel support requires running with sudo, please try again!"
                )
            message = ws.ws2811_get_return_t_str(resp)
            print("Failure!")
            print(f"ws2811_init failed with code {resp} ({message})")
            return False
        print("Success!")
        return True
    # assign all colors!
    buf = buf.reshape(-1, 3).astype(np.int32)
    buf[:,0] = buf[:,0] << 16
    buf[:,1] = buf[:,1] << 8
    buf = np.bitwise_or.reduce(buf, axis = 1)
    changes = np.where(buf != _buf)[0].tolist()
    _buf = buf
    # Below optimization works, but messes up FPS counter badly
    # Couldn't find a way around that
    #if len(changes) == 0:
    #    return
    buf = buf.tolist()
    for i in changes:
        ws.ws2811_led_set(channel, i, buf[i])
    resp = ws.ws2811_render(_led_strip)
    if resp != ws.WS2811_SUCCESS:
        message = ws.ws2811_get_return_t_str(resp)
        raise RuntimeError(
            "ws2811_render failed with code {0} ({1})".format(resp, message)
        )