try:
    from shapely.geometry import shape, mapping
    import numpy as np
except ImportError:
    pass


def _expand_np(coordinates):
    return np.array(_expand_py(coordinates))


def _expand_py(coordinates):
    return list(coordinates)


def expand(ring):
    try:
        return _expand_np(ring)
    except NameError:
        return _expand_py(ring)


def expand_rings(rings):
    try:
        return [_expand_np(ring) for ring in rings]
    except NameError:
        return [_expand_py(ring) for ring in rings]


def expand_geom(geom):
    '''Expand generators in a geometry's coordinates.'''

    coordinates = geom['coordinates']

    if geom['type'] == 'MultiPolygon':
        geom['coordinates'] = [expand_rings(rings) for rings in coordinates]

    elif geom['type'] in ('Polygon', 'MultiLineString'):
        geom['coordinates'] = expand_rings(coordinates)

    elif geom['type'] in ('MultiPoint', 'LineString'):
        geom['coordinates'] = expand(coordinates)

    elif geom['type'] == 'Point':
        geom['coordinates'] = expand(coordinates)

    else:
        raise NotImplementedError("Unsupported geometry type " + geom['type'])

    return geom


def prepare(bbox):
    minx, miny, maxx, maxy = bbox
    bounds = {
        "type": "Polygon",
        "coordinates": [[(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny), (minx, miny)]]
    }
    try:
        bbox = shape(bounds)

        def func(geometry):
            geom = expand_geom(geometry)
            clipped = bbox.intersection(shape(geom))
            return mapping(clipped)

    except NameError:
        func = lambda geometry: geometry

    return func


def clip(geometry, bbox):
    '''Clip a geometry to a bounding box. BBOX may be a tuple or a shapely geometry object'''
    try:
        return prepare(bbox)(geometry)

    except NameError:
        return geometry