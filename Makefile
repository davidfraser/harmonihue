all: chromaturn.ly $(foreach filename,$(wildcard *.genshi.html),out/$(filename:.genshi.html=.html)) $(foreach filename,$(wildcard *.lilypond-genshi.html),out/$(filename:.lilypond-genshi.html=.html))

clean:
	rm -fr out
	rm -fr tmp
	rm chromaturn.ly

out/:
	mkdir out

tmp/:
	mkdir tmp

.PRECIOUS: tmp/%.html

%.ly: %.genshi.ly
	./genshify $< > $@

out/%.html: %.genshi.html book_helpers.py out/
	./genshify $< > $@

out/%.html: tmp/%.html out/ tmp/
	lilypond-book --output out/ $<

tmp/%.html: %.lilypond-genshi.html book_helpers.py tmp/
	./genshify $< > $@

