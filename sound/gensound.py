import sys
from pathlib import Path

OUTPUT = Path("sound.vasm")


def get_label_name(asm_path):
    return asm_path.stem


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 script.py file1.vasm file2.vasm ...")
        sys.exit(1)

    asm_files = [Path(arg) for arg in sys.argv[1:]]

    # Separate songs from sound effects
    songs = []
    others = []

    for asm in asm_files:
        name = asm.stem

        if name.startswith("song"):
            songs.append(name)
        else:
            others.append(name)

    # Sort songs numerically (song1, song2, ...)
    songs.sort(key=lambda x: int(x[4:]))

    with OUTPUT.open("w", newline="\n") as f:
        f.write("    section .sound\n")
        for song in songs:
            f.write(f"    xdef {song}_ref\n")
        for name in others:
            f.write(f"    xdef {name}_ref\n")
        f.write("\n")

        for i in range(1, 17):
            label = f"song{i}"

            if label in songs:
                f.write(f"{label}_ref: dc.l {label}_start\n")
            else:
                f.write(f"{label}_ref: dc.l 0\n")

        for name in others:
            f.write(f"{name}_ref: dc.l {name}_start\n")

        f.write("\n")

        for asm in asm_files:
            if not asm.exists():
                print(f"Warning: {asm} not found")
                continue

            print(f"Appending {asm}")
            f.write(f"; ----- {asm.name} -----\n")
            f.write(asm.read_text())
            f.write("\n")

        max_size = 4096
        for name in songs:
            f.write(f"    if (({name}_end-{name}_start) > {max_size})\n")
            f.write(f'    fail "{name} > {max_size}"\n')
            f.write(f"    endc\n")

        firstfx = others[0]
        lastfx = others[len(others)-1]
        max_size = 2048
        f.write(f"    if (({lastfx}_end-{firstfx}_start) > {max_size})\n")
        f.write(f'    fail "FX > {max_size}"\n')
        f.write(f"    endc\n")


    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
