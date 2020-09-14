import sys
import os
import logging
import time
import json
import urllib2
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
    off_canvas = Clear()
    len = graphics.DrawText(off_canvas, font, pos, 10, textColor, "Hello World")
    pos -= 2
    if (pos + len < 0):
        pos = 60
    time.sleep(0.1)
    off_canvas = mx.SwapOnVSync(off_canvas)

mx.clear()


# Fonts/Colors/Stylings
fontlist = ["fonts/4x6.bdf", "fonts/5x7.bdf", "fonts/5x8.bdf", "fonts/6x9.bdf", "fonts/6x10.bdf", "fonts/6x12.bdf",
            "fonts/6x13.bdf", "fonts/6x13B.bdf", "fonts/6x13O.bdf", "fonts/7x13.bdf", "fonts/7x13B.bdf",
            "fonts/7x13O.bdf", "fonts/7x14.bdf", "fonts/7x14B.bdf", "fonts/8x13.bdf", "fonts/8x13B.bdf",
            "fonts/8x13O.bdf", "fonts/9x15.bdf", "fonts/9x15B.bdf", "fonts/9x18.bdf", "fonts/9x18B.bdf",
            "fonts/10x20.bdf", "fonts/20x40.bdf", "fonts/clR6x12.bdf", "fonts/helvR12.bdf"]
colorDict = {"black": {"color": graphics.Color(0, 0, 0)}, "white": {"color": graphics.Color(130, 130, 130)},
             "red": {"color": graphics.Color(130, 0, 0)}, "green": {"color": graphics.Color(0, 130, 0)},
             "lightblue": {"color": graphics.Color(0, 130, 130)}, "blue": {"color": graphics.Color(0, 0, 130)},
             "purple": {"color": graphics.Color(130, 0, 130)}, "habGold": {"color": graphics.Color(127, 102, 26)}}
fontSmallest = graphics.Font()
fontSmallest.LoadFont(fontlist[0])
fontSmall = graphics.Font()
fontSmall.LoadFont(fontlist[3])
fontLarge = graphics.Font()
fontLarge.LoadFont(fontlist[21])
fontHuge = graphics.Font()
fontHuge.LoadFont(fontlist[22])
dayBright = 50
nightBright = 10

# Flags
normalfunction = True
wuUpdateInterval = 10
iAmAlone = True
iAmAloneSince = datetime.now()
amIAlone = 10
amIAloneLastChecked = datetime.now()
alarmTime = "901"  # Cant use a time that ends in 0
alarmOn = False
futureTime = date(2019, 4, 1)
diffTime = str(int((futureTime - date.today()).days / 7)) + ", " + str((futureTime - date.today()).days)


def isNight():
    if int(time.strftime("%H")) < 6:
        logging.info('isNight returns True')
        return True
    else:
        logging.info('isNight returns False')
        return False


logging.info('Main - Starting up the Matrices')
# Matrices SetUp and Vars
mx = RGBMatrix(32, 4, 1)
if isNight():
    mx.brightness = nightBright
else:
    mx.brightness = dayBright
canvas = mx.CreateFrameCanvas()
canvas2 = mx.CreateFrameCanvas()
canvi = [canvas, canvas2]


def amIAloneTest():
    print
    'changes screen to an animated gif, and listens for 60 seconds'
    print
    'obviously can be interrupted'
    print
    'if truly alone, set iAmAlone to True, set iAmAloneSince and amIAloneLastChecked to datetime.now().'
    return True


def canvasFlip():
    global canvi, mx
    mx.SwapOnVSync(canvi[0])
    if canvi == [canvas, canvas2]:
        canvi = [canvas2, canvas]
    else:
        canvi = [canvas, canvas2]


