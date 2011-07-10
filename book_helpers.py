#!/usr/bin/env python

"""A set of functions that are called from within book.genshi.html"""

import math
import os
import matplotlib
from matplotlib import pyplot
import decorator

OUTPUT_DIR = "out"

tones = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab"]

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

@decorator.decorator
def figure_saver(f, *args, **kwargs):
    filename = "_".join([f.__name__] + [repr(a) for a in args] + [repr(v) for k, v in sorted(kwargs.items())]) + ".png"
    fig = f(*args, **kwargs)
    fig.savefig(os.path.join(OUTPUT_DIR, filename))
    pyplot.close()
    return filename

@figure_saver
def draw_tone_circle(interval, start=0):
    fig = pyplot.figure(1, figsize=(2,2))
    ax = fig.add_axes([0.05, 0.05, 0.95, 0.95])
    cycle_7 = list(reversed([tones[i] for i in tone_cycle(7)]))
    pyplot.pie([1.0/12]*12, colors=[(0.7,)*3, (0.9,)*3], labels=cycle_7)
    return fig

def web_color(rgb):
    r, g, b = [int(i*255) for i in rgb]
    return "#%02x%02x%02x" % (r, g, b)

def get_matplotlib_color(i):
    """Returns the default matplotlib color for the ith line drawn in a figure in html form"""
    default_colors = ['b','g','r','c','m','y','k']
    rgb = matplotlib.colors.colorConverter.to_rgb(default_colors[i])
    return web_color(rgb)

@figure_saver
def draw_tone_cycles(interval):
    fig = pyplot.figure(1, figsize=(2,2))
    ax = fig.add_axes([0.2, 0.2, 0.7, 0.7], polar=True)
    cycle_7 = list(tone_cycle(7))
    cycle_7.reverse()
    s = 2*math.pi/12
    ax.set_xticks([s*i for i in range(12)])
    ax.set_xticklabels([tones[i] for i in cycle_7])
    ax.set_yticks([])
    ax.set_rmax(1)
    for offset in range(0, (interval if (12 % interval == 0) else 1)):
        tone_indexes = list(tone_cycle(interval, offset))
        cycle = [cycle_7.index(i) for i in tone_indexes]
        cycle.reverse()
        l = len(cycle)
        cycle.append(cycle[0])
        theta = [s*i for i in cycle]
        r = [1 for i in cycle]
        ax.plot(theta, r)
    pyplot.grid(False)
    pyplot.axis('tight')
    return fig


