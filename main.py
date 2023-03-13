import sys
import os
import logging
import time
import json
import subprocess

# Yes, you should pipenv install RGBMatrixEmulator TODO: add to documentation

sys.path.append(os.path.dirname(__file__) + "/RGBMatrixEmulator")
sys.path.append(os.path.dirname(__file__) + "/rpi-rgb-led-matrix/bindings/python")

import graphics
#from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions# , graphics
from rgbmatrix import RGBMatrix, RGBMatrixOptions # , graphics

# from samplebase import SampleBase
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.parallel = 3
options.chain_length = 3
options.brightness = 50
options.gpio_slowdown = 4
#options.led_limit_refresh = 20
options.hardware_mapping = "regular"
options.pixel_mapper_config = "" # "Rotate:90"
options.disable_hardware_pulsing = False
options.drop_privileges = True

font9 = graphics.Font()
font10 = graphics.Font()
font20 = graphics.Font()

font9.LoadFont("Misc/fonts/9x15.bdf")
font10.LoadFont("Misc/fonts/10x20.bdf")
font20.LoadFont("Misc/fonts/20x40x2.bdf")


# Daytime Color Spectrum
daytime_color_spectrum = {0: graphics.Color(21, 40, 108),
                          130: graphics.Color(21, 41, 114),
                          300: graphics.Color(21, 41, 114),
                          430: graphics.Color(118, 80, 101),
                          600: graphics.Color(253, 193, 17),
                          730: graphics.Color(255, 241, 68),
                          900: graphics.Color(255, 255, 255),
                          1030: graphics.Color(166, 220, 230),
                          1200: graphics.Color(69, 196, 215),
                          1330: graphics.Color(225, 243, 245),
                          1500: graphics.Color(255, 255, 255),
                          1630: graphics.Color(255, 249, 203),
                          1800: graphics.Color(251, 240, 0),
                          1930: graphics.Color(253, 184, 21),
                          2100: graphics.Color(247, 148, 29),
                          2230: graphics.Color(74, 61, 107)}


def color_the_time():
    # initializing nearest key
    search_key = int(time.strftime("%H%M"))


    # Using list comprehension + keys() + lambda
    # Closest key in dictionary
    res = daytime_color_spectrum.get(search_key) or daytime_color_spectrum[min(daytime_color_spectrum.keys(), key=lambda key: abs(key - search_key))]
    # the min() function takes an argument "key" which defines "how to define the minimum" of the given list.
    # In this case, looping through every value of the list as variable "key" and subtracting the search_key, taking
    # the value closest to 0
    # This line is wizardry, to understand it better, read these:
    # https://www.geeksforgeeks.org/python-find-closest-number-to-k-in-given-list/?ref=lbp
    # https://www.geeksforgeeks.org/python-find-the-closest-key-in-dictionary/

    return res



# Old Notes I'm saving in case I run into old problems
# os.environ['http_proxy']='' #Per http://code.activestate.com/lists/python-list/617037/ fixes an Errno -2 error I was getting during updateWU ##10/18/16 Commented this line out due to addition of the internetchecker. Can uncomment if problems suddenly reappear.

def isNight():
    return int(time.strftime("%H")) < 6

def canvasFlip():
    global canvi, mx
    canvi.reverse()
    canvi[1].Clear()

def regCycle():
    logging.info('Main - Reg Cycle')
    #offset_canvas = mx.SwapOnVSync(offset_canvas)
    mx.SwapOnVSync(canvi[0])
    graphics.DrawText(canvi[1], font20, 15, 29, color_the_time(), time.strftime("%H:%M:%S"))
    canvasFlip()


"""
#while True:
    off_canvas.Clear()
    len = graphics.DrawText(off_canvas, font, pos, 10, textColor, "Hello World")
    pos -= 2
    if (pos + len < 0):
        pos = 60
    time.sleep(0.1)
    off_canvas = mx.SwapOnVSync(off_canvas)
"""



def go(currentlyLogging=False):
    mx = RGBMatrix(options=options)
    offset_canvas = mx.CreateFrameCanvas()
    pos = 10

    """ This block moves horizontally
    while True:
        offset_canvas.Clear()
        len = graphics.DrawText(offset_canvas, font, pos, 30, textColor, time.strftime("%H:%M:%S"))
        pos -= 2
        if (pos + len < 0):
            pos = 60
        offset_canvas = mx.SwapOnVSync(offset_canvas)
        time.sleep(0.1)
    """

    while True:
        the_hour = int(time.strftime("%H"))
        if 6 < the_hour and the_hour < 22:
            mx.brightness = 75
        else:
            mx.brightness = 25
        offset_canvas.Clear()
        color_now = color_the_time()
        # fyi, font20 has 2 empty pixels padding in every direction
        len = graphics.DrawText(offset_canvas, font20, 0, 58, color_now, time.strftime("%H%M"))
        graphics.DrawText(offset_canvas, font10, len-20, 77, color_now, time.strftime("%a"))
        graphics.DrawText(offset_canvas, font9, len-20, 28, color_now, time.strftime("%m/%d"))

        offset_canvas = mx.SwapOnVSync(offset_canvas)



# Main function
if __name__ == "__main__":
    # eventually remember how to log
    go()
    
