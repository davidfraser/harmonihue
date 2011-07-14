all: out/book.html out/scale-diagrams.html out/torus-tone-geometry.html out/color-theory.html out/musical-maths.html out/color-mapping.html

clean:
	rm -fr out
	rm -fr tmp

out/:
	mkdir out

tmp/:
	mkdir tmp

out/%.html: tmp/%.html out/
	lilypond-book --output out/ $<

.PRECIOUS: tmp/%.html

tmp/%.html: %.genshi.html book_helpers.py tmp/
	./genshify $< > $@

