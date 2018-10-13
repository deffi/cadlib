from numbers import Number

from cadlib.geometry.vector import Vector

def to_list_of_numbers(value, label = None, required_length = None):
    if required_length is not None and len(value) != required_length:
        raise ValueError("Invalid length for {}, must be {}".format(label, required_length))

    for x in value:
        if not isinstance(x, Number):
            raise TypeError("Must be a number: {}".format(x))

    if isinstance(value, (Vector, list, tuple)):
        return list(value)
    else:
        raise TypeError("Not a valid list of numbers: {}".format(value))

def to_number(value, default, label, default_values = [None]):
    if value in default_values:
        return default
    elif isinstance(value, Number):
        return value
    else:
        raise TypeError("Invalid {}: {} ({})".format(label, repr(value), type(value)))
