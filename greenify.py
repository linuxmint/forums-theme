#!/usr/bin/python3

import os

class Color():
    def __init__(self, rgb):
        self.rgb = rgb
        self.a = None
        if len(rgb) == 3:
            self.r = rgb[0]
            self.g = rgb[1]
            self.b = rgb[2]
        elif len(rgb) == 6:
            self.r = rgb[0:2]
            self.g = rgb[2:4]
            self.b = rgb[4:6]
        else:
            rgb = rgb.split("rgba(")[1].split(")")[0]
            self.rgb = "rgba(%s)" % rgb
            (r, g, b, self.a) = rgb.split(", ")
            self.r = int(r)
            self.g = int(g)
            self.b = int(b)

    def is_blueish(self):
        if self.a is None:
            r = int(self.r, 16)
            g = int(self.g, 16)
            b = int(self.b, 16)
            return (b > g and b > r)
        else:
            return (self.b > self.g and self.b > self.r)

    def get_green_equivalent(self):
        if self.a is None:
            return self.g + self.b + self.r
        else:
            return ("rgba(%s, %s, %s, %s)" % (self.g, self.b, self.r, self.a))

previous_css = ""
with open("3.1-colours.css") as css:
    previous_css = css.read()

processed = []
with open("colors.css") as list:
    for line in list:
        line = line.strip()
        if line.startswith("//"):
            continue
        elif "#" in line:
            line = line.split(";")[0]
            line = line[1:].replace("#", "")
            (color, new_color) = line.split()
        elif "rgba" in line:
            line = line.split(";")[0]
            (color, new_color) = line.split("-")
        else:
            continue
        os.system("sed -i 's/#%s/#%s/I' theme/*.css" % (color, new_color))
        processed.append(color)

colors = []
color_codes = []
for file in ("theme/colours.css", "theme/base.css", "theme/content.css"):
    with open(file) as css_file:
        for line in css_file:
            if "#" in line:
                line = line.split("#")[1]
                for delimiter in (";", ",", " ", "'"):
                    line = line.split(delimiter)[0]
                if len(line) != 3 and len(line) != 6:
                    continue

                color = Color(line)
                if color.is_blueish() and color.rgb not in color_codes and color.rgb not in processed and color.rgb:
                    colors.append(color)
                    color_codes.append(color.rgb)
            elif "rgba(" in line:
                color = Color(line)
                if color.is_blueish() and color.rgb not in color_codes and color.rgb not in processed and color.rgb:
                    colors.append(color)
                    color_codes.append(color.rgb)

output = []
for color in colors:
    output.append ("%s --> %s" % (color.rgb, color.get_green_equivalent()))
    #os.system("sed -i 's/#%s/#%s/' %s" % (color.rgb, color.get_green_equivalent(), file))

if len(output) > 0:
    print("\nThe following colors are still blueish:\n")
    for line in output:
        print("   " + line)
    print("\nFix them in colors.list. Basic greenified versions are given above for convenience (a basic -120 hue shift is applied).")

print("")