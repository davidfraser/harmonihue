#!/usr/bin/env python

import decorator
from matplotlib import pyplot
import os.path
import types
from config import *

def filename_part(x):
    if isinstance(x, basestring):
        return x
    if isinstance(x, (int, float, type(None))):
        return repr(x)
    if isinstance(x, (list, tuple)):
        return "_".join(filename_part(e) for e in x)
    if isinstance(x, types.FunctionType):
        return x.__name__
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

