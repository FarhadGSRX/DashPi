from math import e
import re
from PIL import Image, ImageFont, ImageDraw
import csv

# For posterity
# {0: graphics.Color(21, 40, 108),
# 130: graphics.Color(21, 41, 114),
# 300: graphics.Color(21, 41, 114),
# 430: graphics.Color(118, 80, 101),
# 600: graphics.Color(253, 193, 17),
# 730: graphics.Color(255, 241, 68),
# 900: graphics.Color(255, 255, 255),
# 1030: graphics.Color(166, 220, 230),
# 1200: graphics.Color(69, 196, 215),
# 1330: graphics.Color(225, 243, 245),
# 1500: graphics.Color(255, 255, 255),
# 1630: graphics.Color(255, 249, 203),
# 1800: graphics.Color(251, 240, 0),
# 1930: graphics.Color(253, 184, 21),
# 2100: graphics.Color(247, 148, 29),
# 2230: graphics.Color(74, 61, 107)


class DateTimeDigitalView:
    font = ImageFont.truetype("Misc/fonts/FUTURAM.ttf", 30)
    font2 = ImageFont.truetype("Misc/fonts/FUTURAM.ttf", 15)
    font3 = ImageFont.truetype("Misc/fonts/FUTURAM.ttf", 12)

    def display_datetime(self, dt: list[str]):
        black_screen = Image.new("RGB", (256, 96), (0, 0, 0))
        draw = ImageDraw.Draw(black_screen)
        the_color = self.color_the_time(int(dt[0]) - 150)
        draw.text(
            (0, 0),
            dt[0],
            self.color_the_time(dt[0]),
            font=self.font,
            stroke_width=1,
            stroke_fill=the_color,
        )
        draw.text(
            (0, 30),
            dt[1],
            self.color_the_time(dt[0]),
            font=self.font2,
            stroke_width=1,
            stroke_fill=the_color,
        )
        draw.text(
            (48, 33),
            dt[2],
            self.color_the_time(dt[0]),
            font=self.font3,
            stroke_width=1,
            stroke_fill=the_color,
        )
        return black_screen

    def color_the_time(self, time):
        if int(time) > 2230:
            return (74, 61, 107)
        elif int(time) > 2100:
            return (247, 148, 29)
        elif int(time) > 1930:
            return (253, 184, 21)
        elif int(time) > 1800:
            return (251, 240, 0)
        elif int(time) > 1630:
            return (255, 249, 203)
        elif int(time) > 1500:
            return (255, 255, 255)
        elif int(time) > 1330:
            return (225, 243, 245)
        elif int(time) > 1200:
            return (69, 196, 215)
        elif int(time) > 1030:
            return (166, 220, 230)
        elif int(time) > 900:
            return (255, 255, 255)
        elif int(time) > 730:
            return (255, 241, 68)
        elif int(time) > 600:
            return (253, 193, 17)
        elif int(time) > 430:
            return (118, 80, 101)
        elif int(time) > 300:
            return (21, 41, 114)
        elif int(time) > 130:
            return (21, 41, 114)
        else:
            return (21, 40, 108)

    # rgb_color_now = color_the_time(time.strftime("%H%M"), adjustment_degree)

    # # fyi, font16 has 2 empty pixels padding in every direction
    # len = graphics.DrawText(
    #     offset_canvas, font16, 0, 56, rgb_color_now, time.strftime("%H%M")
    # )
    # graphics.DrawText(
    #     offset_canvas, font6, 3, 77, rgb_color_now, time.strftime("%a")
    # )
    # graphics.DrawText(
    #     offset_canvas, font5, 3, 91, rgb_color_now, time.strftime("%m/%d")
    # )

    # # Daytime Color Spectrum
    # with open("Misc/colors.csv", "r", encoding="utf-8") as file:
    #     reader = csv.reader(file)
    #     # rows[0] is the time, and it will be indexed by a string of the form "1330"
    #     # rows[1:3] are integers and should be coerced as such
    #     daily_colors = {
    #         rows[0]: (int(rows[1]), int(rows[2]), int(rows[3])) for rows in reader
    #     }

    # with open("Misc/color_adjust_by_degree.csv", "r", encoding="utf-8") as file:
    #     reader = csv.reader(file)
    #     # values are integer degrees and floats with 2 decimal precision
    #     color_adjust = {int(rows[0]): float(rows[1]) for rows in reader}

    # def color_the_time(time, adj_index, adj_mult=30):
    #     rgb_0 = daily_colors[time]
    #     adj_r = ((adj_index * 10) + 90) % 360
    #     adj_g = ((adj_index * 5) + 90) % 360
    #     adj_b = ((adj_index * 20) + 90) % 360
    #     rgb_1 = (
    #         min(max(0, rgb_0[0] + adj_mult * color_adjust[adj_r]), 255),
    #         min(max(0, rgb_0[1] + adj_mult * color_adjust[adj_g]), 255),
    #         min(max(0, rgb_0[2] + adj_mult * color_adjust[adj_b]), 255),
    #     )

    #     adj_r2 = (adj_index * 10) % 360
    #     adj_g2 = (adj_index * 5) % 360
    #     adj_b2 = (adj_index * 20) % 360
    #     rgb_2 = (
    #         min(max(0, rgb_0[0] + adj_mult * color_adjust[adj_r2]), 255),
    #         min(max(0, rgb_0[1] + adj_mult * color_adjust[adj_g2]), 255),
    #         min(max(0, rgb_0[2] + adj_mult * color_adjust[adj_b2]), 255),
    #     )
