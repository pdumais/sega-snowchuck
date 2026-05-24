
ALL: gen
VGMS=song1.vgm song2.vgm song3.vgm song4.vgm song5.vgm coin.vgm death.vgm object.vgm coffee.vgm
ASMS=$(VGMS:.vgm=.vasm)

%.vasm: %.vgm
	python3 vgmconvert.py $< > $@

gen: $(ASMS)
	python3 gensound.py $(ASMS)

clean:
	rm -f $(ASMS)
