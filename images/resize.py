"""
This script is very hacky. It's a mix of AI generated code and hacks.
It is meant to convert the maps and sprites from snowchuck to a sega compatible format with proper palettes

"""

import struct
from pathlib import Path
import sys
import os
import math
from PIL import Image
import random
from math import sqrt

sprlist = [
    "bad11.spr",
    "bad21.spr",
    "bad31.spr",
    "bad41.spr",
    "bad51.spr",
    "bad12.spr",
    "bad22.spr",
    "bad32.spr",
    "bad42.spr",
    "bad52.spr",
    "bad13.spr",
    "bad23.spr",
    "bad33.spr",
    "bad43.spr",
    "bad53.spr",
    "bad14.spr",
    "bad24.spr",
    "bad34.spr",
    "bad44.spr",
    "bad54.spr",
    "obj1.spr",
    "obj2.spr",
    "obj3.spr",
    "obj4.spr",
    "obj5.spr",
    "obj6.spr",
    "obj7.spr",
    "obj8.spr",
    "obj9.spr",
    "cube1.spr",
    "cube2.spr",
    "cube3.spr",
    "cube4.spr",
    "cube5.spr",
    "cube6.spr",
    "cube7.spr",
    "cube8.spr",
    "cube9.spr",
    "cube10.spr",
    "cube11.spr",
    "cube12.spr",
    "cube13.spr",
    "cube14.spr",
    "cube15.spr",
    "cube16.spr",
    "cube17.spr",
    "cube18.spr",
    "cube19.spr",
    "cube20.spr",
    "cube21.spr",
    "cube22.spr",
    "cube23.spr",
    "cube24.spr",
    "cube25.spr",
    "cube26.spr",
    "cube27.spr",
    "cube36.spr",
    "cube37.spr",
    "cube38.spr",
    "cube39.spr",
    "cube40.spr",
]

basesprlist = [
    "hero1",
    "hero2",
    "hero3",
    "hero4",
    "endp",
    "endp2",
    "dead1",
    "dead2",
    "dead3",
    "dead4",
    "cent2",
    "cent3",
    "cent4",
]

def flip_horizontal(grid):
    return [row[::-1] for row in grid]

def rotate_90_clockwise(grid):
    N = len(grid)  # assumes 24 for your case
    return [[grid[N - 1 - y][x] for y in range(N)] for x in range(N)]



def convert(input_file, output_file):
    with open(input_file, "rb") as f:
        header = f.read(4)
        if len(header) < 4:
            raise ValueError("File too small")

        tx, ty = struct.unpack("<HH", header)

        width = tx + 1
        height = ty

        remaining = f.read()

    if width > 24 or height > 24:
        print(f"ERROR Image too big: {width}x{height}")
        return None

    if (width * height) > len(remaining):
        height = height - 1

    offsetx = math.floor((24 - width) / 2)
    offsety = math.floor((24 - height) / 2)
    grid = [[0] * 24 for _ in range(24)]

    i = 0
    for y in range(height):
        for x in range(width):
            v = remaining[i]
            grid[x + offsetx][y + offsety] = v
            i = i + 1

    return grid

if __name__ == "__main__":
    # Convert all to 24x24 grids
    for src in [f"{f}.spr" for f in basesprlist] + sprlist:
        print("Processing:", src)

        base, _ = os.path.splitext(src)
        dst = base + ".png"
        newf = base + ".spr24"
        grid = flip_horizontal(rotate_90_clockwise(convert(src, dst)))
        with open(newf, "wb") as f:
            for row in grid:
                f.write(bytearray(row))



