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

corrections = {
    "blocks": [
        {
            "op": "add",
            "level": 20,
            "x": 2376,
            "y": 48,
            "type": "16",
        },  # cube16. Proper index will get calculated
        {"op": "add", "level": 20, "x": 2352, "y": 60, "type": "16"},
        {"op": "add", "level": 20, "x": 2400, "y": 48, "type": "16"},
        {"op": "del", "level": 19, "x": 2112, "y": 42},
        {"op": "del", "level": 5, "x": 2424, "y": 160},
        {"op": "del", "level": 5, "x": 2760, "y": 120},
        {"op": "del", "level": 5, "x": 2784, "y": 120},
        {"op": "del", "level": 5, "x": 2808, "y": 120},
        {"op": "del", "level": 5, "x": 2832, "y": 120},
        {"op": "del", "level": 5, "x": 2856, "y": 120},
        {"op": "del", "level": 5, "x": 2880, "y": 120},
        {"op": "del", "level": 5, "x": 2904, "y": 120},
        {"op": "del", "level": 5, "x": 2928, "y": 120},
        {"op": "del", "level": 5, "x": 2952, "y": 120},
        {"op": "del", "level": 5, "x": 3168, "y": 120},
        {"op": "del", "level": 5, "x": 3192, "y": 120},
        {"op": "del", "level": 5, "x": 3216, "y": 120},
        {"op": "del", "level": 5, "x": 3240, "y": 120},
        {"op": "del", "level": 5, "x": 3264, "y": 120},
    ],
    "obj": [
        {
            "op": "add",
            "level": 20,
            "x": 264,
            "y": 168,
            "type": "2",
        },
    ],
}

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
    """k-means++ seeding: pick spread-out initial centroids."""
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
    """
    Returns:
      reduced_palette : list[tuple(int,int,int)]   length <= max_colors
      remap           : list[int]                  length 256, remap[old] = new
    """
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
    """
    img = Image.new("RGBA", (24, 24))
    px = img.load()
    
    for y in range(24):
        for x in range(24):
            v = grid[x][y]

            if v == 0:
                px[x, y] = (0, 0, 0, 0)
            else:
                r, g, b = palette[v]
                px[x, y] = (r, g, b, 255)

    img.save(output_file, "PNG")
    """


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


# This function generates the sprites data. It splits the 24x24 sprite into 9 8x8 tiles
# It writes them in the order required by the VPD (top-down, left-right). Each value is a word representing RGB and NOT the palette index
def gen_sprites(sprites, reduced):
    ret = """
    ; Sprite data is stored as RGB value (3bit). They will need to be mapped to palette before loading in vram\n
    section .rodata\n"""

    for key in sprites:
        ret += f"    xdef sprite_{key}_tile_0\n"

    for key in sprites:
        grid2 = sprites[key]["reduced"]
        subgrids = []

        for block_y in range(0, 24, 8):
            for block_x in range(0, 24, 8):
                flat = [
                    grid2[y][x]
                    for y in range(block_y, block_y + 8)
                    for x in range(block_x, block_x + 8)
                ]
                subgrids.append(flat)
        i = 0
        for tile in [
            subgrids[0],
            subgrids[3],
            subgrids[6],
            subgrids[1],
            subgrids[4],
            subgrids[7],
            subgrids[2],
            subgrids[5],
            subgrids[8],
        ]:
            ret += f"sprite_{key}_tile_{i}:\n"
            i = i + 1
            for b in tile:
                if b == 0:
                    c = 0
                else:
                    r, g, b = reduced[b]
                    c = (
                        (int(r * 7 / 256) << 1)
                        | (int(g * 7 / 256) << 5)
                        | (int(b * 7 / 256) << 9)
                    )
                ret = ret + f"    dc.w ${c:04X}\n"
    return ret


def convert_y(y):
    # We're trying to scale back to 24px height
    newy = ((y / 20) / 10) * 9 * 24
    alignedOn8 = math.floor(newy / 8) * 8
    return int(alignedOn8)


