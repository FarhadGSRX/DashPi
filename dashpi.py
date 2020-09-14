import sys
import os
import logging
import time
import json
import subprocess

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
# from samplebase import SampleBase
options = RGBMatrixOptions()
options.rows = 32
options.cols = 32
options.chain_length = 4
options.brightness = 50
options.gpio_slowdown = 4
options.hardware_mapping = "regular"

# Matrix Vars
dayBright = 60
nightBright = 20

mx = RGBMatrix(options=options)
canvas = mx.CreateFrameCanvas()
canvas2 = mx.CreateFrameCanvas()
canvi = [canvas, canvas2]

textColor = graphics.Color(255, 0, 255)
font = graphics.Font()
fontHuge = graphics.Font()
font.LoadFont("/home/dietpi/DashPi/Misc/fonts/10x20.bdf")
fontHuge.LoadFont("/home/dietpi/DashPi/Misc/fonts/20x40.bdf")

# Old Notes I'm saving in case I run into old problems
# os.environ['http_proxy']='' #Per http://code.activestate.com/lists/python-list/617037/ fixes an Errno -2 error I was getting during updateWU ##10/18/16 Commented this line out due to addition of the internetchecker. Can uncomment if problems suddenly reappear.

graphics.DrawText(canvi[0], fontHuge, 15, 29, graphics.Color(255, 0, 255), time.strftime("%H:%M"))
time.sleep(3)

def isNight():
    return int(time.strftime("%H")) < 6

def canvasFlip():
    global canvi, mx
    mx.SwapOnVSync(canvi[0])
    if canvi == [canvas, canvas2]:
        canvi = [canvas2, canvas]
    else:
        canvi = [canvas, canvas2]



def nightCycle():
    logging.info('Main - Starting another Night Cycle')
    for n in range(1):
        canvasFlip()
        canvi[0].Clear()
        # Trying to generally move from left to right.
        # Time
        graphics.DrawText(canvi[0], fontHuge, 15, 29, graphics.Color(255,0,255), time.strftime("%H:%M"))
        # Todo: Add Sun, Cloud, and Rain.
        # WU
        #graphics.DrawText(canvi[0], fontLarge, 100, 29, colorDict['green']['color'], wu_helper.getTemp())
        #graphics.DrawText(canvi[0], fontSmall, 119, 19, colorDict['green']['color'], "o")


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
    while True:
        if isNight():
            if mx.brightness == dayBright:
                mx.brightness = nightBright
                canvasFlip()
                mx.brightness = nightBright
        else:
            if mx.brightness == nightBright:
                mx.brightness = dayBright
                canvasFlip()
                mx.brightness = dayBright
        nightCycle()
        time.sleep(60)


# Main function
if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG, filename="DashPi_logfile.txt", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info('DashPi Main Called In, Starting up')
    go(True)
    logging.info('Exiting for some reason?')