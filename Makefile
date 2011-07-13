all: out/book.html

book.genshi.html: book_helpers.py

out/:
	mkdir out

out/%.html: %.html out/
	lilypond-book --output out/ $<

%.html: %.genshi.html
	./genshify $< > $@