def load_grid_24x24(filename):
    expected_size = 24 * 24
    data = bytearray()

    with open(filename, "rb") as f:
        while len(data) < expected_size:
            chunk = f.read(expected_size - len(data))
            if not chunk:  # EOF reached
                break
            data.extend(chunk)

    if len(data) != expected_size:
        raise ValueError(f"Expected {expected_size} bytes, got {len(data)}")

    return [list(data[i * 24 : (i + 1) * 24]) for i in range(24)]


def fix_y(level, idx, y, blocks):
    # is it within a block?
    fix = True
    while fix:
        fix = False
        if level == 30 and idx == 0:
            print(blocks["y"])
        for by in blocks["y"]:
            if by > 180:
                continue
            by = convert_y(by)
            if level == 30 and idx == 0:
                print(f"y: {y}, b={by}")
            if y >= (by + 24):
                continue
            if (y + 24) <= by:
                continue
            y = by - 24
            if level == 30 and idx == 0:
                print(f"fix")
            fix = True

    # is it floating?
    """
    lastdelta = 0xFFFF
    lastby = y
    for by in blocks["y"]:
        by = convert_y(by)
        if (y + 24) >= by:
            continue
        delta = by - y
        if delta < lastdelta:
            lastdelta = delta
            lastby = by - 24
    if lastdelta != 0:
        y = lastby
    """
    return y


def rol_columns(grid, shift):
    shift %= 24

    shift %= 24
    return [row[-shift:] + row[:-shift] for row in grid]


def make_corrections(levels, sprite_name_to_index):
    for b in corrections["blocks"]:
        if b["op"] == "add":
            index = int(b["x"] / 24)
            key = b["type"]
            level = levels[int(b["level"])]
            spr_index = key  # sprite_name_to_index[b["level"]][key]
            found = False
            for n in range(5):
                if level["ground"][index]["y"][n] > 180:
                    found = True
                    level["ground"][index]["y"][n] = b["y"]
                    level["ground"][index]["num"][n] = spr_index
                    level["ground"][index][f"fix{n}"] = True
            if not found:
                raise ValueError("Could not make corrections")
        if b["op"] == "del":
            index = int(b["x"] / 24)
            level = levels[int(b["level"])]
            found = False
            for n in range(5):
                if level["ground"][index]["y"][n] == b["y"]:
                    found = True
                    level["ground"][index]["y"][n] = 181
            if not found:
                raise ValueError("Could not make corrections")
    for b in corrections["obj"]:
        if b["op"] == "add":
            key = b["type"]
            level = levels[int(b["level"])]
            obj = {"num": key, "x": b["x"], "y": b["y"], "fix": True}
            level["thing"][level["tmax"]] = obj
            # level["tmax"] = level["tmax"] + 1


