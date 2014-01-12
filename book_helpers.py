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
from torus import *

DEFAULT_SATURATION = 1.0
DEFAULT_VALUE = 0.8

def rgb_float_tuple(c):
    """converts a colormath color object to an rgb tuple in the range [0, 1)"""
    r, g, b = c.convert_to('rgb').get_value_tuple()
    return (r/255., g/255., b/255.)

def rgb_hex(c):
    """converts a colormath color object to an rgb hex string for html like #30bf30"""
    return c.convert_to('rgb').get_rgb_hex()

def lighter_color(c, level):
    """lightens the color by increasing the HSL lightness value by the given amount"""
    c2 = c.convert_to('hsl')
    c2.hsl_l = min(1, c2.hsl_l + level)
    return c2

def get_spread_hues(count=12, saturation=DEFAULT_SATURATION, value=DEFAULT_VALUE):
    """returns an evenly spread number of hues, with the given saturation and value, as rgb"""
    return [rgb_float_tuple(colormath.color_objects.HSVColor(360*float(count*2 - i)/count, saturation, value)) for i in range(count)]

def get_hsv_circle_hues(count=12, saturation=0.75, value=0.75):
    """returns a hsv color range corresponding roughly to the torus, as rgb"""
    M_s, M_h = 0.1875, 0.1875
    hsv_map = {0: (saturation+M_s, value+M_h), 1: (saturation+M_s, value-M_h), 2: (saturation-M_s, value-M_h), 3: (saturation-M_s, value+M_h)}
    return [rgb_float_tuple(colormath.color_objects.HSVColor(360*float(count*2 - i)/count, hsv_map[i%4][0], hsv_map[i%4][1])) for i in range(count)]

def get_hue_spread(points, saturation=DEFAULT_SATURATION, value=DEFAULT_VALUE):
    """Returns a set of colors distributed in a circle around the Hsv space with fixed saturation and value"""
    hues = numpy.linspace(360.0, 0.0, points)
    colors = numpy.array([colormath.color_objects.HSVColor(hue, saturation, value) for hue in hues])
    return colors

def calculate_lab_delta_norm(colors, scale=(1, 0.5, 0.5)):
    """calculates the norm of the deltas between each color in Lab space"""
    points = len(colors)
    labs = numpy.array([color.convert_to('lab').get_value_tuple() for color in colors])
    lab_delta = numpy.diff(labs, axis=0) * points * scale # scale up a and b so the ranges are comparable
    lab_delta_norm = numpy.apply_along_axis(numpy.linalg.norm, 1, lab_delta)
    return lab_delta_norm

def get_lab_spread_colors(count=12, saturation=DEFAULT_SATURATION, value=DEFAULT_VALUE):
    """returns an evenly spread number of colors around the lab color space, with the given saturation and value"""
    points = count*100
    colors = get_hue_spread(points, saturation, value)
    lab_delta_norm = calculate_lab_delta_norm(colors)
    desired_deltas = numpy.linspace(0.0, numpy.sum(lab_delta_norm), count+1)[:count]
    cum_delta_norm = numpy.cumsum(lab_delta_norm, axis=0)
    desired_indexes = [numpy.abs(cum_delta_norm - delta).argmin() for delta in desired_deltas]
    desired_colors = colors.take(desired_indexes)
    return desired_colors

def calculate_colormath_delta(colors):
    """calculates the norm of the deltas between each color in Lab space"""
    points = len(colors)
    labs = [colormath.color_objects.LabColor(*color.convert_to('lab').get_value_tuple()) for color in colors]
    # deltas = [labs[i].delta_e(labs[(i+1) % points], mode='cmc', pl=1, pc=1) for i in range(points)]
    deltas = [labs[i].delta_e(labs[(i+1) % points], mode='cie2000') for i in range(points)]
    return numpy.array(deltas)

def calculate_colormath_delta_matrix(colors):
    """calculates a matrix of the deltas between each pair of points"""
    points = len(colors)
    labs = [colormath.color_objects.LabColor(*color.convert_to('lab').get_value_tuple()) for color in colors]
    # deltas = [labs[i].delta_e(labs[(i+1) % points], mode='cmc', pl=1, pc=1) for i in range(points)]
    deltas = [[labs[i].delta_e(labs[j], mode='cie2000') for i in range(points)] for j in range(points)]
    return numpy.array(deltas)

