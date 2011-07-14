#!/usr/bin/env python

"""A set of functions that are called from within book.genshi.html"""

import colorsys
import math
import os
import grapefruit
import matplotlib
from matplotlib import pyplot
from mpl_toolkits import mplot3d
import numpy
import decorator

OUTPUT_DIR = "out"

tones = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab"]
scales = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 11],
    'pentatonic': [0, 2, 4, 7, 9],
}
chords = {
    'maj': [0, 4, 7],
    'min': [0, 3, 7],
    'maj7': [0, 4, 7, 11],
    '7': [0, 4, 7, 10],
    'min7': [0, 3, 7, 10],
    'sus4': [0, 5, 7],
    'sus2': [0, 2, 7],
    'dim': [0, 3, 6],
    'aug': [0, 4, 8],
}

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

def filename_part(x):
    if isinstance(x, basestring):
        return x
    if isinstance(x, (int, float, type(None))):
        return repr(x)
    if isinstance(x, (list, tuple)):
        return "_".join(filename_part(e) for e in x)
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

def get_spread_hues(count=12, saturation=1.0, value=0.8):
    """returns an evenly spread number of hues, with the given saturation and value, as rgb"""
    return [colorsys.hsv_to_rgb(float(count*2 - i)/count, saturation, value) for i in range(count)]

def get_lab_spread_colors(count=12, saturation=1.0, value=0.8):
    """returns an evenly spread number of colors around the lab color space, with the given saturation and value, as rgb"""
    points = count*10
    hues = numpy.linspace(360.0, 0.0, points)
    colors = numpy.array([grapefruit.Color.NewFromHsv(hue, saturation, value) for hue in hues])
    labs = numpy.array([color.lab for color in colors])
    lab_delta = numpy.diff(labs, axis=0) * points * (1, 50, 50) # scale up a and b so the ranges are comparable
    lab_delta_norm = numpy.apply_along_axis(numpy.linalg.norm, 1, lab_delta)
    desired_deltas = numpy.linspace(0.0, numpy.sum(lab_delta_norm), count+1)[:count]
    cum_delta_norm = numpy.cumsum(lab_delta_norm, axis=0)
    desired_indexes = [numpy.abs(cum_delta_norm-delta).argmin() for delta in desired_deltas]
    desired_colors = colors.take(desired_indexes)
    return desired_colors

def get_lab_spread_hues(count=12, saturation=1.0, value=0.8):
    """returns an evenly spread number of hues around the lab color space, with the given saturation and value, as rgb"""
    return [color.rgb for color in get_lab_spread_colors(count, saturation, value)]

@figure_function
def draw_lab_hues(R=10.0, r=5.0, figsize=(5,5)):
    """Draws the spread hue values in the Lab color space"""
    fig = pyplot.figure(1, figsize=figsize)
    ax = mplot3d.Axes3D(fig)
    count = 12
    points = count * 10
    saturation, value = 1.0, 0.8
    hues = numpy.linspace(360.0, 0.0, points)
    colors = [grapefruit.Color.NewFromHsv(hue, saturation, value) for hue in hues]
    lab_colors = numpy.array([color.lab for color in colors])
    rgb_colors = [color.rgb for color in colors]
    L, a, b = lab_colors.transpose()
    ax.scatter(L, a, b, s=20, color=rgb_colors)
    new_colors = get_lab_spread_colors()
    lab_colors = numpy.array([color.lab for color in new_colors])
    rgb_colors = [color.rgb for color in new_colors]
    L, a, b = lab_colors.transpose()
    ax.scatter(L, a, b, s=200, color=rgb_colors)
    return fig

def get_hsv_circle_hues(count=12, saturation=0.75, value=0.75):
    """returns a hsv color range corresponding roughly to the torus, as rgb"""
    M_s, M_h = 0.1875, 0.1875
    hsv_map = {0: (saturation+M_s, value+M_h), 1: (saturation+M_s, value-M_h), 2: (saturation-M_s, value-M_h), 3: (saturation-M_s, value+M_h)}
    return [colorsys.hsv_to_rgb(float(count*2 - i)/count, hsv_map[i%4][0], hsv_map[i%4][1]) for i in range(count)]

@figure_function
def draw_hue_tone_circle(interval=7, hues_function=None, radius=1):
    """A diagram of the circle of fifths/semitones with hue mapped on it"""
    cycle, fig = interval_circle_figure(interval)
    hue_cycle = list(tone_cycle(7))
    if hues_function is None:
        hues = get_spread_hues()
    else:
        hues = hues_function()
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
    hues = get_spread_hues()
    ax = fig.axes[0]
    scatter_gamma = numpy.arange(0, 2*numpy.pi, 2*numpy.pi/12)
    for i in range(12):
        hue_i = hue_cycle.index(cycle[i])
        ax.scatter(scatter_gamma[i], 0.875, color=hues[hue_i], s=100, marker=(2, 0, (hue_i%4)*numpy.pi/4), linewidths=(4))
    return fig

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

def tone_sequence(ax, base_sequence, sequence):
    s = 2*math.pi/12
    l = len(sequence)
    gamma = [s*base_sequence.index(i) for i in sequence]
    r = [1 for i in sequence]
    ax.plot(gamma, r)
    return ax

