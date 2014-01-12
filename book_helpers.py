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

def hue_tone_rotation_table(interval=1, hues_function=None):
    hues = get_delta_spread_hues() if hues_function is None else hues_function()
    cycle = list(tone_cycle(interval))
    hue_cycle = list(tone_cycle(7))
    for i in range(12):
        hue_i = hue_cycle.index(cycle[i])
        r, g, b = (int(l*255) for l in hues[hue_i])
        rot = (hue_i % 4)
        yield tones[i], (r, g, b), rot


if __name__ == "__main__":
    import sys
    L = locals()
    for arg in sys.argv[1:]:
        if arg in L and hasattr(L[arg], "show"):
            print ("Running %s" % arg)
            L[arg].show()
        else:
            print ("Could not find %s" % arg)

