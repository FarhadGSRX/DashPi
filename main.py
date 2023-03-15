import csv
import sys
import os
#import logging
import time
#import json
#import subprocess
import csv

# Yes, you should pipenv install RGBMatrixEmulator TODO: add to documentation

sys.path.append(os.path.dirname(__file__) + "/RGBMatrixEmulator")
sys.path.append(os.path.dirname(__file__) + "/rpi-rgb-led-matrix/bindings/python")

# Demoing on PC
import graphics
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions #, graphics

# Running on Pi
#import graphics
#from rgbmatrix import RGBMatrix, RGBMatrixOptions #, graphics

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
font8 = graphics.Font()

font9.LoadFont("Misc/fonts/9x15.bdf")
font10.LoadFont("Misc/fonts/10x20.bdf")
font20.LoadFont("Misc/fonts/20x40x2.bdf")
font8.LoadFont("Misc/fonts/8x13.bdf")



# For posterity
#{0: graphics.Color(21, 40, 108),
#130: graphics.Color(21, 41, 114),
#300: graphics.Color(21, 41, 114),
#430: graphics.Color(118, 80, 101),
#600: graphics.Color(253, 193, 17),
#730: graphics.Color(255, 241, 68),
#900: graphics.Color(255, 255, 255),
#1030: graphics.Color(166, 220, 230),
#1200: graphics.Color(69, 196, 215),
#1330: graphics.Color(225, 243, 245),
#1500: graphics.Color(255, 255, 255),
#1630: graphics.Color(255, 249, 203),
#1800: graphics.Color(251, 240, 0),
#1930: graphics.Color(253, 184, 21),
#2100: graphics.Color(247, 148, 29),
#2230: graphics.Color(74, 61, 107)}

# Daytime Color Spectrum
with open("Misc/colors.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    # rows[0] is the time, and it will be indexed by a string of the form "1330"
    # rows[1:3] are integers and should be coerced as such
    daily_colors = {rows[0]: (int(rows[1]), int(rows[2]), int(rows[3])) for rows in reader}

with open("Misc/color_adjust_by_degree.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    # values are integer degrees and floats with 2 decimal precision
    color_adjust = {int(rows[0]): float(rows[1]) for rows in reader}


def color_the_time(time, adj_index, adj_mult=30):
    rgb_0 = daily_colors[time]
    adj_r = ((adj_index*10)+90)%360
    adj_g = ((adj_index*5)+90)%360
    adj_b = ((adj_index*20)+90)%360
    rgb_1 = (min(max(0,rgb_0[0] + adj_mult*color_adjust[adj_r]),255), 
           min(max(0,rgb_0[1] + adj_mult*color_adjust[adj_g]),255), 
           min(max(0,rgb_0[2] + adj_mult*color_adjust[adj_b]),255))
    
    adj_r2 = (adj_index*10)%360
    adj_g2 = (adj_index*5)%360
    adj_b2 = (adj_index*20)%360
    rgb_2 = (min(max(0,rgb_0[0] + adj_mult*color_adjust[adj_r2]),255), 
             min(max(0,rgb_0[1] + adj_mult*color_adjust[adj_g2]),255), 
             min(max(0,rgb_0[2] + adj_mult*color_adjust[adj_b2]),255))
    return (rgb_1, rgb_2)

def canvasFlip():
    global canvi, mx
    canvi.reverse()
    canvi[1].Clear()

def regCycle():
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

def set_brightness(matrix):
    int(time.strftime("%H"))
    the_hour = int(time.strftime("%H"))
    if 6 < the_hour and the_hour < 22:
        matrix.brightness = 75
    else:
        matrix.brightness = 25

def go(currentlyLogging=False):
    mx = RGBMatrix(options=options)
    offset_canvas = mx.CreateFrameCanvas()
    adjustment_degree = 0

    while True:
        if int(time.strftime("%M")) % 30 == 0:
            set_brightness(mx)

        offset_canvas.Clear()
        
        adjustment_degree += 2
        if adjustment_degree > 359:
            adjustment_degree = 0
        
        rgb_color_now = color_the_time(time.strftime("%H%M"), adjustment_degree)

        # fyi, font20 has 2 empty pixels padding in every direction
        len = graphics.DrawText(offset_canvas, font20, 0, 56, rgb_color_now, time.strftime("%H%M%S"))
        graphics.DrawText(offset_canvas, font10, 3, 77, rgb_color_now, time.strftime("%a"))
        graphics.DrawText(offset_canvas, font9, 3, 91, rgb_color_now, time.strftime("%m/%d"))
        
        # Displaying color information on screen  
        #graphics.DrawText(offset_canvas, font8, 50, 77, rgb_color_now, f"{rgb_color_now[0][0]}/{rgb_color_now[0][1]}/{rgb_color_now[0][2]}")
        #graphics.DrawText(offset_canvas, font8, 50, 91, rgb_color_now, f"{rgb_color_now[1][0]}/{rgb_color_now[1][1]}/{rgb_color_now[1][2]}")

        offset_canvas = mx.SwapOnVSync(offset_canvas)
        time.sleep(0.05)

        



# Main function
if __name__ == "__main__":
    # eventually remember how to log
    go()
    
