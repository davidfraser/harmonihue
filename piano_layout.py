#!/usr/bin/env python

"""constants and functions related to the layout of a piano-style keyboard and the decorations for the fretboard"""

from musicality import *
from spectrum import *

octaves = 2 
height = 120.0
octave_width = 160.0
total_width = octaves * octave_width

height_black = height * 2/3
width_black = octave_width / 12
width_white = octave_width / 7
white_sticker_radius = width_white * 1/3
black_sticker_radius = width_black * 2/5
c_tones = tones[3:] + tones[:3]
white_notes = [index for index, tone in enumerate(c_tones + [c_tones[0]]) if len(tone) == 1]
black_notes = [index for index, tone in enumerate(c_tones) if len(tone) >  1]
hue_cycle = list(tone_cycle(7))
colors = default_spread_colors(saturation=1.0, value=0.6)
hue_colors = [colors[hue_cycle.index((index+3)%12)] for index in range(12)]
hue_rotations = [index % 4 for index in range(12)]
bg_colors = [lighter_color(color, 0.6) for color in hue_colors]

figure_width = total_width / 10
figure_height = height / 10

