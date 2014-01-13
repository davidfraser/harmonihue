#!/usr/bin/env python

import colormath.color_objects
import numpy
from figurine import *
from spectrum import *
from torus import *

def get_hsv_circle_hues(count=12, saturation=0.75, value=0.75):
    """returns a hsv color range corresponding roughly to the torus, as rgb"""
    M_s, M_h = 0.1875, 0.1875
    hsv_map = {0: (saturation+M_s, value+M_h), 1: (saturation+M_s, value-M_h), 2: (saturation-M_s, value-M_h), 3: (saturation-M_s, value+M_h)}
    return [rgb_float_tuple(colormath.color_objects.HSVColor(360*float(count*2 - i)/count, hsv_map[i%4][0], hsv_map[i%4][1])) for i in range(count)]

def get_spread_hues(count=12, saturation=DEFAULT_SATURATION, value=DEFAULT_VALUE):
    """returns an evenly spread number of hues, with the given saturation and value, as rgb"""
    return [rgb_float_tuple(colormath.color_objects.HSVColor(360*float(count*2 - i)/count, saturation, value)) for i in range(count)]

@figure_function
def draw_hue_tone_circle(interval=7, hues_function=None, radius=1):
    """A diagram of the circle of fifths/semitones with hue mapped on it"""
    cycle, fig = interval_circle_figure(interval)
    hue_cycle = list(tone_cycle(7))
    hues = get_delta_spread_hues() if hues_function is None else hues_function()
    ax = fig.axes[0]
    gamma = numpy.arange(-numpy.pi/12, 2*numpy.pi - numpy.pi/12, 2*numpy.pi/12)
    radii = [radius for i in range(12)]
    width = 2*numpy.pi/12
    bars = ax.bar(gamma, radii, width=width, bottom=0.0)
    for i, bar in zip(cycle, bars):
        bar.set_facecolor(hues[hue_cycle.index(i)])
    return fig

@figure_function
def draw_hue_torus_tone_circle(R=10.0, r=5.0, hues_function=None):
    """draws the hues of the color map onto the torus"""
    fig = draw_torus(R, r, figsize=(5,5))
    fig.points.remove()
    x, y, z = torus_tone_coords(R, r)
    ax = fig.axes[0]
    hue_cycle = list(tone_cycle(7))
    hues = get_delta_spread_hues() if hues_function is None else hues_function()
    for interval, hue in enumerate(hues):
        ax.scatter([x[interval]], [y[interval]], [z[interval]], s=100, color=hue)
    set_torus_view(ax, R, r)
    return fig

@figure_function
def draw_hue_rotation_tone_circle(interval=7, hues_function=None):
    """A diagram of the circle of fifths/semitones with hue mapped on it and rotation displayed with a superimposed line"""
    fig = draw_hue_tone_circle(interval, hues_function=hues_function, radius=0.75)
    cycle = list(tone_cycle(interval))
    hue_cycle = list(tone_cycle(7))
    hues = get_delta_spread_hues() if hues_function is None else hues_function()
    ax = fig.axes[0]
    scatter_gamma = numpy.arange(0, 2*numpy.pi, 2*numpy.pi/12)
    for i in range(12):
        hue_i = hue_cycle.index(cycle[i])
        ax.scatter(scatter_gamma[i], 0.875, color=hues[hue_i], s=100, marker=(2, 0, (hue_i%4)*45), linewidths=(4))
    return fig

@figure_function
def draw_lab_hues(R=10.0, r=5.0, figsize=(5,5)):
    """Draws the spread hue values in the Lab color space"""
    fig = pyplot.figure(1, figsize=figsize)
    ax = mplot3d.Axes3D(fig)
    count = 12
    points = count * 10
    colors = get_hue_spread(points)
    lab_colors = numpy.array([color.convert_to('lab').get_value_tuple() for color in colors])
    rgb_colors = [rgb_float_tuple(color) for color in colors]
    L, a, b = lab_colors.transpose()
    ax.scatter(L, a, b, s=20, color=rgb_colors)
    new_colors = get_lab_spread_colors(count)
    lab_colors = numpy.array([color.convert_to('lab').get_value_tuple() for color in new_colors])
    rgb_colors = [rgb_float_tuple(color) for color in new_colors]
    L, a, b = lab_colors.transpose()
    ax.scatter(L, a, b, s=200, color=rgb_colors)
    return fig

@figure_function
def draw_lab_delta_hues(R=10.0, r=5.0, figsize=(5,5)):
    """Draws the delta-spread hue values in the Lab color space"""
    fig = pyplot.figure(1, figsize=figsize)
    ax = mplot3d.Axes3D(fig)
    count = 12
    points = count * 10
    colors = get_hue_spread(points)
    lab_colors = numpy.array([color.convert_to('lab').get_value_tuple() for color in colors])
    rgb_colors = [rgb_float_tuple(color) for color in colors]
    L, a, b = lab_colors.transpose()
    ax.scatter(L, a, b, s=20, color=rgb_colors)
    new_colors = get_delta_spread_colors(count)
    lab_colors = numpy.array([color.convert_to('lab').get_value_tuple() for color in new_colors])
    rgb_colors = [rgb_float_tuple(color) for color in new_colors]
    L, a, b = lab_colors.transpose()
    ax.scatter(L, a, b, s=200, color=rgb_colors)
    return fig

if __name__ == '__main__':
    cmdline_show_figure(available_figure_functions(locals()))

