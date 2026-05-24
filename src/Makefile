
AS=../toolchain/vasm/vasmm68k_mot
ASZ80=../toolchain/vasm/vasmz80_mot
LD=../toolchain/vlink/vlink
LSCRIPT=linker.ld
ASFLAGS=-m68000 -Felf -spaces -no-opt
ASZ80FLAGS=-Fvobj -spaces
LDFLAGS=-brawbin1 -T $(LSCRIPT) 
LDZ80FLAGS=-brawbin1 -T linkerz80.ld -Mmapz80.txt
SRCS=main.vasm vdp.vasm sprites.vasm levels.vasm graphx.vasm ram.vasm soundengine.vasm sound.vasm font.vasm write.vasm
OBJS=$(SRCS:.vasm=.o)
OBJS-DEBUG=$(SRCS:.vasm=-debug.o)
OUT=snowchuck.bin
OUT-DEBUG=snowchuck-debug.bin

ALL: gen z80.bin $(OUT) $(OUT-DEBUG)

z80.bin: z80.vasm
	$(ASZ80) z80.vasm $(ASZ80FLAGS) -o z80.o
	$(LD) $(LDZ80FLAGS) -o z80.bin z80.o

.PHONY: gen
.PHONY: font.vasm

font.vasm:
	python3 ../images/fontconvert.py ../images/font.asm > font.vasm

sprites.vasm: 
	cp ../images/sprites.vasm ./

levels.vasm:
	cp ../images/levels.vasm ./

sound.vasm:
	cd ../sound && make
	cp ../sound/sound.vasm ./
sound.o: sound.vasm

soundengine.o: soundengine.vasm z80.bin

%.o: %.vasm
	$(AS) $(ASFLAGS) -o $@ $<

%-debug.o: %.vasm
	$(AS) $(ASFLAGS) -DDEBUG_MODE -o $@ $<

$(OUT): z80.bin $(OBJS) $(LSCRIPT)
	$(LD) $(LDFLAGS) -o $@ $(OBJS) -Mmap.txt

$(OUT-DEBUG): z80.bin $(OBJS-DEBUG) $(LSCRIPT)
	$(LD) $(LDFLAGS) -o $@ $(OBJS-DEBUG) -Mmap-debug.txt

clean:
	rm -f *.o sound.vasm levels.vasm sprites.vasm *.bin

start_xpra:
	xpra start :100 --bind-tcp=0.0.0.0:3000 --html=on --daemon=false --speaker=on

run_on_xpra: $(OUT)
	DISPLAY=:100 blastem $(OUT)

run: $(OUT)
	blastem $(OUT)

disz80:
	z80dasm -g0 z80.bin -l -a
