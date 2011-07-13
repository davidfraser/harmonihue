all: out/book.html out/scale-diagrams.html out/torus-tone-geometry.html

out/:
	mkdir out

tmp/:
	mkdir tmp

out/%.html: tmp/%.html out/
	lilypond-book --output out/ $<

.PRECIOUS: tmp/%.html

tmp/%.html: %.genshi.html book_helpers.py tmp/
	./genshify $< > $@

