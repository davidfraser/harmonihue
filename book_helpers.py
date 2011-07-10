#!/usr/bin/env python

"""A set of functions that are called from within book.genshi.html"""

import os
import pylab

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

def draw_tone_cycle(filename, interval, start=0):
    pylab.figure(1, figsize=(2,2))
    ax = pylab.axes([0.05, 0.05, 0.95, 0.95])
    cycle_7 = list(reversed([tones[i] for i in tone_cycle(7)]))
    pylab.pie([1.0/12]*12, colors=[(0.7,)*3, (0.9,)*3], labels=cycle_7)
    pylab.savefig(os.path.join(OUTPUT_DIR, filename))


