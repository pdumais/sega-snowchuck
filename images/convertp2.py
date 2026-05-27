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
import json
from math import sqrt

"""
sprlist = [
    "bad11.spr24",
    "bad21.spr24",
    "bad31.spr24",
    "bad41.spr24",
    "bad51.spr24",
    "bad12.spr24",
    "bad22.spr24",
    "bad32.spr24",
    "bad42.spr24",
    "bad52.spr24",
    "bad13.spr24",
    "bad23.spr24",
    "bad33.spr24",
    "bad43.spr24",
    "bad53.spr24",
    "bad14.spr24",
    "bad24.spr24",
    "bad34.spr24",
    "bad44.spr24",
    "bad54.spr24",
    "obj1.spr24",
    "obj2.spr24",
    "obj3.spr24",
    "obj4.spr24",
    "obj5.spr24",
    "obj6.spr24",
    "obj7.spr24",
    "obj8.spr24",
    "obj9.spr24",
    "cube1.spr24",
    "cube2.spr24",
    "cube3.spr24",
    "cube4.spr24",
    "cube5.spr24",
    "cube6.spr24",
    "cube7.spr24",
    "cube8.spr24",
    "cube9.spr24",
    "cube10.spr24",
    "cube11.spr24",
    "cube12.spr24",
    "cube13.spr24",
    "cube14.spr24",
    "cube15.spr24",
    "cube16.spr24",
    "cube17.spr24",
    "cube18.spr24",
    "cube19.spr24",
    "cube20.spr24",
    "cube21.spr24",
    "cube22.spr24",
    "cube23.spr24",
    "cube24.spr24",
    "cube25.spr24",
    "cube26.spr24",
    "cube27.spr24",
    "cube36.spr24",
    "cube37.spr24",
    "cube38.spr24",
    "cube39.spr24",
    "cube40.spr24",
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
    "water1",
    "water2",
    "water3",
]


palette = [
    (0, 0, 0),
    (0, 0, 170),
    (0, 170, 0),
    (0, 170, 170),
    (170, 0, 0),
    (170, 0, 170),
    (170, 85, 0),
    (170, 170, 170),
    (85, 85, 85),
    (85, 85, 255),
    (85, 255, 85),
    (85, 255, 255),
    (255, 85, 85),
    (255, 85, 255),
    (255, 255, 85),
    (255, 255, 255),
    (0, 0, 0),
    (20, 20, 20),
    (32, 32, 32),
    (44, 44, 44),
    (56, 56, 56),
    (68, 68, 68),
    (80, 80, 80),
    (96, 96, 96),
    (112, 112, 112),
    (128, 128, 128),
    (144, 144, 144),
    (160, 160, 160),
    (180, 180, 180),
    (200, 200, 200),
    (224, 224, 224),
    (255, 255, 255),
    (0, 0, 255),
    (64, 0, 255),
    (128, 0, 255),
    (192, 0, 255),
    (255, 0, 255),
    (255, 0, 192),
    (255, 0, 128),
    (255, 0, 64),
    (255, 0, 0),
    (255, 64, 0),
    (255, 128, 0),
    (255, 192, 0),
    (255, 255, 0),
    (192, 255, 0),
    (128, 255, 0),
    (64, 255, 0),
    (0, 255, 0),
    (0, 255, 64),
    (0, 255, 128),
    (0, 255, 192),
    (0, 255, 255),
    (0, 192, 255),
    (0, 128, 255),
    (0, 64, 255),
    (128, 128, 255),
    (160, 128, 255),
    (192, 128, 255),
    (224, 128, 255),
    (255, 128, 255),
    (255, 128, 224),
    (255, 128, 192),
    (255, 128, 160),
    (255, 128, 128),
    (255, 160, 128),
    (255, 192, 128),
    (255, 224, 128),
    (255, 255, 128),
    (224, 255, 128),
    (192, 255, 128),
    (160, 255, 128),
    (128, 255, 128),
    (128, 255, 160),
    (128, 255, 192),
    (128, 255, 224),
    (128, 255, 255),
    (128, 224, 255),
    (128, 192, 255),
    (128, 160, 255),
    (184, 184, 255),
    (200, 184, 255),
    (216, 184, 255),
    (232, 184, 255),
    (255, 184, 255),
    (255, 184, 232),
    (255, 184, 216),
    (255, 184, 200),
    (255, 184, 184),
    (255, 200, 184),
    (255, 216, 184),
    (255, 232, 184),
    (255, 255, 184),
    (232, 255, 184),
    (216, 255, 184),
    (200, 255, 184),
    (184, 255, 184),
    (184, 255, 200),
    (184, 255, 216),
    (184, 255, 232),
    (184, 255, 255),
    (184, 232, 255),
    (184, 216, 255),
    (184, 200, 255),
    (0, 0, 112),
    (28, 0, 112),
    (56, 0, 112),
    (84, 0, 112),
    (112, 0, 112),
    (112, 0, 84),
    (112, 0, 56),
    (112, 0, 28),
    (112, 0, 0),
    (112, 28, 0),
    (112, 56, 0),
    (112, 84, 0),
    (112, 112, 0),
    (84, 112, 0),
    (56, 112, 0),
    (28, 112, 0),
    (0, 112, 0),
    (0, 112, 28),
    (0, 112, 56),
    (0, 112, 84),
    (0, 112, 112),
    (0, 84, 112),
    (0, 56, 112),
    (0, 28, 112),
    (56, 56, 112),
    (68, 56, 112),
    (84, 56, 112),
    (96, 56, 112),
    (112, 56, 112),
    (112, 56, 96),
    (112, 56, 84),
    (112, 56, 68),
    (112, 56, 56),
    (112, 68, 56),
    (112, 84, 56),
    (112, 96, 56),
    (112, 112, 56),
    (96, 112, 56),
    (84, 112, 56),
    (68, 112, 56),
    (56, 112, 56),
    (56, 112, 68),
    (56, 112, 84),
    (56, 112, 96),
    (56, 112, 112),
    (56, 96, 112),
    (56, 84, 112),
    (56, 68, 112),
    (80, 80, 112),
    (88, 80, 112),
    (96, 80, 112),
    (104, 80, 112),
    (112, 80, 112),
    (112, 80, 104),
    (112, 80, 96),
    (112, 80, 88),
    (112, 80, 80),
    (112, 88, 80),
    (112, 96, 80),
    (112, 104, 80),
    (112, 112, 80),
    (104, 112, 80),
    (96, 112, 80),
    (88, 112, 80),
    (80, 112, 80),
    (80, 112, 88),
    (80, 112, 96),
    (80, 112, 104),
    (80, 112, 112),
    (80, 104, 112),
    (80, 96, 112),
    (80, 88, 112),
    (0, 0, 64),
    (16, 0, 64),
    (32, 0, 64),
    (48, 0, 64),
    (64, 0, 64),
    (64, 0, 48),
    (64, 0, 32),
    (64, 0, 16),
    (64, 0, 0),
    (64, 16, 0),
    (64, 32, 0),
    (64, 48, 0),
    (64, 64, 0),
    (48, 64, 0),
    (32, 64, 0),
    (16, 64, 0),
    (0, 64, 0),
    (0, 64, 16),
    (0, 64, 32),
    (0, 64, 48),
    (0, 64, 64),
    (0, 48, 64),
    (0, 32, 64),
    (0, 16, 64),
    (32, 32, 64),
    (40, 32, 64),
    (48, 32, 64),
    (56, 32, 64),
    (64, 32, 64),
    (64, 32, 56),
    (64, 32, 48),
    (64, 32, 40),
    (64, 32, 32),
    (64, 40, 32),
    (64, 48, 32),
    (64, 56, 32),
    (64, 64, 32),
    (56, 64, 32),
    (48, 64, 32),
    (40, 64, 32),
    (32, 64, 32),
    (32, 64, 40),
    (32, 64, 48),
    (32, 64, 56),
    (32, 64, 64),
    (32, 56, 64),
    (32, 48, 64),
    (32, 40, 64),
    (44, 44, 64),
    (48, 44, 64),
    (52, 44, 64),
    (60, 44, 64),
    (64, 44, 64),
    (64, 44, 60),
    (64, 44, 52),
    (64, 44, 48),
    (64, 44, 44),
    (64, 48, 44),
    (64, 52, 44),
    (64, 60, 44),
    (64, 64, 44),
    (60, 64, 44),
    (52, 64, 44),
    (48, 64, 44),
    (44, 64, 44),
    (44, 64, 48),
    (44, 64, 52),
    (44, 64, 60),
    (44, 64, 64),
    (44, 60, 64),
    (44, 52, 64),
    (44, 48, 64),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
]


def rotate_90_clockwise(grid):
    N = len(grid)  # assumes 24 for your case
    return [[grid[N - 1 - y][x] for y in range(N)] for x in range(N)]


MAX_COLORS = 56

# Perceptual weights (luma coefficients) — emphasize green, de-emphasize blue.
W_R, W_G, W_B = 0.30, 0.59, 0.11


def color_distance_sq(c1, c2):
    dr = c1[0] - c2[0]
    dg = c1[1] - c2[1]
    db = c1[2] - c2[2]
    return W_R * dr * dr + W_G * dg * dg + W_B * db * db


def kmeans_pp_init(points, k, rng):
    centroids = [rng.choice(points)]
    for _ in range(k - 1):
        # Distance from each point to its nearest existing centroid.
        d2 = [min(color_distance_sq(p, c) for c in centroids) for p in points]
        total = sum(d2)
        if total == 0:
            # All remaining points already coincide with a centroid.
            centroids.append(rng.choice(points))
            continue
        r = rng.random() * total
        acc = 0.0
        for p, d in zip(points, d2):
            acc += d
            if acc >= r:
                centroids.append(p)
                break
    return centroids


def reduce_palette(palette256, max_colors=MAX_COLORS, max_iter=50, seed=0):
    # Deduplicate: identical RGB entries should map to the same cluster.
    unique = list({c: None for c in palette256}.keys())

    # If we already have <= max_colors distinct colors, no reduction needed.
    if len(unique) <= max_colors:
        reduced = unique
        lookup = {c: i for i, c in enumerate(reduced)}
        return reduced, [lookup[c] for c in palette256]

    rng = random.Random(seed)
    centroids = kmeans_pp_init(unique, max_colors, rng)

    assignments = [0] * len(unique)
    for _ in range(max_iter):
        changed = False

        # --- Assignment step ---
        for i, p in enumerate(unique):
            best, best_d = 0, float("inf")
            for j, c in enumerate(centroids):
                d = color_distance_sq(p, c)
                if d < best_d:
                    best_d, best = d, j
            if assignments[i] != best:
                assignments[i] = best
                changed = True

        # --- Update step ---
        sums = [[0.0, 0.0, 0.0] for _ in range(max_colors)]
        counts = [0] * max_colors
        for p, a in zip(unique, assignments):
            sums[a][0] += p[0]
            sums[a][1] += p[1]
            sums[a][2] += p[2]
            counts[a] += 1

        new_centroids = []
        for j in range(max_colors):
            if counts[j] == 0:
                # Empty cluster: re-seed on the farthest unique point.
                farthest = max(
                    unique,
                    key=lambda p: min(color_distance_sq(p, c) for c in centroids),
                )
                new_centroids.append(farthest)
                changed = True
            else:
                new_centroids.append(
                    (
                        sums[j][0] / counts[j],
                        sums[j][1] / counts[j],
                        sums[j][2] / counts[j],
                    )
                )
        centroids = new_centroids
        if not changed:
            break

    # Final integer palette (clamped to byte range).
    reduced_palette = [
        (
            max(0, min(255, round(r))),
            max(0, min(255, round(g))),
            max(0, min(255, round(b))),
        )
        for r, g, b in centroids
    ]

    # reduced_palette = [(r&7,g&7,b&7) for r,g,b in reduced_palette]

    # Build the 256-entry remap by snapping each original color to its cluster.
    unique_to_cluster = {p: a for p, a in zip(unique, assignments)}
    remap = [unique_to_cluster[c] for c in palette256]

    return reduced_palette, remap

    # def convert(input_file, output_file):
    #    with open(input_file, "rb") as f:
    #        header = f.read(4)
    #        if len(header) < 4:
    #            raise ValueError("File too small")
    #
    #        tx, ty = struct.unpack("<HH", header)
    #
    #        width = tx + 1
    #        height = ty
    #
    #        remaining = f.read()
    #
    #    if width > 24 or height > 24:
    #        print(f"ERROR Image too big: {width}x{height}")
    #        return None
    #
    #    if (width * height) > len(remaining):
    #        height = height - 1
    #
    #    offsetx = math.floor((24 - width) / 2)
    #    offsety = math.floor((24 - height) / 2)
    #    grid = [[0] * 24 for _ in range(24)]
    #
    #    i = 0
    #    for y in range(height):
    #        for x in range(width):
    #            v = remaining[i]
    #            grid[x + offsetx][y + offsety] = v
    #            i = i + 1
    #
    #    return grid


def grids_to_sprite_sheet(grids: dict, pal, pal2, output):
    tile_size = 24
    names = list(grids.keys())
    count = len(names)

    # compute grid layout (rough square)
    cols = math.ceil(math.sqrt(count))
    rows = math.ceil(count / cols)

    sheet_w = cols * tile_size * 2
    sheet_h = rows * tile_size

    img = Image.new("RGBA", (sheet_w, sheet_h))

    for i, name in enumerate(names):
        grid = grids[name]["original"]
        grid2 = grids[name]["reduced"]

        tx = (i % cols) * tile_size * 2
        ty = (i // cols) * tile_size

        for y in range(tile_size):
            for x in range(tile_size):
                v = pal[grid[y][x]]
                r, g, b = v
                a = 255
                img.putpixel((tx + x, ty + y), (r, g, b, a))

        tx = tx + tile_size
        for y in range(tile_size):
            for x in range(tile_size):
                v = pal2[grid2[y][x]]
                r, g, b = v
                a = 255
                img.putpixel((tx + x, ty + y), (r, g, b, a))

    img.save(output)


def gen_palette(sprites, reduced_palette, prefix):
    cols = {}
    sets = []
    for key in sprites:
        g = sprites[key]["reduced"]
        s = []
        for c in sum(g, []):
            if c == 0:
                continue
            if c not in cols:
                cols[c] = 0
            cols[c] = cols[c] + 1
            if c not in s:
                s.append(c)
        sprites[key]["colset"] = s
        sets.append(s)

    sets = {frozenset(b) for b in sets}
    sets = [s for s in sets if not any(s < t for t in sets)]
    clusters = exact_partition(sets, max_groups=4)
    print(f"Total cols: {len(cols)}")
    if clusters == None:
        print("Too many colors")
        return

    # Check it
    sprites_pal = []
    i = 0
    for key in sprites:
        g = sprites[key]["reduced"]
        flat = sum(g, [])
        pal = None
        candidate_pal = [{"index": i, "pal": p} for i, p in enumerate(clusters)]
        for c in flat:
            if c == 0:
                continue
            for p in candidate_pal:
                if c not in p["pal"]:
                    candidate_pal.remove(p)
        if len(candidate_pal) < 1:
            raise ValueError("no common set")
        pal_index = candidate_pal[0]["index"]
        flags = 0
        if key in ["cube36", "cube37", "cube38", "cube39", "cube40"]:
            flags = 1
        i = i + 1
        sprites_pal.append((pal_index, flags, key))

    # If less than 4 palettes needed, create the other ones with zeros only
    if len(clusters) < 4:
        clusters.extend([[]] * (4 - len(clusters)))

    p = 0
    ret = ""
    palettes = []
    for cluster in clusters:
        ret = ret + f"    xdef {prefix}_palette{p}\n"
        ret = ret + f"{prefix}_palette{p}:\n"
        if len(cluster) > 15:
            raise ValueError("Palette too big")
        lst = list(cluster)
        palette_colors = [0]
        for col in lst:
            if col == 0:
                c = 0
            else:
                r, g, b = reduced_palette[col]
                c = (
                    (int(r * 7 / 256) << 1)
                    | (int(g * 7 / 256) << 5)
                    | (int(b * 7 / 256) << 9)
                )
            if c not in palette_colors:
                palette_colors.append(c)
        if len(palette_colors) < 16:
            palette_colors.extend([0] * (16 - len(palette_colors)))
        for c in palette_colors:
            ret = ret + f"    dc.w ${c:04X}\n"
        palettes.append(palette_colors)
        p = p + 1

    return (palettes, sprites_pal)


def exact_partition(buckets, max_groups=4, max_size=15):
    # Sort by descending size — fail fast on the hardest buckets first.
    buckets = sorted([set(b) for b in buckets], key=len, reverse=True)
    groups = [set() for _ in range(max_groups)]
    used = 0  # how many groups have been opened so far

    def backtrack(idx):
        nonlocal used
        if idx == len(buckets):
            return [g.copy() for g in groups if g]

        b = buckets[idx]

        # Try existing non-empty groups first (symmetry breaking).
        for g in range(used):
            if len(groups[g] | b) <= max_size:
                before = groups[g].copy()
                groups[g] |= b
                result = backtrack(idx + 1)
                if result is not None:
                    return result
                groups[g] = before

        # Open a new group if allowed.
        if used < max_groups:
            groups[used] = set(b)
            used += 1
            result = backtrack(idx + 1)
            if result is not None:
                return result
            used -= 1
            groups[used] = set()

        return None

    return backtrack(0)


def read(fmt, f):
    size = struct.calcsize(fmt)
    data = f.read(size)
    if len(data) != size:
        raise EOFError("Unexpected end of file")
    return struct.unpack(fmt, data)


# --- record readers ---


def read_ground(f):
    ground = []
    for _ in range(1000):
        num = list(read("5B", f))  # 5 bytes
        y = list(read("5H", f))  # 5 words (unsigned short)
        ground.append({"num": num, "y": y})
    return ground


def read_badguy(f):
    badguy = []
    for _ in range(30):
        num = read("B", f)[0]
        plus = read("b", f)[0]  # signed
        maxx = read("i", f)[0]
        minx = read("i", f)[0]
        x = read("i", f)[0]
        y = read("i", f)[0]
        p = read("I", f)[0]  # pointer (raw value)
        badguy.append(
            {
                "num": num,
                "plus": plus,
                "maxx": maxx,
                "minx": minx,
                "x": x,
                "y": y,
                "p": p,
            }
        )
    return badguy


def read_thing(f):
    thing = []
    for _ in range(30):
        num = read("B", f)[0]
        x = read("i", f)[0]
        y = read("i", f)[0]
        p = read("I", f)[0]
        ena = read("?", f)[0]
        thing.append({"num": num, "x": x, "y": y, "p": p, "ena": ena})
    return thing


def parse_levels(fname):
    levels = {}
    with open(fname, "rb") as f:
        maxlevel = read("B", f)[0]
        levels = {"max": maxlevel, "levels": []}
        for _ in range(maxlevel):
            levels["levels"].append(
                {
                    "endlev": read("i", f)[0],
                    "backname": f.read(13).rstrip(b"\x00").decode(errors="ignore"),
                    "tmax": read("H", f)[0],
                    "cmax": read("H", f)[0],
                    "bmax": read("H", f)[0],
                    "thing": read_thing(f),
                    "ground": read_ground(f),
                    "badguys": read_badguy(f),
                }
            )
    for level in levels["levels"]:
        blocks = level["ground"]
        for b in blocks:
            seen = []
            for i in range(5):
                if b["y"][i] not in seen:
                    seen.append(b["y"][i])
                else:
                    b["y"][i] = 255
                    b["num"][i] = 255

    return levels


def get_sprites_by_level(level):
    sprites = []
    for i in range(level["bmax"]):
        num = level["badguys"][i]["num"]
        for n in range(4):
            sprites.append(f"bad{num}{n+1}")

    for i in range(level["tmax"]):
        num = level["thing"][i]["num"]
        sprites.append(f"obj{num}")

    for i in range(level["cmax"]):
        for n in range(5):
            if level["ground"][i]["y"][n] < 181:
                num = level["ground"][i]["num"][n]
                sprites.append(f"cube{num}")

    return basesprlist + list(set(sprites))
"""


