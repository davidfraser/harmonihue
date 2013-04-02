#!/usr/bin/env python

"""constants and functions related to the layout of guitar strings and the decorations for the fretboard"""

from book_helpers import *

strings = ["E", "A", "D", "G", "B", "E"]
string_count = len(strings)
units = "cm"
edge_string_gap = 0.5
# the gap between strings is the distance between the top and bottom strings divided by the gaps
nut_string_gap = 3.2
saddle_string_gap = 4.6
string_length = 48
string_width = 0.1
frets = 18
dotted_frets = [5, 7, 9, 12]
fret_width = 0.2
sticker_radius = 0.3
dot_radius = 0.15
show_guitar = True

nut_width = fret_width * 2
saddle_width = fret_width * 2

vcenter = saddle_string_gap/2

def string_gap(hpos):
    """calculated the gap between strings at this distance along the guitar"""
    ratio = hpos/string_length
    return saddle_string_gap * (1-ratio) + nut_string_gap * ratio

def string_pos(s, hpos):
    """returns the vertical position of the given string at that horizontal position"""
    gap = string_gap(hpos)
    return vcenter - (gap/2) + (s*gap/(string_count-1))

fretboard_height = (edge_string_gap*2) + string_gap(nut_string_gap)*(string_count-1)
fret_height = fretboard_height
fret_pos = [string_length/(2**(fret/12.)) for fret in range(frets+1)]
fret_cpos = [(fret_pos[fret]+fret_pos[fret+1])/2 for fret in range(frets)]
hue_cycle = list(tone_cycle(7))
colors = get_lab_spread_colors(saturation=1.0, value=0.6)
hue_colors = [colors[hue_cycle.index((index)%12)] for index in range(12)]
figure_width = string_length + saddle_width + nut_width
figure_height = saddle_string_gap + edge_string_gap*2 + dot_radius*2

