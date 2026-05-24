# Snowchuck
# Patrick Dumais
# This script is Mostly AI generated
#

import re
import sys

ON_NIBBLE = 0x3
OFF_NIBBLE = 0x0


def unpack_byte(value):
    """Expand one byte into 8 individual bits (MSB first)."""
    return [(value >> (7 - bit)) & 1 for bit in range(8)]


def pack_bits_to_nibbles(bits):
    """
    Convert 64 bits into 32 bytes.
    Each bit becomes a 4-bit nibble:
        0 -> 0x0
        1 -> 0xF
    Two nibbles packed per byte.
    """
    packed = []

    for i in range(0, len(bits), 2):
        hi = ON_NIBBLE if bits[i] else OFF_NIBBLE
        lo = ON_NIBBLE if bits[i + 1] else OFF_NIBBLE
        packed.append((hi << 4) | lo)

    return packed


def parse_font_file(input_path):
    """Read DC.B lines and convert each glyph."""
    glyphs = []

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line.startswith("DC.B"):
                continue

            match = re.search(r"DC\.B\s+(.+?)\s*;", line)
            if not match:
                continue

            values = [int(x.strip()) for x in match.group(1).split(",")]

            if len(values) != 8:
                raise ValueError(f"Expected 8 values, got {len(values)}:\n{line}")

            # Step 1: unpack 8 bytes -> 64 bits
            bits = []
            for byte in values:
                bits.extend(unpack_byte(byte))

            # Step 2: repack into 32 bytes of 4bpp
            packed = pack_bits_to_nibbles(bits)

            glyphs.append(packed)

    return glyphs


def write_output(glyphs):
    """Write assembly to stdout."""
    print("; Auto-generated 4bpp font data")
    print()
    print("    section .rodata")
    print("    xdef font_chars")
    print("font_chars:")

    for i, glyph in enumerate(glyphs):
        print(f"glyph_{i:03d}:")

        # 16 bytes per line (2 lines per glyph)
        for row in range(0, 32, 16):
            chunk = glyph[row : row + 16]
            values = ",".join(f"${b:02X}" for b in chunk)
            print(f"    DC.B {values}")

        print()


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("    python unpack_font.py input.asm")
        sys.exit(1)

    input_path = sys.argv[1]

    glyphs = parse_font_file(input_path)
    glyphs.append([0xFF for i in range(32)])  # full square
    write_output(glyphs)


if __name__ == "__main__":
    main()
