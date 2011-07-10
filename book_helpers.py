#!/usr/bin/env python

"""A set of functions that are called from within book.genshi.html"""

import math
import os
import matplotlib
from matplotlib import pyplot
from mpl_toolkits import mplot3d
import numpy
import decorator

OUTPUT_DIR = "out"

tones = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab"]

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

@figure_function
def draw_even_temper():
    """draws a diagram of the different rational frequences and how they related to the even-tempered twelve-tone scale"""
    fig = pyplot.figure(1, figsize=(10,4))
    ax = fig.add_axes([0.25, 0.15, 0.65, 0.75])
    ax.semilogx(basex=2)
    bases = [2, 3, 5, 7, 11]
    for i, base in enumerate(bases):
        for j in [0, 1] if (base == 2) else range(-6,7):
            f = float(base) ** j
            p = 1
            while f < 1:
                f *= 2
                p -= 1
            while f > 2:
                f /= 2
                p += 1
            alpha = 1.0/(abs(j) + abs(p))
            ax.scatter([f], [i+1], alpha=alpha)
            ax.text(f, i+1, str(j), alpha=math.sqrt(alpha))
    y_tick_info = {2: "octaves", 3: "fifths", 5: "major thirds"}
    ax.set_yticks(range(len(bases)+1))
    ax.set_yticklabels(["(even-temper) $2^\\frac{1}{12}$"] + ["%s $\\frac{1}{%d}$" % (y_tick_info.get(base, ""), base) for base in bases])
    ax.set_ylabel("base harmonic ratio")
    even_temper = [2 ** (float(i)/12) for i in range(13)]
    ax.scatter(even_temper, [0]*13)
    ax.set_xticks(even_temper)
    ax.set_xticklabels([str(i) for i in range(14)])
    ax.set_xlim((1, 2))
    ax.set_xlabel("frequency ($log 2$)")
    ax.xaxis.grid(True)
    return fig

def interval_circle_figure(base_interval):
    """sets up a matplotlib figure with a polar plot based on the circle of tones generated by the given interval. Returns (cycle, fig)"""
    fig = pyplot.figure(1, figsize=(2,2))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
    cycle = list(tone_cycle(base_interval))
    cycle.reverse()
    s = 2*math.pi/12
    ax.set_xticks([s*i for i in range(12)])
    ax.set_xticklabels([tones[i] for i in cycle])
    ax.set_yticks([])
    ax.set_rmax(1)
    ax.set_frame_on(False)
    pyplot.grid(False)
    pyplot.axis('tight')
    return cycle, fig

@figure_function
def draw_tone_circle(interval):
    """A diagram of the circle of fifths/semitones with nothing drawn on it"""
    return interval_circle_figure(interval)[1]

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

@figure_function
def draw_tone_cycles(interval, base_interval=7):
    base_cycle, fig = interval_circle_figure(base_interval)
    ax = fig.axes[0]
    s = 2*math.pi/12
    for offset in range(0, (interval if (12 % interval == 0) else 1)):
        tone_indexes = list(tone_cycle(interval, offset))
        cycle = [base_cycle.index(i) for i in tone_indexes]
        cycle.reverse()
        l = len(cycle)
        cycle.append(cycle[0])
        theta = [s*i for i in cycle]
        r = [1 for i in cycle]
        ax.plot(theta, r)
    return fig

def torus_figure(ax, R=10.0, r=3.0, alpha=0.3, color='b'):
    """Returns a polyc for a torus plot on the given (3d) axes"""
    u = numpy.linspace(0, 2*numpy.pi, 180)
    v = numpy.linspace(0, 2*numpy.pi, 180)
    x = numpy.outer(R + r*numpy.cos(v), numpy.cos(u))
    y = numpy.outer(R + r*numpy.cos(v), numpy.sin(u))
    z = numpy.outer(r*numpy.sin(v), numpy.ones(numpy.size(u)))
    polyc = ax.plot_surface(x, y, z,  rstride=9, cstride=9, color=color, alpha=alpha)
    polyc.set_linewidth(0)
    polyc.set_edgecolor(color)
    return polyc

def tone_spiral(ax, R, r, color='yellow'):
    """Draws a tone spiral around a torus of given radii"""
    u = numpy.linspace(0, 2*numpy.pi, 180)
    v = numpy.linspace(0, 3*2*numpy.pi, 180)
    x = (R + r*numpy.cos(v))*numpy.cos(u)
    y = (R + r*numpy.cos(v))*numpy.sin(u)
    z = r*numpy.sin(v)
    return ax.plot(x, y, z, color='yellow')

def tone_points(ax, R, r, color='orange'):
    """Draws tone points and labels them around a torus of given radii"""
    u = numpy.linspace(0, 2*numpy.pi, 12)
    v = numpy.linspace(0, 3*2*numpy.pi, 12)
    x = (R + r*numpy.cos(v))*numpy.cos(u)
    y = (R + r*numpy.cos(v))*numpy.sin(u)
    z = r*numpy.sin(v)
    cycle = list(tone_cycle(7))
    cycle.reverse()
    for n, i in enumerate(cycle):
        ax.text(x[n], y[n], z[n], tones[i])
    return ax.scatter(x, y, z, color='orange')

@figure_function
def draw_torus(R=10.0, r=5.0):
    """Draws a torus"""
    fig = pyplot.figure(1, figsize=(10,10))
    ax = mplot3d.Axes3D(fig)
    torus = torus_figure(ax, R, r, color='red')
    spiral = tone_spiral(ax, R, r, color='yellow')
    points = tone_points(ax, R, r, color='orange')
    ax.set_xlim3d((-R-r, R+r))
    ax.set_ylim3d((-R-r, R+r))
    ax.set_zlim3d((-R-r, R+r))
    ax.view_init(40, 40)
    return fig

if __name__ == "__main__":
    import sys
    L = locals()
    for arg in sys.argv[1:]:
        if arg in L and hasattr(L[arg], "show"):
            print ("Running %s" % arg)
            L[arg].show()
        else:
            print ("Could not find %s" % arg)

