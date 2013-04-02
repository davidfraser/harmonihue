.PHONY: all clean

all: chromaturn.ly $(foreach filename,$(wildcard *.genshi.html),out/$(filename:.genshi.html=.html)) $(foreach filename,$(wildcard *.lilypond-genshi.html),out/$(filename:.lilypond-genshi.html=.html))

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

out/%.svg: %.genshi.svg book_helpers.py $(OUT)
	./genshify $< > $@

out/%.html: %.genshi.html book_helpers.py $(OUT)
	./genshify $< > $@

out/%.txt: %.genshi.txt book_helpers.py $(OUT)
	./genshify $< > $@

out/%.html: tmp/%.html $(OUT) $(TMP)
	lilypond-book --output out/ $<

tmp/%.html: %.lilypond-genshi.html book_helpers.py chromaturn.ly $(TMP)
	./genshify $< > $@

