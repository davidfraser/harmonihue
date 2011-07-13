all: out/book.html out/scale-diagrams.html out/torus-tone-geometry.html

book.genshi.html: book_helpers.py
scale-diagrams.genshi.html: book_helpers.py
torus-tone-geometry.genshi.html: book_helpers.py

out/:
	mkdir out

tmp/:
	mkdir tmp

out/%.html: tmp/%.html out/
	lilypond-book --output out/ $<

.PRECIOUS: tmp/%.html

tmp/%.html: %.genshi.html tmp/
	./genshify $< > $@

