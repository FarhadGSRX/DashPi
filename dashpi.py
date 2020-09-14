import sys
import os
import logging
import time
import json
import subprocess

import Image
import ImageDraw


logging.basicConfig(level=logging.DEBUG, filename="DashPi_logfile.txt", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
logging.info('DashPi Main Called In')


# Old Notes I'm saving in case I run into old problems
# os.environ['http_proxy']='' #Per http://code.activestate.com/lists/python-list/617037/ fixes an Errno -2 error I was getting during updateWU ##10/18/16 Commented this line out due to addition of the internetchecker. Can uncomment if problems suddenly reappear.


from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
# from samplebase import SampleBase

options = RGBMatrixOptions()
options.rows=32
options.cols=32
options.chain_length=4
options.brightness=50
options.gpio_slowdown=4
options.hardware_mapping = "regular"

mx = RGBMatrix(options = options)
canvas = mx.CreateFrameCanvas()
off_canvas = mx.CreateFrameCanvas()

textColor = graphics.Color(255,0,255)
font = graphics.Font()
font.LoadFont("/home/dietpi/rpi-rgb-leg-matrix/fonts/7x13.bdf")

pos = 30

while True:
    off_canvas.Clear()
    len = graphics.DrawText(off_canvas, font, pos, 10, textColor, "Hello World")
    pos -= 2
    if (pos + len < 0):
        pos = 60
    time.sleep(0.1)
    off_canvas = mx.SwapOnVSync(off_canvas)

mx.clear()
