#!/usr/bin/env python

import colormath.color_objects
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

def lighter_color(c, level):
    """lightens the color by increasing the HSL lightness value by the given amount"""
    c2 = c.convert_to('hsl')
    c2.hsl_l = min(1, c2.hsl_l + level)
    return c2

def get_hue_spread(points, saturation=DEFAULT_SATURATION, value=DEFAULT_VALUE):
    """Returns a set of colors distributed in a circle around the Hsv space with fixed saturation and value"""
    hues = numpy.linspace(360.0, 0.0, points)
    colors = numpy.array([colormath.color_objects.HSVColor(hue, saturation, value) for hue in hues])
    return colors

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

