from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import six
import warnings
import numpy as np
from matplotlib.layoutbox import get_renderer

"""
Simple utility functions to parse and translate common
drawing units
"""

suffixes = ['in', 'cm', 'mm', 'px', 'pt', 'em']
cmperin = 2.54
mmperin = 25.4
ptperin = 72.272


def tofigw(lenstr, fig):
    """

    """
    return tofig(lenstr, fig, 'width')


def tofigh(lenstr, fig):
    """

    """
    return tofig(lenstr, fig, 'height')


def tofig(lenstr, fig, dir):
    """

    """

    if is_numlike(lenstr):
        return lenstr
    units = lenstr[-2:]
    try:
        val = float(lenstr[:-2])
    except ValueError:
        raise Exception("Couldn't convert value %s to a float" % str[:-2])
    if units not in suffixes:
        raise Exception("Unit %s is not in list of acceptable units" % unit)

    renderer = get_renderer(fig)
    if dir == 'width':
        widthpx = renderer.width
    else:
        widthpx = renderer.height
    dpi = renderer.dpi
    if units == 'px':
        return (val / widthpx)
    if units == 'in':
        return (val * dpi / widthpx)
    if units == 'cm':
        return (val / cmperin * dpi / widthpx)
    if units == 'mm':
        return (val / mmperin * dpi / widthpx)
    if units == 'pt':
        return (val / ptperin * dpi / widthpx)
    else:
        raise Exception("")