def dayCycle():
    ###Schema######################
    ###Canvas1###Canvas2###Sleep###
    ###############################
    ###       ### Swap  ###     ###
    ### Clear ###       ###     ###
    ### Code  ###       ###     ###
    ###       ###       ###Sleep###
    ### Swap  ###       ###     ###
    ###       ### Clear ###     ###
    ###       ### Code  ###     ###
    ###       ###       ###Sleep###
    ###############################
    logging.info('Main - Starting another DayCycle')
    for n in range(6):
        canvasFlip()
        canvi[0].Clear()

        # Trying to generally move from left to right.
        # Time
        graphics.DrawText(canvi[0], fontLarge, 1, 15, colorDict['purple']['color'], time.strftime("%H"))
        graphics.DrawText(canvi[0], fontLarge, 1, 30, colorDict['purple']['color'], time.strftime("%M"))
        graphics.DrawText(canvi[0], fontSmall, 22, 8, colorDict['purple']['color'],
                          str(datetime.now().month) + '/' + str(datetime.now().day))

        # Todo: Add Sun, Cloud, and Rain.
        # WU
        graphics.DrawText(canvi[0], fontSmall, 22, 23, colorDict['green']['color'], wu_helper.getTemp())
        graphics.DrawText(canvi[0], fontSmallest, 34, 19, colorDict['green']['color'], 'o')
        graphics.DrawText(canvi[0], fontSmall, 22, 30, colorDict['blue']['color'], wu_helper.getLow())
        graphics.DrawText(canvi[0], fontSmall, 32, 30, colorDict['green']['color'], '|')
        graphics.DrawText(canvi[0], fontSmall, 36, 30, colorDict['red']['color'], wu_helper.getHigh())
        if wu_helper.rainToday():
            graphics.DrawText(canvi[0], fontSmall, 47, 30, colorDict['blue']['color'], 'U')

        # Stats
        if todoist_helper.get_karma_trend() == 'up':
            graphics.DrawText(canvi[0], fontLarge, 128 - (10 * len(str(todoist_helper.get_karma()))), 15,
                              colorDict['green']['color'], str(todoist_helper.get_karma()))
        else:
            graphics.DrawText(canvi[0], fontLarge, 128 - (10 * len(str(todoist_helper.get_karma()))), 15,
                              colorDict['red']['color'], str(todoist_helper.get_karma()))
        graphics.DrawText(canvi[0], fontLarge, 128 - (10 * len(diffTime)), 30, colorDict['lightblue']['color'],
                          diffTime)
        time.sleep(5)


def nightCycle():
    logging.info('Main - Starting another Night Cycle')
    for n in range(1):
        canvasFlip()
        canvi[0].Clear()
        # Trying to generally move from left to right.
        # Time
        graphics.DrawText(canvi[0], fontHuge, 0, 29, colorDict['purple']['color'], time.strftime("%H:%M"))
        # Todo: Add Sun, Cloud, and Rain.
        # WU
        graphics.DrawText(canvi[0], fontLarge, 100, 29, colorDict['green']['color'], wu_helper.getTemp())
        graphics.DrawText(canvi[0], fontSmall, 119, 19, colorDict['green']['color'], "o")


def sleepScreen():
    print
    "Should turn all pixels off, and start a listener for the room, listening for noise"
    print
    "Maybe a while loop using the iAmAlone flag, which resets if it senses sound."


def go(currentlyLogging=False):
    while normalfunction:
        if isNight() and iAmAlone:
            if not mx.brightness == nightBright:
                mx.brightness = nightBright
                canvasFlip()
                mx.brightness = nightBright
            nightCycle()
            # If 30 minutes past iAmAloneSince, do screenOff()
            time.sleep(60)  # remove this line once the listener is implemented
            # For loop 30-60 times, something that listens for one second.
            # If that function senses sound, it should flip the iAmAlone flag to False, change the aloneSince flag to datetime.now(), and break from the loop so that we can escape this if clause.
        elif False:  # replace False with iAmAlone flag.
            print
            "shouldn't be here..."
            # sleepScreen()
        else:  # daytime function
            if mx.brightness == nightBright:
                logging.info('Switching night to day brightness')
                mx.brightness = dayBright
                canvasFlip()
                mx.brightness = dayBright
                canvasFlip()
                logging.info('Made it through brightness switching')
            dayCycle()
            # if time since last amIAloneLastChecked > 10 minutes, do a quickCheck
            # if iAmAloneQuickCheck():#something like 10 seconds
            #   if iAmAloneTest():
            #       sleepScreen()

        # Commented out the next few lines to make sure no fancy stuff happens for the next few weeks while I work out kinks. 8/13/16
        # #Should I wake you up?
        # if not alarmOn and datetime.now().hour == int(alarmTime[:1]):
        # if int(alarmTime[1:]) -1 < datetime.now().minute < int(alarmTime[1:])+1:
        # soundTheAlarm()

        # if alarmOn and int(alarmTime[1:])+53 <datetime.now().minute < int(alarmTime[1:])+55:
        # killTheAlarm()

        # Update WU
        if datetime.now().replace(tzinfo=wu_helper.getLastLoadTime().tzinfo) > (
                wu_helper.getLastLoadTime() + timedelta(minutes=wuUpdateInterval)):
            logging.info('Updating WuHelper')
            wu_helper.updateWU()


