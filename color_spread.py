#!/usr/bin/env python

import colormath.color_objects
import numpy
from figurine import *
from spectrum import *
from torus import *

@figure_function
def draw_hue_circle(count=12, hues_function=None, radius=1):
    """A diagram of a circle with hue mapped on it"""
    fig = hue_circle_figure(count)
    hues = default_spread_colors() if hues_function is None else hues_function()
    ax = fig.axes[0]
    gamma = numpy.arange(-numpy.pi/count, 2*numpy.pi - numpy.pi/count, 2*numpy.pi/count)
    radii = [radius for i in range(count)]
    width = 2*numpy.pi/count
    bars = ax.bar(gamma, radii, width=width, bottom=0.0)
    for hue, bar in zip(hues, bars):
        bar.set_facecolor(rgb_float_tuple(hue))
    return fig

@figure_function
def draw_lab_hues(count=12, R=10.0, r=5.0, figsize=(5,5), hues_function=None):
    """Draws the spread hue values in the Lab color space"""
    fig = pyplot.figure(1, figsize=figsize)
    ax = mplot3d.Axes3D(fig)
    points = count * 10
    colors = get_hue_spread(points)
    lab_colors = numpy.array([color.convert_to('lab').get_value_tuple() for color in colors])
    rgb_colors = [rgb_float_tuple(color) for color in colors]
    L, a, b = lab_colors.transpose()
    ax.scatter(L, a, b, s=20, color=rgb_colors)
    new_colors = hues_function(count) if hues_function else default_spread_colors(count)
    lab_colors = numpy.array([color.convert_to('lab').get_value_tuple() for color in new_colors])
    rgb_colors = [rgb_float_tuple(color) for color in new_colors]
    L, a, b = lab_colors.transpose()
    ax.scatter(L, a, b, s=200, color=rgb_colors)
    return fig

if __name__ == '__main__':
    cmdline_show_figure(available_figure_functions(locals()))

