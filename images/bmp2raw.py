import struct

WIDTH = 24
HEIGHT = 24
SIZE = WIDTH * HEIGHT


def read_bmp_8bit_raw(path):
    with open(path, "rb") as f:
        data = f.read()

    # --- BMP HEADER ---
    if data[0:2] != b"BM":
        raise ValueError("Not a BMP file")

    pixel_offset = struct.unpack_from("<I", data, 10)[0]

    dib_size = struct.unpack_from("<I", data, 14)[0]
    if dib_size < 40:
        raise ValueError("Unsupported BMP format")

    width = struct.unpack_from("<I", data, 18)[0]
    height = struct.unpack_from("<I", data, 22)[0]
    bpp = struct.unpack_from("<H", data, 28)[0]

    if width != WIDTH or height != HEIGHT:
        raise ValueError(f"Expected {WIDTH}x{HEIGHT}, got {width}x{height}")

    if bpp != 8:
        raise ValueError("Only 8-bit BMP supported")

    # --- PIXEL DATA ---
    row_size = WIDTH
    padding = (4 - (row_size % 4)) % 4
    stride = row_size + padding

    pixels = []

    # BMP is bottom-up
    for y in range(HEIGHT):
        row_start = pixel_offset + (HEIGHT - 1 - y) * stride
        row = data[row_start:row_start + WIDTH]
        pixels.extend(row)

    if len(pixels) != SIZE:
        raise ValueError(f"Invalid pixel data size: {len(pixels)}")

    return bytes(pixels)


def write_raw_24x24(path, raw_bytes):
    if len(raw_bytes) != SIZE:
        raise ValueError(f"Expected {SIZE} bytes, got {len(raw_bytes)}")

    with open(path, "wb") as f:
        f.write(raw_bytes)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python bmp_to_raw.py input.bmp output.bin")
        raise SystemExit(1)

    inp, outp = sys.argv[1], sys.argv[2]

    raw = read_bmp_8bit_raw(inp)
    write_raw_24x24(outp, raw)

    print(f"Converted BMP → raw Mode 13h: {outp}")
