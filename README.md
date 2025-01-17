harmonihue
==========

License
-------

All source code in this repository is available under the [GPL v3](./LICENSE) license, unless otherwise specified.

Book
----

The main current focus is `book.genshi.html`. This is the source template for the documentation. It comprises of a [genshi](https://genshi.edgewall.org/) template for a HTML page that is then processed by lilypond to include musical score. The Python code used to generate the diagrams and tables in the template is located in `book_helpers.py`. To compile the book run `./make-book` - the book is then produced in `docs/book.html` with associated files that are required.

Dependencies
------------

Compiling the book requires:
* Python 3.x, and the following Python modules (the correct list is in `requirements.txt`):
  - `genshi`
  - `matplotlib` (with a backend that can produce image files)
  - `mplot_toolkits.mplot3d` (part of `matplotlib`)
  - `numpy`
  - `decorator`
  - `colormath`
  - `grapefruit` (needs a fork of the main project to support Python 3)
* Lilypond 2.22.x for rendering sheet music (2.24.x has an issue currently)
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

If installing Lilypond manually, don't include the built-in python.
This doesn't help as it seems to install it anyway :(
So if you install for example to `%USERPROFILE\AppData\Local\Programs\Lilypond\LilyPondNN\usr\bin`,
then run `rename python.exe lilypond-python.exe` in that directory.

On Windows 11, the following might work (assuming you have [chocolatey](https://chocolatey.org/) set up):
```bat
choco install -y python
choco install -y lilypond==2.22.2
choco install -y inkscape
choco install -y make
choco install -y rsync
```

Then from the `harmonihue` directory:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

To actually build the contents, run:
```
make
```
