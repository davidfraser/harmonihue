#!/usr/bin/env python

from matplotlib import pyplot
import math
from figurine import *
from torus import *

@figure_function
def draw_even_temper():
    """draws a diagram of the different rational frequences and how they related to the even-tempered twelve-tone scale"""
    fig = pyplot.figure(1, figsize=(10,4))
    ax = fig.add_axes([0.25, 0.15, 0.65, 0.75])
    ax.semilogx(base=2)
    bases = [2, 3, 5, 7, 11]
    for i, base in enumerate(bases):
        for j in [0, 1] if (base == 2) else list(range(-6,7)):
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
    ax.set_yticks(list(range(len(bases)+1)))
    ax.set_yticklabels(["(even-temper) $2^\\frac{1}{12}$"] + ["%s $\\frac{1}{%d}$" % (y_tick_info.get(base, ""), base) for base in bases])
    ax.set_ylabel("base harmonic ratio")
    even_temper = [2 ** (float(i)/12) for i in range(13)]
    ax.scatter(even_temper, [0]*13)
    ax.set_xticks(even_temper)
    ax.set_xticklabels([str(i) for i in range(len(even_temper))])
    ax.set_xlim((1, 2))
    ax.set_xlabel("frequency ($log 2$)")
    ax.xaxis.grid(True)
    return fig

@figure_function
def draw_tone_circle(interval):
    """A diagram of the circle of fifths/semitones with nothing drawn on it"""
    return interval_circle_figure(interval)[1]

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

@figure_function
def draw_torus_tone_cycles(interval=3, R=10.0, r=5.0):
    """Draws a torus with the given tone cycles on"""
    fig = draw_torus(R, r, figsize=(5,5))
    ax = fig.axes[0]
    torus_tone_cycles(ax, interval, R, r)
    set_torus_view(ax, R, r)
    return fig

if __name__ == '__main__':
    cmdline_show_figure(available_figure_functions(locals()))

