all: chromaturn.ly $(foreach filename,$(wildcard *.genshi.html),out/$(filename:.genshi.html=.html)) $(foreach filename,$(wildcard *.lilypond-genshi.html),out/$(filename:.lilypond-genshi.html=.html))

clean:
	rm -fr out
	rm -fr tmp

out/:
	mkdir out

tmp/:
	mkdir tmp

.PRECIOUS: tmp/%.html

%.ly: %.genshi.ly
	./genshify $< > $@

out/%.html: %.genshi.html book_helpers.py tmp/
	./genshify $< > $@

out/%.html: tmp/%.html out/
	lilypond-book --output out/ $<

tmp/%.html: %.lilypond-genshi.html book_helpers.py tmp/
	./genshify $< > $@

