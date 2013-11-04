.PHONY: all clean build_all upload local

export PATH := /home/davidf/frasergo-upstream/lilypond/bin/:$(PATH)

output_genshi=$(foreach filename,$(wildcard *.genshi.html),out/$(filename:.genshi.html=.html))
output_lilypond_genshi=$(foreach filename,$(wildcard *.lilypond-genshi.html),out/$(filename:.lilypond-genshi.html=.html))
output_svg=$(foreach filename,$(wildcard *.genshi.svg),out/$(filename:.genshi.svg=.svg))
output_png=$(foreach filename,$(wildcard *.genshi.svg),out/$(filename:.genshi.svg=.png))
html_includes=header.html footer.html head_contents.html

all: build_all

build_all: chromaturn.ly $(output_genshi) $(output_lilypond_genshi) $(output_svg) $(output_png)

clean:
	rm -fr out
	rm -fr tmp
	rm chromaturn.ly

OUT=out/.d
TMP=tmp/.d

%/.d:
	mkdir -p $(@D)
	touch $@

.PRECIOUS: %/.d tmp/%.html

%.ly: %.genshi.ly
	./genshify $< -o $@

out/guitar-fretboard.svg: guitar_layout.py sticker-def.genshi.xml guitar-base.genshi.xml guitar-strings.genshi.xml

out/piano-keyboard.svg: piano_layout.py

out/%.svg: %.genshi.svg book_helpers.py $(OUT)
	./genshify $< -o $@

out/%.png: out/%.svg
	rasterizer -d $@ -m image/png $<
	# convert $< $@

out/%.html: %.genshi.html book_helpers.py $(html_includes) $(OUT)
	./genshify $< -o $@

out/%.txt: %.genshi.txt book_helpers.py $(OUT)
	./genshify $< -o $@

out/%.html: tmp/%.html $(OUT) $(TMP)
	# Remove temporary files to ensure regeneration of lilypond pictures, since lilypond-book does its own incomplete dependency check
	rm -r out/lily/
	lilypond-book --lily-output-dir out/lily/ --process "lilypond -dbackend=eps" --output out/ $<

tmp/%.html: %.lilypond-genshi.html book_helpers.py chromaturn.ly $(TMP)
	./genshify $< -o $@

local: build_all
	mkdir -p ~/frasergo-website/frasergo-mezzanine/static/projects/harmonihue/
	rsync -avzP out/ ~/frasergo-website/frasergo-mezzanine/static/projects/harmonihue/

upload: build_all
	ssh longlake.frasergo.org "mkdir -p .virtualenv/frasergo/project/static/projects/harmonihue/"
	rsync -avzP out/ longlake.frasergo.org:.virtualenv/frasergo/project/static/projects/harmonihue/