if __name__ == "__main__":

    levels = parse_levels("chuck.map")

    sprites = {}
    reduced, remap = reduce_palette(palette, max_colors=56)

    # Convert all to 24x24 grids
    for src in [f"{f}.spr24" for f in basesprlist] + sprlist:
        print("Processing:", src)

        base, _ = os.path.splitext(src)
        # dst = base + ".png"
        # grid = rotate_90_clockwise(convert(src, dst))
        grid = load_grid_24x24(src)
        if grid != None:
            if base == "water2":
                grid = rol_columns(sprites["water1"]["original"], 8)
            if base == "water3":
                grid = rol_columns(sprites["water1"]["original"], 16)
            sprites[base] = {"original": grid, "reduced": None}

    # Make a copy with reduced palette
    for key in sprites:
        grid = sprites[key]["original"]
        grid2 = [[0] * 24 for _ in range(24)]
        for y in range(24):
            for x in range(24):
                pixel = grid[x][y]
                grid2[x][y] = remap[pixel] if pixel != 0 else 0
        sprites[key]["reduced"] = grid2

    pal_data = []
    i = 0

    for level in levels["levels"]:
        # print(f"\nLevel {i}")
        level_sprites_names = get_sprites_by_level(level)

        level_sprites = {}
        for s in level_sprites_names:
            # print(f"\t{s}")
            level_sprites[s] = sprites[s]

        level_palette, sprite_palettes = gen_palette(
            level_sprites, reduced, f"level_{i}"
        )
        pal_data.append((level_palette, sprite_palettes))
        i = i + 1

    for level, d in enumerate(pal_data):
        palettes = d[0]

        found = None
        for p, pal in enumerate(palettes):
            if found != None:
                break
            for i, c in enumerate(pal[1:]):
                if c == 0:
                    found = ((p & 3) << 4) + (i + 1)
                    palettes[p][i + 1] = 0x0E22  # All background will be light blue
                    levels["levels"][level]["bgcol"] = found
                    break

    sprite_name_to_index = []
    level = 0
    for d in pal_data:
        sprite_pal = d[1]
        sprite_name_to_index.append({})
        spr_index = 0

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
            key = pdata[2]
            sprite_name_to_index[level][key] = spr_index
            spr_index = spr_index + 1
        level = level + 1

    if True:
        for idx, level in enumerate(levels["levels"]):
            for i in range(level["bmax"]):
                num = level["badguys"][i]["num"]
                x = level["badguys"][i]["x"]
                x = (round(x / 20) - 1) * 24
                y = level["badguys"][i]["y"]
                y = convert_y(y)
                y = fix_y(idx, -1, y, level["ground"][int((x + 0) / 24)])
                num = sprite_name_to_index[idx][f"bad{num}1"]
                level["badguys"][i]["num"] = num
                level["badguys"][i]["x"] = x
                level["badguys"][i]["y"] = y

        for idx, level in enumerate(levels["levels"]):
            endp = "endp"
            lastIndex = 0
            for i in range(level["tmax"]):
                num = level["thing"][i]["num"]
                if num == 8:
                    # There is a key in the level. Set the door as a locked door
                    endp = "endp2"
                x = level["thing"][i]["x"]
                y = level["thing"][i]["y"]
                x = (round(x / 20) - 1) * 24
                y = convert_y(y)
                y = fix_y(idx, i, y, level["ground"][int((x + 0) / 24)])
                num = sprite_name_to_index[idx][f"obj{num}"]

                level["thing"][i]["x"] = x
                level["thing"][i]["y"] = y
                level["thing"][i]["num"] = num
                lastIndex = i

            # Now add end door as an object
            level["thing"].append({})
            num = sprite_name_to_index[idx][endp]
            x = level["endlev"]
            x = (round(x / 20) - 1) * 24
            # in original pascal code, door was always on ground[(endlev div 20)].y[1]-20. Pascal indices are 1-based
            y = convert_y(level["ground"][round(x / 24)]["y"][0]) - 24
            level["thing"][lastIndex + 1] = {"x": x, "y": y, "num": num}
            level["tmax"] = level["tmax"] + 1

        # Create list of blocks for each levels
        for idx, level in enumerate(levels["levels"]):
            for i in range(level["cmax"]):
                for n in range(5):
                    if level["ground"][i]["y"][n] < 181:
                        num = level["ground"][i]["num"][n]
                        y = level["ground"][i]["y"][n]
                        y = convert_y(y)
                        num = sprite_name_to_index[idx][f"cube{num}"]
                    else:
                        num = 0xFF
                        y = 0xFF
                    level["ground"][i]["y"][n] = y
                    level["ground"][i]["num"][n] = num

        for idx, level in enumerate(levels["levels"]):
            endlev = round(level["endlev"] / 20) * 24
            level["endlev"] = endlev

    if sys.argv[1] == "-s":
        with open("sprites.vasm", "w") as f:
            f.write("; Snowchuck\n")
            f.write("; Patrick Dumais\n")
            f.write("; File generated by convert.py\n")

            spr_code = gen_sprites(sprites, reduced)
            f.write(spr_code)

    if sys.argv[1] == "-m":
        with open("map.json", "w") as f:
            j = {"l": levels, "p": pal_data, "sprnames": sprite_name_to_index}
            f.write(json.dumps(j))
