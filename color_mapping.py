#!/usr/bin/env python

import colormath.color_objects
import numpy
from figurine import *
from musicality import *
from spectrum import *
from torus import *

@figure_function
def draw_hue_tone_circle(interval=7, hues_function=None, radius=1):
    """A diagram of the circle of fifths/semitones with hue mapped on it"""
    cycle, fig = interval_circle_figure(interval)
    hue_cycle = list(tone_cycle(7))
    hues = default_spread_colors() if hues_function is None else hues_function()
    ax = fig.axes[0]
    gamma = numpy.arange(-numpy.pi/12, 2*numpy.pi - numpy.pi/12, 2*numpy.pi/12)
    radii = [radius for i in range(12)]
    width = 2*numpy.pi/12
    bars = ax.bar(gamma, radii, width=width, bottom=0.0)
    for i, bar in zip(cycle, bars):
        bar.set_facecolor(rgb_float_tuple(hues[hue_cycle.index(i)]))
    return fig

@figure_function
def draw_hue_torus_tone_circle(R=10.0, r=5.0, hues_function=None):
    """draws the hues of the color map onto the torus"""
    fig = draw_torus(R, r, figsize=(5,5))
    fig.points.remove()
    x, y, z = torus_tone_coords(R, r)
    ax = fig.axes[0]
    hue_cycle = list(tone_cycle(7))
    hues = default_spread_colors() if hues_function is None else hues_function()
    for interval, hue in enumerate(hues):
        ax.scatter([x[interval]], [y[interval]], [z[interval]], s=100, color=rgb_float_tuple(hue))
    set_torus_view(ax, R, r)
    return fig

@figure_function
def draw_hue_rotation_tone_circle(interval=7, hues_function=None):
    """A diagram of the circle of fifths/semitones with hue mapped on it and rotation displayed with a superimposed line"""
    fig = draw_hue_tone_circle(interval, hues_function=hues_function, radius=0.75)
    cycle = list(tone_cycle(interval))
    hue_cycle = list(tone_cycle(7))
    hues = default_spread_colors() if hues_function is None else hues_function()
    ax = fig.axes[0]
    scatter_gamma = numpy.arange(0, 2*numpy.pi, 2*numpy.pi/12)
    for i in range(12):
        tone = cycle[i]
        hue_i = hue_cycle.index(tone)
        r = get_rotation(tone)
        ax.scatter(scatter_gamma[i], 0.875, color=rgb_float_tuple(hues[hue_i]), s=100, marker=(2, 0, -r), linewidths=(4))
    return fig

if __name__ == '__main__':
    cmdline_show_figure(available_figure_functions(locals()))

