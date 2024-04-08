import os.path
import subprocess
from musicality import *
from spectrum import *

def lilypond_pitch_colors(hues_function=None):
    """generates tuples of lilypond pitch definitions and colors"""
    colors = default_spread_colors() if hues_function is None else hues_function()
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

def lilypond_pitch_rotations():
    """generates tuples of lilypond pitch definitions and colors"""
    hue_cycle = list(tone_cycle(7))
    count = len(tones)
    for note, tone in enumerate("abcdefg"):
        base_tone_index = tones.index(tone.upper())
        for offset, accidental in [(0, ""), (-1, "es"), (+1, "is"), (-2, "eses"), (+2, "isis")]:
            tone_index = (base_tone_index + offset + count) % count
            hue_index = hue_cycle.index(tone_index)
            rotation = get_rotation(hue_index)
            # lilypond pitches are C-based
            lilypond_note = (note + 7 - 2) % 7
            if offset:
                yield ("0 %d %d/2" % (lilypond_note, offset), rotation)
            else:
                yield ("0 %d %d" % (lilypond_note, offset), rotation)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
chromaturn_ly_filename = os.path.join(BASE_DIR, "chromaturn.ly")
_lilypond_bool = {"#f": False, "#t": True}

def lilypond_has_chromaturn():
    check_file = os.path.join(BASE_DIR, "check-chromaturn.ly")
    response = subprocess.check_output(["lilypond", check_file], cwd=BASE_DIR, stderr=subprocess.PIPE).strip()
    if response in _lilypond_bool:
        return _lilypond_bool[response]
    raise ValueError("Unexpected response trying to check for chromaturn presence in lilypond: %s" % response)