def gen_asm(levels, pal_data, sprite_name_to_index):
    with open("levels.vasm", "w") as f:
        f.write("; Snowchuck\n")
        f.write("; Patrick Dumais\n")
        f.write("; File generated by convert.py\n")
        f.write("    section .rodata\n")

        # Inject background colors in first available spot
        f.write(f"  xdef level_0_bg\n")

        l = 0
        for level in levels["levels"]:
            prefix = f"level_{l}"
            bg = level["bgcol"]
            f.write(f"{prefix}_bg: dc.w ${bg:04X}\n")
            l = l + 1

        # Write all palettes
        level = 0
        for d in pal_data:
            palettes = d[0]
            prefix = f"level_{level}"
            level = level + 1

            p = 0
            for pal in palettes:
                f.write(f"    xdef {prefix}_palette{p}\n")
                f.write(f"{prefix}_palette{p}:\n")
                p = p + 1
                for idx, c in enumerate(pal):
                    f.write(f"    dc.w ${c:04X}\n")

        level = 0
        for d in pal_data:
            sprite_pal = d[1]
            prefix = f"level_{level}"
            f.write(f"{prefix}_ref_start:\n")

            # This will produce a list with a predictable position for hero, endp and dead. And all bad guys
            # Will be sequential so that badX2 comes after badX1 ...
            list_without_bad_guys = [
                pdata for pdata in sprite_pal if not pdata[2].startswith("bad")
            ]
            list_of_bad_guys = sorted(
                [pdata for pdata in sprite_pal if pdata[2].startswith("bad")],
                key=lambda t: t[2],
            )
            for pdata in list_without_bad_guys + list_of_bad_guys:
                pal_index = pdata[0]
                flags = pdata[1]
                key = pdata[2]
                f.write(f"{prefix}_sprite_{key}_palette: dc.b {pal_index}\n")
                f.write(f"{prefix}_sprite_{key}_flags:  dc.b {flags}\n")
                f.write(f"{prefix}_sprite_{key}_tile:    dc.l sprite_{key}_tile_0\n")
            f.write(f"{prefix}_sprite_last_palette: dc.b 255\n")
            f.write(f"{prefix}_sprite_last_flags:   dc.b 255\n")
            f.write(f"{prefix}_sprite_last_tile:    dc.l $FFFFFFFF\n")
            level = level + 1

        level = 0
        f.write(f"    xdef level_0_ref\n")
        for level_pal in pal_data:
            f.write(f"level_{level}_ref: dc.l level_{level}_ref_start\n")
            level = level + 1

        # Create list of blocks for each levels
        for idx, level in enumerate(levels["levels"]):
            f.write(f"level_{idx}_blocks: \n")
            for i in range(level["cmax"]):
                for n in range(5):
                    num = level["ground"][i]["num"][n]
                    y = level["ground"][i]["y"][n]
                    f.write(f"    dc.w {num} ; level {idx}, x={i*24}\n")
                    f.write(f"    dc.w {y}\n")

        # Create list of bad guys for each levels
        f.write(f"  section .data\n")
        for idx, level in enumerate(levels["levels"]):
            f.write(f"level_{idx}_bad: \n")
            for i in range(level["bmax"]):
                num = level["badguys"][i]["num"]
                x = level["badguys"][i]["x"]
                y = level["badguys"][i]["y"]
                f.write(f"    dc.w {num} ; level {idx}\n")
                f.write(f"    dc.w {x}\n")
                f.write(f"    dc.w {y}\n")
                f.write(f"    dc.b 1 ; direction \n")
                f.write(f"    dc.b 0 ; deviation\n")


        # Create list of objects for each levels
        for idx, level in enumerate(levels["levels"]):
            f.write(f"level_{idx}_obj: \n")
            for i in range(level["tmax"]):
                num = level["thing"][i]["num"]
                x = level["thing"][i]["x"]
                y = level["thing"][i]["y"]
                f.write(f"    dc.w {num} ; level {idx}\n")
                f.write(f"    dc.w {x}\n")
                f.write(f"    dc.w {y}\n")

        #######################################################################
        f.write(f"  section .rodata\n")
        f.write("    xdef level_blocks_table\nlevel_blocks_table:\n")
        for idx, level in enumerate(levels["levels"]):
            endlev = level["endlev"]
            f.write(
                f"level_blocks_ref_{idx}_blocks:\n    dc.l level_{idx}_blocks\n    dc.w {level['cmax']}\n    dc.w {endlev}\n"
            )

        f.write("    xdef level_badguys_table\nlevel_badguys_table:\n")
        for idx, level in enumerate(levels["levels"]):
            f.write(
                f"level_badguys_ref_{idx}_badguys:\n    dc.l level_{idx}_bad\n    dc.w {level['bmax']}\n"
            )
        f.write("    xdef level_obj_table\nlevel_obj_table:\n")
        for idx, level in enumerate(levels["levels"]):
            f.write(
                f"level_obj_ref_{idx}_obj:\n    dc.l level_{idx}_obj\n    dc.w {level['tmax']+1}\n"
            )

        f.write("    xdef level_objid_table\nlevel_objid_table:\n")
        for idx, level in enumerate(levels["levels"]):
            if "obj1" in sprite_name_to_index[idx]:
                cidx = sprite_name_to_index[idx]["obj1"]
            else:
                cidx = 0xFF
            f.write(f"    dc.w {cidx} ; Level {idx} - Speed \n")
            if "obj2" in sprite_name_to_index[idx]:
                cidx = sprite_name_to_index[idx]["obj2"]
            else:
                cidx = 0xFF
            f.write(f"    dc.w {cidx} ; Level {idx} - Jumper \n")
            if "obj3" in sprite_name_to_index[idx]:
                cidx = sprite_name_to_index[idx]["obj3"]
            else:
                cidx = 0xFF
            f.write(f"    dc.w {cidx} ; Level {idx} - Coffee \n")
            if "obj6" in sprite_name_to_index[idx]:
                cidx = sprite_name_to_index[idx]["obj6"]
            else:
                cidx = 0xFF
            f.write(f"    dc.w {cidx} ; Level {idx} - coin \n")
            if "obj7" in sprite_name_to_index[idx]:
                cidx = sprite_name_to_index[idx]["obj7"]
            else:
                cidx = 0xFF
            f.write(f"    dc.w {cidx} ; Level {idx} - Mushroom \n")
            if "obj8" in sprite_name_to_index[idx]:
                cidx = sprite_name_to_index[idx]["obj8"]
            else:
                cidx = 0xFF
            f.write(f"    dc.w {cidx} ; Level {idx} - Key \n")

            # This is not a typo. We check if key (obj8) exists to know if we want endp or endp2
            if "obj8" in sprite_name_to_index[idx]:
                cidx = sprite_name_to_index[idx]["endp2"]
            else:
                cidx = sprite_name_to_index[idx]["endp"]
            f.write(f"    dc.w {cidx} ; Level {idx} - door \n")
            if "cube36" in sprite_name_to_index[idx]:  # Water
                cidx = sprite_name_to_index[idx]["cube36"]
            else:
                cidx = 0xFF
            f.write(f"    dc.w {cidx} ; Level {idx} - Water \n")


    # Just for debugging. Renders all images in a png
    #grids_to_sprite_sheet(sprites, palette, reduced, "sheet.png")


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
        gen_asm(data["l"], data["p"], data["sprnames"])

