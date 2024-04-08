#!/usr/bin/env python

from matplotlib import pyplot
from mpl_toolkits import mplot3d
import numpy
from figurine import *
from musicality import *

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

def torus_tone_spiral(ax, R, r, color='yellow'):
    """Draws a tone spiral around a torus of given radii"""
    u = numpy.linspace(0, 2*numpy.pi, 180)
    v = numpy.linspace(0, 3*2*numpy.pi, 180)
    x = (R + r*numpy.cos(v))*numpy.cos(u)
    y = (R + r*numpy.cos(v))*numpy.sin(u)
    z = r*numpy.sin(v)
    return ax.plot(x, y, z, color='yellow')

def torus_tone_points(ax, R, r, color='orange'):
    """Draws tone points and labels them around a torus of given radii"""
    x, y, z = torus_tone_coords(R, r)
    cycle = list(tone_cycle(7))
    cycle.reverse()
    for n, i in enumerate(cycle):
        ax.text(x[n], y[n], z[n], tones[i])
    return ax.scatter(x, y, z, color='orange')

def torus_tone_coords(R, r):
    """Returns the x, y, z vectors for 12 tone points around the torus"""
    u = numpy.linspace(0, 2*numpy.pi, 13)[:12]
    v = numpy.linspace(0, 3*2*numpy.pi, 13)[:12]
    x = (R + r*numpy.cos(v))*numpy.cos(u)
    y = (R + r*numpy.cos(v))*numpy.sin(u)
    z = r*numpy.sin(v)
    return x, y, z

@figure_function
def draw_torus(R=10.0, r=5.0, figsize=(10,10)):
    """Draws a torus"""
    fig = pyplot.figure(1, figsize=figsize)
    ax = mplot3d.Axes3D(fig)
    torus = torus_figure(ax, R, r, color='grey')
    spiral = torus_tone_spiral(ax, R, r, color='yellow')
    # stop the spiral from using the first default color
    ax._get_lines.set_prop_cycle(color=[])
    fig.points = torus_tone_points(ax, R, r, color='orange')
    set_torus_view(ax, R, r)
    return fig

def torus_scale(ax, scale_name, R, r, base_interval=7):
    """Draws straight lines between tone points to show scales on torus"""
    base_cycle = list(tone_cycle(base_interval))
    base_cycle.reverse()
    x, y, z = torus_tone_coords(R, r)
    s = 2*math.pi/12
    scale = scales[scale_name][:]
    scale.append(scale[0])
    xc = [x[base_cycle.index(i)] for i in scale]
    yc = [y[base_cycle.index(i)] for i in scale]
    zc = [z[base_cycle.index(i)] for i in scale]
    ax.plot(xc, yc, zc, color='blue')

def torus_chord(ax, chord_name, R, r, base_interval=7):
    """Draws straight lines between tone points to show chords on torus"""
    base_cycle = list(tone_cycle(base_interval))
    base_cycle.reverse()
    x, y, z = torus_tone_coords(R, r)
    s = 2*math.pi/12
    chord = chords[chord_name]
    xc = [x[base_cycle.index(i)] for i in chord]
    yc = [y[base_cycle.index(i)] for i in chord]
    zc = [z[base_cycle.index(i)] for i in chord]
    ax.plot(xc, yc, zc, color='black')

def torus_tone_cycles(ax, interval, R, r, base_interval=7):
    """Draws straight lines between tone points to show interval cycles on torus"""
    base_cycle = list(tone_cycle(base_interval))
    base_cycle.reverse()
    x, y, z = torus_tone_coords(R, r)
    s = 2*math.pi/12
    color_sequence = iter(matplotlib_colors)
    for offset in range(0, (interval if (12 % interval == 0) else 1)):
        tone_indexes = list(tone_cycle(interval, offset))
        cycle = [base_cycle.index(i) for i in tone_indexes]
        cycle.reverse()
        l = len(cycle)
        cycle.append(cycle[0])
        xc = [x[c] for c in cycle]
        yc = [y[c] for c in cycle]
        zc = [z[c] for c in cycle]
        ax.plot(xc, yc, zc, color=color_sequence.next())

def set_torus_view(ax, R, r):
    ax.set_xlim3d((-R-r, R+r))
    ax.set_ylim3d((-R-r, R+r))
    ax.set_zlim3d((-R-r, R+r))
    ax.view_init(50, 30) 

if __name__ == '__main__':
    cmdline_show_figure(available_figure_functions(locals()))

