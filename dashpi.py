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
options.brightness = 20
options.gpio_slowdown = 4
options.hardware_mapping = "regular"

textColor = graphics.Color(255, 0, 255)
font = graphics.Font()
fontHuge = graphics.Font()
font.LoadFont("/home/dietpi/DashPi/Misc/fonts/10x20.bdf")
fontHuge.LoadFont("/home/dietpi/DashPi/Misc/fonts/20x40.bdf")

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
    graphics.DrawText(canvi[1], font, 15, 29, graphics.Color(255, 0, 255), time.strftime("%H:%M:%S"))
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

    while True:
        offset_canvas.Clear()
        len = graphics.DrawText(offset_canvas, font, pos, 10, textColor, time.strftime("%H:%M:%S"))
        pos -= 2
        if (pos + len < 0):
            pos = 60
        offset_canvas = mx.SwapOnVSync(offset_canvas)
        time.sleep(0.1)



# Main function
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename="DashPi_logfile.txt", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info('DashPi Main Called In, Starting up')
    go()
    logging.info('Exiting for some reason?')