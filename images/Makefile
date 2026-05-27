ALL: genasm genbmp
SPRS=bad11.spr24 bad24.spr24 bad43.spr24 cent3.spr24 cube15.spr24 cube21.spr24 cube2.spr24 cube4.spr24 dead2.spr24 hero3.spr24 obj6.spr24 bad12.spr24 bad31.spr24 bad44.spr24 cent4.spr24 cube16.spr24 cube22.spr24 cube36.spr24 cube5.spr24 dead3.spr24 hero4.spr24 obj7.spr24 bad13.spr24 bad32.spr24 bad51.spr24 cube10.spr24 cube17.spr24 cube23.spr24 cube37.spr24 cube6.spr24 dead4.spr24 obj1.spr24 obj8.spr24 bad14.spr24 bad33.spr24 bad52.spr24 cube11.spr24 cube18.spr24 cube24.spr24 cube38.spr24 cube7.spr24 endp2.spr24 obj2.spr24 obj9.spr24 bad21.spr24 bad34.spr24 bad53.spr24 cube12.spr24 cube19.spr24 cube25.spr24 cube39.spr24 cube8.spr24 endp.spr24 obj3.spr24 water1.spr24 bad22.spr24 bad41.spr24 bad54.spr24 cube13.spr24 cube1.spr24 cube26.spr24 cube3.spr24 cube9.spr24 hero1.spr24 obj4.spr24 water2.spr24 bad23.spr24 bad42.spr24 cent2.spr24 cube14.spr24 cube20.spr24 cube27.spr24 cube40.spr24 dead1.spr24 hero2.spr24 obj5.spr24 water3.spr24
BMPS=$(SPRS:.spr24=.bmp)
MAP=map.json

# Generating map.json should be done only once. We can then generate the vasm file from json using convertp2.py
# map.json may have been edited by the map editor. map.json was generated from the original chuck file
map.json: 
	python3 convertp1.py -m

.PHONY: sprites.vasm
sprites.vasm: 
	python3 convertp1.py -s

.PHONY: levels.vasm
levels.vasm: map.json
	python3 convertp2.py $(MAP)

genasm: levels.vasm sprites.vasm

%.bmp: %.spr24
	python3 raw2bmp.py $< $@

genbmp: $(BMPS)

edit: MAP=edited-map.json
edit: levels.vasm sprites.vasm
