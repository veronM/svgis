#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of svgis.
# https://github.com/fitnr/svgis

# Licensed under the GNU General Public License v3 (GPLv3) license:
# http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2016, Neil Freeman <contact@fakeisthenewreal.org>

'''
Create string versions of SVG elements.
'''


def _wrap(tag, contents=None, **kwargs):
    '''Wrap contents in a tag'''
    attribs = toattribs(**kwargs)
    if contents:
        return u'<{0}{1}>{2}</{0}>'.format(tag, attribs, contents)
    else:
        return u'<{0}{1}/>'.format(tag, attribs)


def _element(tag, **kwargs):
    return u'<{}{}/>'.format(tag, toattribs(**kwargs))


def _round(i, precision):
    if precision is None:
        return i
    else:
        return round(i, precision)


def _fmtcoord(precision):
    if precision is None:
        return u'{0[0]},{0[1]}'
    else:
        return u'{{0[0]:.{0}f}},{{0[1]:.{0}f}}'.format(precision)


def circle(point, precision=None, **kwargs):
    '''
    Create a svg circle element. Keyword arguments are mapped to attributes.

    Args:
        point (tuple): The center of the circle
        precision (int): rounding precision

    Returns:
        str
    '''
    return _element(u'circle', cx=_round(point[0], precision), cy=_round(point[1], precision), **kwargs)


def text(string, start, precision=None, **kwargs):
    '''
    Create an svg text element.

    Args:
        string (str): text for element
        start (tuple): starting coordinate

    Returns:
        str
    '''
    start = [_round(i, precision) for i in start]
    return _wrap(u'text', string, x=start[0], y=start[1], **kwargs)


def rect(start, width, height, precision=None, **kwargs):
    '''
    Create an svg rect element.

    Args:
        start (tuple): starting coordinate
        width (int): rect width
        height (int): rect height
        precision (int): rounding precision

    Returns:
        str
    '''
    start = [_round(i, precision) for i in start]
    width = _round(width, precision)
    height = _round(height, precision)

    return _element(u'rect', x=start[0], y=start[1], width=width, height=height, **kwargs)


def line(start, end, precision=None, **kwargs):
    '''
    Create an svg line element.

    Args:
        start (tuple): starting coordinate
        end (tuple): ending coordinate
        precision (int): rounding precision

    Returns:
        str
    '''
    start = [_round(i, precision) for i in start]
    end = [_round(i, precision) for i in end]

    return _element(u'line', x1=start[0], y1=start[1], x2=end[0], y2=end[1], **kwargs)


def _isstr(x):
    return isinstance(x, basestring)


def path(coordinates, precision=None, **kwargs):
    '''
    Create an svg path element as a string.

    Args:
        coordinates (Sequence): A sequence of coordinates and string instructions
        precision (int): rounding precision

    Returns:
        str
    '''
    fmt = _fmtcoord(precision)
    coords = [i if _isstr(i) else fmt.format(i) for i in coordinates]
    return _element(u'path', d=' '.join(coords), **kwargs)


def polyline(coordinates, precision=None, **kwargs):
    '''
    Create an svg polyline element

    Args:
        coordinates (Sequence): x, y coordinates
        precision (int): rounding precision

    Returns:
        str
    '''
    fmt = _fmtcoord(precision)
    points = u' '.join(fmt.format(c) for c in coordinates)
    return _element(u'polyline', points=points, **kwargs)


def polygon(coordinates, precision=None, **kwargs):
    '''
    Create an svg polygon element

    Args:
        coordinates (Sequence): x, y coordinates
        precision (int): rounding precision

    Returns:
        str
    '''
    fmt = _fmtcoord(precision)
    points = u' '.join(fmt.format(c) for c in coordinates)
    return _element(u'polygon', points=points, **kwargs)


def toattribs(**kwargs):
    attribs = u' '.join(u'{}="{}"'.format(k, v) for k, v in kwargs.items() if v is not None)

    if len(attribs) > 0:
        attribs = ' ' + attribs

    return attribs


def defstyle(style=None):
    '''
    Create a defs element that wraps a CSS style.

    Args:
        style (string): A CSS string.

    Returns:
        unicode
    '''
    if style:
        return u'<defs><style type="text/css"><![CDATA[{}]]></style></defs>'.format(style)
    else:
        return u'<defs />'


def group(members=None, **kwargs):
    '''
    Create a group with the given scale and translation.

    Args:
        members (Sequence): unicode SVG elements
        kwargs (dict): elements of this dictionary will be converted to
                        attributes of the group, i.e. key="value".

    Returns:
        unicode
    '''
    members = members or ''
    return _wrap(u'g', ''.join(members), **kwargs)


def drawing(size, members, viewbox=None, style=None):
    '''
    Create an SVG element.

    Args:
        size (tuple): width, height
        members (list): Strings to add to output.
        viewbox (Sequence): Four coordinates that describe an SVG viewBox.
        style (string): CSS string.
    '''
    kwargs = {
        'width': size[0],
        'height': size[1],
        'baseProfile': 'full',
        'version': '1.1',
        'xmlns': 'http://www.w3.org/2000/svg',
    }
    if viewbox:
        kwargs['viewBox'] = '{},{},{},{}'.format(*viewbox)

    contents = defstyle(style) + u''.join(members)
    return _wrap(u'svg', contents, **kwargs)
