harmonihue
==========

Book
----

The main current focus is `book.genshi.html`. This is the source template for the documentation. It comprises of a [genshi](https://genshi.edgewall.org/) template for a HTML page that is then processed by lilypond to include musical score. The Python code used to generate the diagrams and tables in the template is located in `book_helpers.py`. To compile the book run `./make-book` - the book is then produced in `out/book.html` with associated files that are required.

Dependencies
------------

Compiling the book requires:
* Python 2, and the following Python modules (the correct list is in `requirements.txt`):
  - `genshi`
  - `matplotlib` (with a backend that can produce image files)
  - `mplot_toolkits.mplot3d` (part of `matplotlib`)
  - `numpy`
  - `decorator`
  - `colormath`
* Lilypond for rendering sheet music
* Inkscape for converting SVG (vector) images to PNG (rendered)
* Make for running the process

On Ubuntu 22.04, the following should work:
```
sudo apt install python2.7 python-tk virtualenv python2-pip-whl python2-setuptools-whl
sudo apt install lilypond
sudo apt install inkscape
sudo apt install make
```

Then from the `harmonihue` directory:
```
virtualenv --python=`which python2` venv/
. venv/bin/activate
pip install -r requirements.txt
make
```