def soundTheAlarm():
    global alarmOn
    alarmOn = True
    subprocess.call(["irsend", "SEND_ONCE", "NAD", "KEY_POWER"])
    time.sleep(1)
    subprocess.call(["irsend", "SEND_ONCE", "NAD", "KEY_POWER"])
    time.sleep(1)
    subprocess.call(["irsend", "SEND_ONCE", "NAD", "KEY_8"])
    time.sleep(1)
    subprocess.call(["irsend", "SEND_ONCE", "NAD", "KEY_8"])
    subprocess.call("mpsyt pl PLZk6LMCIBnIs-BCrKQcwtnaN_Gk196NkC, shuffle, all > /dev/null < /dev/null &", shell=True)


def killTheAlarm():
    global alarmOn
    alarmOn = False
    # this beautiful line came from http://stackoverflow.com/questions/3510673/find-and-kill-a-process-in-one-line-using-bash-and-regex
    subprocess.call("sudo kill $(ps aux | grep 'mpsyt' | awk '{print $2}')", shell=True)
    subprocess.call(["irsend", "SEND_ONCE", "NAD", "KEY_3"])
    subprocess.call(["irsend", "SEND_ONCE", "NAD", "KEY_3"])
    time.sleep(1)
    subprocess.call(["irsend", "SEND_ONCE", "NAD", "KEY_SLEEP"])
    subprocess.call(["irsend", "SEND_ONCE", "NAD", "KEY_SLEEP"])


def jasperFlash():  # Wow this shit is insane. Too bad it doesn't work.
    graphics.DrawLine(mx, 0, 0, 127, 0, colorDict['lightblue']['color'])
    graphics.DrawLine(mx, 127, 0, 127, 31, colorDict['lightblue']['color'])
    graphics.DrawLine(mx, 127, 31, 0, 31, colorDict['lightblue']['color'])
    graphics.DrawLine(mx, 0, 31, 0, 0, colorDict['lightblue']['color'])
    graphics.DrawLine(mx, 0, 0, 127, 0, colorDict['black']['color'])
    graphics.DrawLine(mx, 127, 0, 127, 31, colorDict['black']['color'])
    graphics.DrawLine(mx, 127, 31, 0, 31, colorDict['black']['color'])
    graphics.DrawLine(mx, 0, 31, 0, 0, colorDict['black']['color'])
    graphics.DrawLine(mx, 0, 0, 127, 0, colorDict['lightblue']['color'])
    graphics.DrawLine(mx, 127, 0, 127, 31, colorDict['lightblue']['color'])
    graphics.DrawLine(mx, 127, 31, 0, 31, colorDict['lightblue']['color'])
    graphics.DrawLine(mx, 0, 31, 0, 0, colorDict['lightblue']['color'])
    time.sleep(3)
    graphics.DrawLine(mx, 0, 0, 127, 0, colorDict['black']['color'])
    graphics.DrawLine(mx, 127, 0, 127, 31, colorDict['black']['color'])
    graphics.DrawLine(mx, 127, 31, 0, 31, colorDict['black']['color'])
    graphics.DrawLine(mx, 0, 31, 0, 0, colorDict['black']['color'])


def getMatrix():
    return mx


# Main function
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename="Matrixlogfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info('Starting Go')
    go(True)
    logging.info('Exiting for some reason?')
