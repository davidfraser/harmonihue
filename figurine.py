#!/usr/bin/env python

import decorator
import math
from matplotlib import pyplot
import os.path
import types
from config import *

tones = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab"]

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

def tone_cycle(interval, start=0):
    current = start
    finished = False
    while not finished:
        yield current
        current = (current + interval) % 12
        finished = (current == start)

def tone_cycle_pos(i, interval, start=0):
    c = list(tone_cycle(interval, start))
    return c.index(i)

def interval_circle_figure(base_interval):
    """sets up a matplotlib figure with a polar plot based on the circle of tones generated by the given interval. Returns (cycle, fig)"""
    fig = pyplot.figure(1, figsize=(2,2))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
    cycle = list(tone_cycle(base_interval))
    s = 2*math.pi/12
    ax.set_xticks([s*i for i in range(12)])
    ax.set_xticklabels([tones[i] for i in cycle])
    ax.set_yticks([])
    ax.set_rmax(1)
    ax.set_frame_on(False)
    pyplot.grid(False)
    pyplot.axis('tight')
    return cycle, fig