def get_delta_spread_colors(count=12, saturation=DEFAULT_SATURATION, value=DEFAULT_VALUE):
    """returns an evenly spread number of colors around the lab color space, using the colormath delta function, with the given saturation and value"""
    points = count
    hues = numpy.linspace(0.0, 360.0, points+1)[:points]
    resolved = False
    while not resolved:
        hue_deltas = numpy.array([(360 + hues[(i+1) % points] - hues[i]) % 360 for i in range(points)])
        colors = numpy.array([colormath.color_objects.HSVColor(hue, saturation, value) for hue in hues])
        deltas = numpy.array([colors[i].delta_e(colors[(i+1) % points], mode='cie2000') for i in range(points)])
        print "D ", deltas
        delta_variance = deltas / numpy.average(deltas)
        print "dv", delta_variance
        in_range = 0
        for i in range(0, points):
            dv = delta_variance[i]
            if dv < 0.95:
                hue_deltas[i] += 1
            elif dv > 1.05:
                hue_deltas[i] -= 1
            else:
                in_range += 1
        if in_range == points:
            break
        # print hue_deltas
        hue_deltas *= 360.0 / sum(hue_deltas)
        print "hd", hue_deltas
        hues = [numpy.sum(hue_deltas[:i]) for i in range(points)]
        print "H ", hues
    desired_colors = [colormath.color_objects.HSVColor(hue, saturation, value) for hue in hues]
    return desired_colors

def get_lab_spread_hues(count=12, saturation=DEFAULT_SATURATION, value=DEFAULT_VALUE):
    """returns an evenly spread number of hues around the lab color space, with the given saturation and value, as rgb"""
    return [rgb_float_tuple(color) for color in get_lab_spread_colors(count, saturation, value)]

def get_delta_spread_hues(count=12, saturation=DEFAULT_SATURATION, value=DEFAULT_VALUE):
    """returns an evenly spread number of hues around the lab color space by measuring deltas, with the given saturation and value, as rgb"""
    return [rgb_float_tuple(color) for color in get_delta_spread_colors(count, saturation, value)]

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

def hue_tone_rotation_table(interval=1, hues_function=None):
    hues = get_delta_spread_hues() if hues_function is None else hues_function()
    cycle = list(tone_cycle(interval))
    hue_cycle = list(tone_cycle(7))
    for i in range(12):
        hue_i = hue_cycle.index(cycle[i])
        r, g, b = (int(l*255) for l in hues[hue_i])
        rot = (hue_i % 4)
        yield tones[i], (r, g, b), rot

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

def lilypond_pitch_colors(hue_function=None):
    """generates tuples of lilypond pitch definitions and colors"""
    # hues = get_delta_spread_hues() if hues_function is None else hues_function()
    colors = get_lab_spread_colors()
    hue_cycle = list(tone_cycle(7))
    count = len(tones)
    for note, tone in enumerate("abcdefg"):
        base_tone_index = tones.index(tone.upper())
        for offset, accidental in [(0, ""), (-1, "es"), (+1, "is"), (-2, "eses"), (+2, "isis")]:
            tone_index = (base_tone_index + offset + count) % count
            hue_index = hue_cycle.index(tone_index)
            # lilypond pitches are C-based
            lilypond_note = (note + 7 - 2) % 7
            if offset:
                yield ("0 %d %d/2" % (lilypond_note, offset), colors[hue_index])
            else:
                yield ("0 %d %d" % (lilypond_note, offset), colors[hue_index])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
chromaturn_ly_filename = os.path.join(BASE_DIR, "chromaturn.ly")
_lilypond_bool = {"#f": False, "#t": True}

def lilypond_has_chromaturn():
    check_file = os.path.join(BASE_DIR, "check-chromaturn.ly")
    response = subprocess.check_output(["lilypond", check_file], cwd=BASE_DIR, stderr=subprocess.PIPE).strip()
    if response in _lilypond_bool:
        return _lilypond_bool[response]
    raise ValueError("Unexpected response trying to check for chromaturn presence in lilypond: %s" % response)


if __name__ == "__main__":
    import sys
    L = locals()
    for arg in sys.argv[1:]:
        if arg in L and hasattr(L[arg], "show"):
            print ("Running %s" % arg)
            L[arg].show()
        else:
            print ("Could not find %s" % arg)

