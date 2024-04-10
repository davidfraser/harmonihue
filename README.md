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
* Lilypond 2.20.x for rendering sheet music
* Inkscape for converting SVG (vector) images to PNG (rendered)
* Make for running the process

The makefile assumes that you have the right version of Lilypond in the current path,
and the appropriate Python environment with the required scripts activated.

Installing on a modern Linux distro
-----------------------------------

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
```

To actually build the contents, run:
```
make
```

Installing on a modern Windows
------------------------------

If installing Lilypond manually, don't include the built-in python - it's really old.
This doesn't help as it seems to install it anyway :(
So if you install for example to `%USERPROFILE\AppData\Local\Programs\Lilypond\LilyPondNN\usr\bin`,
then run `del python*.exe` in that directory.

On Windows 11, the following might work (assuming you have [chocolatey](https://chocolatey.org/) set up):
```bat
choco install -y python2
python2 -m ensurepip
python2 -m pip install --upgrade pip setuptools virtualenv
python2 -m virtualenv venv
choco install -y lilypond==2.20.0
choco install -y inkscape
choco install -y make
choco install -y rsync
```

Then from the `harmonihue` directory:
```
rem virtualenv doesn't seem to copy required tcl and tk to the expected places
rem xcopy /e %USERPROFILE%\AppData\Local\Programs\Python\Python27\tcl\tcl8.5\ venv\Lib\tcl8.5\
rem xcopy /e %USERPROFILE%\AppData\Local\Programs\Python\Python27\tcl\tk8.5\ venv\Lib\tk8.5\
venv\Scripts\activate
pip install -r requirements.txt
```

To actually build the contents, run:
```
make
```
