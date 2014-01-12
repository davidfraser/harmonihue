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

def rgb_hex(c):
    """converts a colormath color object to an rgb hex string for html like #30bf30"""
    return c.convert_to('rgb').get_rgb_hex()

def lighter_color(c, level):
    """lightens the color by increasing the HSL lightness value by the given amount"""
    c2 = c.convert_to('hsl')
    c2.hsl_l = min(1, c2.hsl_l + level)
    return c2


if __name__ == "__main__":
    import sys
    L = locals()
    for arg in sys.argv[1:]:
        if arg in L and hasattr(L[arg], "show"):
            print ("Running %s" % arg)
            L[arg].show()
        else:
            print ("Could not find %s" % arg)

