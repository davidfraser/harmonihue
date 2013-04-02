#!/usr/bin/env python

"""constants and functions related to the layout of a piano-style keyboard and the decorations for the fretboard"""

from book_helpers import *

octaves = 3
height = 120.0
height_black = height * 2/3
total_width = 160.0
width_black = total_width / 12
width_white = total_width / 7
c_tones = tones[3:] + tones[:3]
white_notes = [index for index, tone in enumerate(c_tones + [c_tones[0]]) if len(tone) == 1]
black_notes = [index for index, tone in enumerate(c_tones) if len(tone) >  1]
hue_cycle = list(tone_cycle(7))
colors = get_lab_spread_colors(saturation=1.0, value=0.6)
hue_colors = [colors[hue_cycle.index((index+3)%12)] for index in range(12)]
bg_colors = [color.LighterColor(0.6) for color in hue_colors]

figure_width = total_width / 10
figure_height = height / 10

