.PHONY: all out_dir tmp_dir clean

all: chromaturn.ly $(foreach filename,$(wildcard *.genshi.html),out/$(filename:.genshi.html=.html)) $(foreach filename,$(wildcard *.lilypond-genshi.html),out/$(filename:.lilypond-genshi.html=.html))

clean:
	rm -fr out
	rm -fr tmp
	rm chromaturn.ly

out_dir:
	mkdir -p out

tmp_dir:
	mkdir -p tmp

.PRECIOUS: tmp/%.html

%.ly: %.genshi.ly
	./genshify $< > $@

out/%.svg: %.genshi.svg book_helpers.py out_dir
	./genshify $< > $@

out/%.html: %.genshi.html book_helpers.py out_dir
	./genshify $< > $@

out/%.html: tmp/%.html out_dir tmp_dir
	lilypond-book --output out/ $<

tmp/%.html: %.lilypond-genshi.html book_helpers.py chromaturn.ly tmp_dir
	./genshify $< > $@