@figure_function
def draw_scale(scale_name, base_interval=7):
    base_cycle, fig = interval_circle_figure(base_interval)
    ax = fig.axes[0]
    scale = scales[scale_name][:]
    scale.append(scale[0])
    tone_sequence(ax, base_cycle, scale)
    return fig

@figure_function
def draw_chord(chord_name, base_interval=7):
    base_cycle, fig = interval_circle_figure(base_interval)
    ax = fig.axes[0]
    tone_sequence(ax, base_cycle, chords[chord_name])
    return fig

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
        gamma = [s*i for i in cycle]
        r = [1 for i in cycle]
        ax.plot(gamma, r)
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

def torus_tone_spiral(ax, R, r, color='yellow'):
    """Draws a tone spiral around a torus of given radii"""
    u = numpy.linspace(0, 2*numpy.pi, 180)
    v = numpy.linspace(0, 3*2*numpy.pi, 180)
    x = (R + r*numpy.cos(v))*numpy.cos(u)
    y = (R + r*numpy.cos(v))*numpy.sin(u)
    z = r*numpy.sin(v)
    return ax.plot(x, y, z, color='yellow')

def torus_tone_coords(R, r):
    """Returns the x, y, z vectors for 12 tone points around the torus"""
    u = numpy.linspace(0, 2*numpy.pi, 13)[:12]
    v = numpy.linspace(0, 3*2*numpy.pi, 13)[:12]
    x = (R + r*numpy.cos(v))*numpy.cos(u)
    y = (R + r*numpy.cos(v))*numpy.sin(u)
    z = r*numpy.sin(v)
    return x, y, z

def torus_tone_points(ax, R, r, color='orange'):
    """Draws tone points and labels them around a torus of given radii"""
    x, y, z = torus_tone_coords(R, r)
    cycle = list(tone_cycle(7))
    cycle.reverse()
    for n, i in enumerate(cycle):
        ax.text(x[n], y[n], z[n], tones[i])
    return ax.scatter(x, y, z, color='orange')

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
    ax.plot(xc, yc, zc)

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
    ax.plot(xc, yc, zc)

def torus_tone_cycles(ax, interval, R, r, base_interval=7):
    """Draws straight lines between tone points to show interval cycles on torus"""
    base_cycle = list(tone_cycle(base_interval))
    base_cycle.reverse()
    x, y, z = torus_tone_coords(R, r)
    s = 2*math.pi/12
    for offset in range(0, (interval if (12 % interval == 0) else 1)):
        tone_indexes = list(tone_cycle(interval, offset))
        cycle = [base_cycle.index(i) for i in tone_indexes]
        cycle.reverse()
        l = len(cycle)
        cycle.append(cycle[0])
        xc = [x[c] for c in cycle]
        yc = [y[c] for c in cycle]
        zc = [z[c] for c in cycle]
        ax.plot(xc, yc, zc)

def set_torus_view(ax, R, r):
    ax.set_xlim3d((-R-r, R+r))
    ax.set_ylim3d((-R-r, R+r))
    ax.set_zlim3d((-R-r, R+r))
    ax.view_init(50, 30) 

@figure_function
def draw_torus(R=10.0, r=5.0, figsize=(10,10)):
    """Draws a torus"""
    fig = pyplot.figure(1, figsize=figsize)
    ax = mplot3d.Axes3D(fig)
    torus = torus_figure(ax, R, r, color='grey')
    spiral = torus_tone_spiral(ax, R, r, color='yellow')
    # stop the spiral from using the first default color
    ax._get_lines._clear_color_cycle()
    fig.points = torus_tone_points(ax, R, r, color='orange')
    set_torus_view(ax, R, r)
    return fig

@figure_function
def draw_hue_torus_tone_circle(R=10.0, r=5.0):
    """draws the hues of the color map onto the torus"""
    fig = draw_torus(R, r, figsize=(5,5))
    fig.points.remove()
    x, y, z = torus_tone_coords(R, r)
    ax = fig.axes[0]
    hue_cycle = list(tone_cycle(7))
    hues = get_spread_hues()
    for interval, hue in enumerate(hues):
        ax.scatter([x[interval]], [y[interval]], [z[interval]], s=100, color=hue)
    set_torus_view(ax, R, r)
    return fig

@figure_function
def draw_torus_tone_cycles(interval=3, R=10.0, r=5.0):
    """Draws a torus with the given tone cycles on"""
    fig = draw_torus(R, r, figsize=(5,5))
    ax = fig.axes[0]
    torus_tone_cycles(ax, interval, R, r)
    set_torus_view(ax, R, r)
    return fig

@figure_function
def draw_torus_scale(scale_name, R=10.0, r=5.0):
    """Draws a torus with the given tone cycles on"""
    fig = draw_torus(R, r, figsize=(5,5))
    ax = fig.axes[0]
    torus_scale(ax, scale_name, R, r)
    set_torus_view(ax, R, r)
    return fig

@figure_function
def draw_torus_chord(chord_name, R=10.0, r=5.0):
    """Draws a torus with the given tone cycles on"""
    fig = draw_torus(R, r, figsize=(5,5))
    ax = fig.axes[0]
    torus_chord(ax, chord_name, R, r)
    set_torus_view(ax, R, r)
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

