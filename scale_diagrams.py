#!/usr/bin/env python

from figurine import *
from musicality import *
from torus import *

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

if __name__ == '__main__':
    cmdline_show_figure(available_figure_functions(locals()))

