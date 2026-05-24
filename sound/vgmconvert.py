import struct
import sys

VGM_EOF = 0x66
VGM_WAIT = 0x61
VGM_WAIT_735 = 0x62
VGM_WAIT_882 = 0x63
VGM_YM2612_0 = 0x52
VGM_YM2612_1 = 0x53
VGM_PSG = 0x50
VGM_DATA_BLOCK = 0x67


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def u8(b, o):
    return b[o]


def parse_vgm(path):
    with open(path, "rb") as f:
        data = f.read()

    if data[0:4] != b"Vgm ":
        raise ValueError("Not a valid VGM file")

    eof_offset = u32(data, 0x04)
    version = u32(data, 0x08)

    gd3_offset = u32(data, 0x14)
    total_samples = u32(data, 0x18)
    loop_offset = u32(data, 0x1C)

    data_offset = u32(data, 0x34)
    if data_offset == 0:
        data_offset = 0x40
    else:
        data_offset += 0x34

    i = data_offset
    wait_time = 0

    last_wait = 0
    while i < len(data):
        cmd = data[i]

        if cmd != VGM_WAIT_735 and last_wait != 0:
            print(f"    dc.b $2, ${last_wait:02X}, $0, $0")
            last_wait = 0

        # End of stream
        if cmd == VGM_EOF:
            # print("END OF STREAM")
            break

        # PSG write
        elif cmd == VGM_PSG:
            val = data[i + 1]
            val2 = 0xFF
            if i + 2 < len(data):
                if data[i + 2] == VGM_PSG and data[i + 3] & 0x80 == 0:
                    val2 = data[i + 3]
                    i += 2

            # Skip anything about noise channel, it interferes with jetpack sound
            if (val & 0xE0) != 0xE0:
                print(f"    dc.b $3, ${val:02X}, ${val2:02X}, $0")
            i += 2

        # YM2612 port 0
        elif cmd == VGM_YM2612_0:
            reg = data[i + 1]
            val = data[i + 2]
            # print(f"[YM2612 P0] reg 0x{reg:02X} = 0x{val:02X}")
            print(f"    dc.b $0, ${reg:02X}, ${val:02X}, $0")
            i += 3

        # YM2612 port 1
        elif cmd == VGM_YM2612_1:
            reg = data[i + 1]
            val = data[i + 2]
            # print(f"[YM2612 P1] reg 0x{reg:02X} = 0x{val:02X}")
            print(f"    dc.b $1, ${reg:02X}, ${val:02X}, $0")
            i += 3

        # Wait n samples (16-bit)
        elif cmd == VGM_WAIT:
            wait = data[i + 1] | (data[i + 2] << 8)
            print(f"[WAIT] {wait} samples")
            # print(f"    dc.b $2, ${(data[i + 2]):02X}, ${(data[i + 1]):02X}, $00")
            i += 3

        # Wait 735 samples (~1/60 sec)
        elif cmd == VGM_WAIT_735:
            last_wait = last_wait + 1
            # print("[WAIT735] 735 samples (~1 frame)")
            i += 1

        # Wait 882 samples (~1/50 sec)
        elif cmd == VGM_WAIT_882:
            print("[WAIT882] 882 samples (~PAL frame)")
            i += 1

        # Data block (skip)
        elif cmd == VGM_DATA_BLOCK:
            data_type = data[i + 1]
            size = u32(data, i + 2)
            # print(f"[DATA BLOCK] type={data_type:02X} size={size}")
            i += 6 + size

        else:
            # Unknown command
            # print(f"[UNKNOWN CMD] 0x{cmd:02X} at {i:X}")
            i += 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python vgm_dump.py file.vgm")
        sys.exit(1)

    name = sys.argv[1].split(".")[0]
    print(f"    xdef {name}_start")
    print(f"    xdef {name}_end")
    print(f"    xdef {name}_size")
    print(f"{name}_start:")
    parse_vgm(sys.argv[1])
    print(f"    dc.b $FF, $0, $0, $0")
    print(f"{name}_end:")
    print(f"{name}_size: dc.w ({name}_end-{name}_start)")
