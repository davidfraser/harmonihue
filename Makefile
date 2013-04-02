.PHONY: all clean

output_genshi=$(foreach filename,$(wildcard *.genshi.html),out/$(filename:.genshi.html=.html))
output_lilypond_genshi=$(foreach filename,$(wildcard *.lilypond-genshi.html),out/$(filename:.lilypond-genshi.html=.html))
output_svg=$(foreach filename,$(wildcard *.genshi.svg),out/$(filename:.genshi.svg=.svg))
output_png=$(foreach filename,$(wildcard *.genshi.svg),out/$(filename:.genshi.svg=.png))

all: chromaturn.ly $(output_genshi) $(output_lilypond_genshi) $(output_svg) $(output_png)

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
	./genshify $< > $@

out/guitar-fretboard.svg: guitar_layout.py sticker-def.genshi.xml guitar-base.genshi.xml guitar-strings.genshi.xml

out/%.svg: %.genshi.svg book_helpers.py $(OUT)
	./genshify $< > $@

out/%.png: out/%.svg
	rasterizer -d $@ -m image/png $<
	# convert $< $@

out/%.html: %.genshi.html book_helpers.py $(OUT)
	./genshify $< > $@

out/%.txt: %.genshi.txt book_helpers.py $(OUT)
	./genshify $< > $@

out/%.html: tmp/%.html $(OUT) $(TMP)
	lilypond-book --output out/ $<

tmp/%.html: %.lilypond-genshi.html book_helpers.py chromaturn.ly $(TMP)
	./genshify $< > $@

