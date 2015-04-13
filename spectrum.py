#!/usr/bin/env python

import colormath.color_objects
import decorator
import numpy

DEFAULT_SATURATION = 1.0
DEFAULT_VALUE = 0.8

def rgb_hex(c):
    """converts a colormath color object to an rgb hex string for html like #30bf30"""
    return c.convert_to('rgb').get_rgb_hex()

def rgb_float_tuple(c):
    """converts a colormath color object to an rgb tuple in the range [0, 1)"""
    r, g, b = c.convert_to('rgb').get_value_tuple()
    return (r/255., g/255., b/255.)

@decorator.decorator
def rgb_tuplize(f, *args, **kwargs):
    """when f produces a list of color objects, converts them all to rgb tuples"""
    return [rgb_float_tuple(c) for c in f(*args, **kwargs)]

def color_function(f):
    f.rgb = rgb_tuplize(f)
    return f

def lighter_color(c, level):
    """lightens the color by increasing the HSL lightness value by the given amount"""
    c2 = c.convert_to('hsl')
    c2.hsl_l = min(1, c2.hsl_l + level)
    return c2

def get_hsv_circle_hues(count=12, saturation=0.75, value=0.75):
    """returns a hsv color range corresponding roughly to the torus, as rgb"""
    M_s, M_h = 0.1875, 0.1875
    hsv_map = {0: (saturation+M_s, value+M_h), 1: (saturation+M_s, value-M_h), 2: (saturation-M_s, value-M_h), 3: (saturation-M_s, value+M_h)}
    return [colormath.color_objects.HSVColor(360*float(count*2 - i)/count, hsv_map[i%4][0], hsv_map[i%4][1]) for i in range(count)]

@color_function
def get_hue_spread(points=12, saturation=DEFAULT_SATURATION, value=DEFAULT_VALUE):
    """Returns a set of colors distributed in a circle around the Hsv space with fixed saturation and value"""
    hues = numpy.linspace(360.0, 0.0, points+1)[:points]
    colors = numpy.array([colormath.color_objects.HSVColor(hue, saturation, value) for hue in hues])
    return colors

def apply_scale_shifts(scale_shifts):
    result = []
    _start_range = 0
    _target_offset = 0
    for _end_range, _range_scale in scale_shifts:
        result.append((_start_range, _end_range, _target_offset, _range_scale))
        _target_offset += (_end_range - _start_range) * _range_scale
        _start_range = _end_range
    return result

def compile_scale_shifts(scale_shifts):
    code = []
    code.append("def scale_shift(h):\n    return ")
    for start_range, end_range, target_offset, range_scale in apply_scale_shifts(scale_shifts):
        code.append("(%r+(h-%r)*%r) if %r <= h < %r " % (target_offset, start_range, range_scale, start_range, end_range))
        code.append("else ")
    code = code + ["None\n"]
    c = compile("".join(code), __file__, "exec")
    exec(c)
    return scale_shift

# yellow is half way between green and red
# so red=0=360, blue=240, green=120 -> yellow=60
SCALE_SHIFTS = [
    (120, 0.5),    # shift green to yellow
    (240, 1.5),    # compress green-blue
    (300, 45/60.),    # expand blue-purple slightly
    (360, 75/60.),    # squish purple-red
    (361, 1.0),    # don't die on handling 360 hues
]

ymap_scale_shifter = compile_scale_shifts(SCALE_SHIFTS)

def ymap(hues):
    """makes yellow the midpoint between red and blue, instead of green"""
    return [ymap_scale_shifter(hue) for hue in hues]

@color_function
def get_yhue_spread(points=12, saturation=DEFAULT_SATURATION, value=DEFAULT_VALUE):
    """Returns a set of colors distributed in a circle around the Hsv space, but with RYB equidistant instead of RGB, with fixed saturation and value"""
    hues = numpy.linspace(360.0, 0.0, points+1)[:points]
    hues = ymap(hues)
    colors = numpy.array([colormath.color_objects.HSVColor(hue, saturation, value) for hue in hues])
    return colors

@color_function
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

def calculate_lab_delta_norm(colors, scale=(1, 0.5, 0.5)):
    """calculates the norm of the deltas between each color in Lab space"""
    points = len(colors)
    labs = numpy.array([color.convert_to('lab').get_value_tuple() for color in colors])
    lab_delta = numpy.diff(labs, axis=0) * points * scale # scale up a and b so the ranges are comparable
    lab_delta_norm = numpy.apply_along_axis(numpy.linalg.norm, 1, lab_delta)
    return lab_delta_norm

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

@color_function
def get_delta_spread_colors(count=12, saturation=DEFAULT_SATURATION, value=DEFAULT_VALUE, use_ymap=False):
    """returns an evenly spread number of colors around the lab color space, using the colormath delta function, with the given saturation and value"""
    points = count
    max_variance = 0.05 if count <= 60 else 0.1
    direction = -1
    if direction > 0:
        hues = numpy.linspace(0.0, 360.0, points+1)[:points]
    else:
        hues = numpy.linspace(360.0, 0.0, points+1)[:points]
    resolved = False
    while not resolved:
        deg_delta = lambda deg1, deg2: (360 + (deg1-deg2)) % 360
        norm_deg_delta = lambda dd: dd if dd <= 180 else dd-360
        hue_deltas = numpy.array([norm_deg_delta(deg_delta(hues[(i+1) % points], hues[i])) for i in range(points)])
        colors = numpy.array([colormath.color_objects.HSVColor(hue, saturation, value) for hue in hues])
        deltas = numpy.array([colors[i].delta_e(colors[(i+1) % points], mode='cie2000') for i in range(points)])
        # print "D ", deltas
        delta_variance = deltas / numpy.average(deltas)
        # print "dv", delta_variance
        in_range = 0
        for i in range(0, points):
            dv = delta_variance[i]
            if dv < 1 - max_variance:
                hue_deltas[i] += direction * 12.0/count
            elif dv > 1 + max_variance:
                hue_deltas[i] -= direction * 12.0/count
            else:
                in_range += 1
        if in_range == points:
            break
        # print "hd~", hue_deltas
        hue_deltas *= direction * 360.0 / sum(hue_deltas)
        # print "hd", hue_deltas
        hues = [numpy.sum(hue_deltas[:i]) % 360 for i in range(points)]
        print "H ", hues
    if use_ymap:
        hues = ymap(hues)
    desired_colors = [colormath.color_objects.HSVColor(hue, saturation, value) for hue in hues]
    return desired_colors

@color_function
def get_ydelta_spread_colors(count=12, saturation=DEFAULT_SATURATION, value=DEFAULT_VALUE):
    return get_delta_spread_colors(count, saturation, value, use_ymap=True)

@color_function
def get_sine_bow_colors(count=12, saturation=None, value=None):
    hues = numpy.linspace(numpy.pi/2, numpy.pi*3/2, count+1)[:count]
    r = numpy.sin(hues)
    g = numpy.sin(hues + numpy.pi/3)
    b = numpy.sin(hues + 2*numpy.pi/3)
    r, g, b = r*r, g*g, b*b
    return [colormath.color_objects.RGBColor(r[i]*255, g[i]*255, b[i]*255) for i in range(count)]


# use this to affect pages that are just wanting to use the chosen color spreading function
default_spread_colors = get_yhue_spread

