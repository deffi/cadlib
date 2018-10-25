from cadlib.csg import Union, Intersection, Difference

__all__ = ['union', 'intersection', 'difference']

def union(objects = None):
    return Union(objects or [])

def intersection(objects = None):
    return Intersection(objects or [])

def difference(objects = None):
    return Difference(objects or [])

