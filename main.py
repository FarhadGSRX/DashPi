import sys
import os
import configparser
from PIL import Image

# import logging
import time

# import json
# import subprocess

# from model.weather import WeatherModel
# from view.dashboard import WeatherView
# from presenter.weather_presenter import WeatherPresenter
from model.datetime_digital_model import DateTimeDigitalModel
from view.datetime_digital_view import DateTimeDigitalView
from presenter.datetime_digital_presenter import DateTimeDigitalPresenter

# Yes, you should pipenv install RGBMatrixEmulator TODO: add to documentation

sys.path.append(os.path.dirname(__file__) + "/RGBMatrixEmulator")
sys.path.append(os.path.dirname(__file__) + "/rpi-rgb-led-matrix/bindings/python")

# Demoing on PC? Use these.
import graphics
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions  # , graphics

# Running on Pi? Use these.
# import graphics
# from rgbmatrix import RGBMatrix, RGBMatrixOptions #, graphics


# Load up Config
config = configparser.ConfigParser()
config.read("config.ini")


# from samplebase import SampleBase
options = RGBMatrixOptions()
options.rows = int(config["Matrix Setup"]["rows"])
options.cols = int(config["Matrix Setup"]["cols"])
options.parallel = int(config["Matrix Setup"]["parallel"])
options.chain_length = int(config["Matrix Setup"]["chain_length"])
options.brightness = int(config["Matrix Setup"]["brightness"])
options.gpio_slowdown = int(config["Matrix Setup"]["gpio_slowdown"])
# options.led_limit_refresh = 20
options.hardware_mapping = config["Matrix Setup"]["hardware_mapping"]
options.pixel_mapper_config = config["Matrix Setup"]["pixel_mapper_config"]
options.disable_hardware_pulsing = bool(
    config["Matrix Setup"]["disable_hardware_pulsing"]
)
options.drop_privileges = bool(config["Matrix Setup"]["drop_privileges"])


def set_brightness(matrix):
    int(time.strftime("%H"))
    the_hour = int(time.strftime("%H"))
    if 6 < the_hour and the_hour < 22:
        matrix.brightness = 75
    else:
        matrix.brightness = 25


def main(currentlyLogging=False):
    mx = RGBMatrix(options=options)
    # offset_canvas = mx.CreateFrameCanvas()
    adjustment_degree = 0

    datetime_model = DateTimeDigitalModel()
    datetime_view = DateTimeDigitalView()
    datetime_presenter = DateTimeDigitalPresenter(datetime_model, datetime_view)

    # black_screen = Image.new("RGB", (canvas_width, canvas_height), (0,0,0))
    black_screen = Image.new("RGB", (256, 96), (0, 0, 0))

    scroll_ix = -60
    scroll_iy = 0
    while True:
        if scroll_ix > 230:
            scroll_ix = -60
            scroll_iy += 10
            if scroll_iy > 60:
                scroll_iy = 0
        else:
            scroll_ix += 1
        # if int(time.strftime("%M")) % 30 == 0:
        #     set_brightness(mx)

        next_frame = black_screen.copy()
        next_frame.paste(datetime_presenter.generate(), (scroll_ix, scroll_iy))
        # adjustment_degree += 5
        # if adjustment_degree > 359:
        #     adjustment_degree = 0

        # Displaying color information on screen
        # graphics.DrawText(offset_canvas, font8, 50, 77, rgb_color_now, f"{rgb_color_now[0][0]}/{rgb_color_now[0][1]}/{rgb_color_now[0][2]}")
        # graphics.DrawText(offset_canvas, font8, 50, 91, rgb_color_now, f"{rgb_color_now[1][0]}/{rgb_color_now[1][1]}/{rgb_color_now[1][2]}")

        # mx.SwapOnVSync(next_frame)
        mx.SetImage(next_frame)
        time.sleep(0.15)


def main_new():
    pass
    # model = WeatherModel()
    # view = WeatherView()
    # presenter = WeatherPresenter(model, view)

    # # Initial data load
    # presenter.update_weather_data()


# Main function
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
