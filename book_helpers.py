#!/usr/bin/env python

"""A set of functions that are called from within book.genshi.html"""

import math
import os
import matplotlib
from matplotlib import pyplot
import colormath.color_objects
import subprocess
import genshi
from figurine import *
from musicality import *
from spectrum import *
from torus import *


if __name__ == "__main__":
    import sys
    L = locals()
    for arg in sys.argv[1:]:
        if arg in L and hasattr(L[arg], "show"):
            print ("Running %s" % arg)
            L[arg].show()
        else:
            print ("Could not find %s" % arg)

