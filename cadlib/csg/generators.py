from cadlib.csg import Union, Intersection, Difference

__all__ = ['union', 'intersection', 'difference']

def union(objects):
    return Union(objects)

def intersection(objects):
    return Intersection(objects)

def difference(objects):
    return Difference(objects)

