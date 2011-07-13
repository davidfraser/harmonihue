all: out/book.html

book.genshi.html: book_helpers.py

out/:
	mkdir out

tmp/:
	mkdir tmp

out/%.html: tmp/%.html out/
	lilypond-book --output out/ $<

.PRECIOUS: tmp/%.html

tmp/%.html: %.genshi.html tmp/
	./genshify $< > $@

