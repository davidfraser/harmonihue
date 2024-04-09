#!/usr/bin/env python

import decorator
import math
import matplotlib
from matplotlib import pyplot
import os.path
import types
from config import *
from musicality import *

def mod_delta(a, b, m):
    """simple function for calculating the delta of two numbers in a modulo space"""
    d = (a - b)
    while d < 0:
        d += m
    while d > m:
        d -= m
    if d > m/2:
        d = m - d
    return d

def web_color(rgb):
    r, g, b = [int(i*255) for i in rgb]
    return "#%02x%02x%02x" % (r, g, b)

def get_matplotlib_colors():
    """Returns the default matplotlib colors for the lines drawn in a figure in html form"""
    fig = pyplot.figure(1)
    ax = fig.add_axes([0, 0, 1, 1])
    colors_so_far = set()
    while True:
        line = ax.plot([1], [1])[0]
        color = line.get_color()
        if color in colors_so_far:
            break
        yield web_color(matplotlib.colors.colorConverter.to_rgb(color))
        colors_so_far.add(color)
    pyplot.close()

matplotlib_colors = list(get_matplotlib_colors())

def filename_part(x):
    if isinstance(x, basestring):
        return x
    if isinstance(x, (int, float, type(None))):
        return repr(x)
    if isinstance(x, (list, tuple)):
        return "_".join(filename_part(e) for e in x)
    if isinstance(x, types.FunctionType):
        return x.__name__
    return repr(x)

@decorator.decorator
def figure_saver(f, *args, **kwargs):
    filename = "_".join([f.__name__] + [filename_part(a) for a in args] + [filename_part(v) for k, v in sorted(kwargs.items())]) + ".png"
    fig = f(*args, **kwargs)
    fig.savefig(os.path.join(OUTPUT_DIR, filename))
    pyplot.close()
    return filename

@decorator.decorator
def figure_shower(f, *args, **kwargs):
    fig = f(*args, **kwargs)
    fig.show()
    pyplot.show()
    pyplot.close()

def figure_function(f):
    """decorator that adds .save and .show functions as attributes of the original function, whilst leaving it unchanged"""
    f.save = figure_saver(f)
    f.show = figure_shower(f)
    return f

def hue_circle_figure(n):
    """sets up a matplotlib figure with a polar plot based on a circle of hues. Returns (cycle, fig)"""
    fig = pyplot.figure(1, figsize=(2,2))
    ax = fig.add_axes([0.15, 0.2, 0.7, 0.6], polar=True)
    s = 2*math.pi/n
    ax.set_xticks([s*i for i in range(n)])
    ax.set_xticklabels([str(i) for i in range(n)])
    ax.set_rticks([])
    ax.set_rlim(0, 1)
    ax.set_frame_on(True)
    pyplot.grid(True)
    fig.tight_layout()
    return fig

def hue_spread_figure(n):
    """sets up a matplotlib figure with a polar plot based on a circle of hues. Returns (cycle, fig)"""
    fig = pyplot.figure(1, figsize=(4,4))
    ax = fig.add_axes([0.15, 0.2, 0.7, 0.6], polar=True)
    s = 2*math.pi/n
    ax.set_xticks([])
    ax.set_rticks([])
    ax.set_rlim(0, 1)
    ax.set_frame_on(False)
    pyplot.grid(False)
    fig.tight_layout()
    return fig

def interval_circle_figure(base_interval):
    """sets up a matplotlib figure with a polar plot based on the circle of tones generated by the given interval. Returns (cycle, fig)"""
    fig = pyplot.figure(1, figsize=(2,2))
    ax = fig.add_axes([0.15, 0.2, 0.7, 0.6], polar=True)
    cycle = list(tone_cycle(base_interval))
    s = 2*math.pi/12
    ax.set_xticks([s*i for i in range(12)])
    ax.set_xticklabels([tones[i] for i in cycle])
    ax.set_xlim(0, 2*math.pi)
    ax.set_rlim(0, 1)
    ax.set_rticks([])
    ax.set_frame_on(False)
    pyplot.grid(False)
    fig.tight_layout()
    return cycle, fig

def available_figure_functions(local_dict):
    """filters a dict of local variables to those which are functions with a show attribute (which is the value of the returned dict)"""
    return dict((name, f.show) for name, f in local_dict.items() if hasattr(f, "show"))

def cmdline_show_figure(available_functions):
    """provides a commandline interface to select a function and run it by name"""
    import sys
    for arg in sys.argv[1:]:
        if arg in available_functions:
            print ("Running %s" % arg)
            available_functions[arg]()
        else:
            print ("Could not find %s" % arg)

