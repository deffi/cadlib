from numbers import Number

from cadlib.util.vector import Vector

def to_list_of_numbers(value, label = None, required_length = None):
    # Value must be one of the supported types
    if not isinstance(value, (Vector, list, tuple)):
        raise TypeError("Not a valid list of numbers: {}".format(value))

    # Value must have the correct length, if specified
    if required_length is not None and len(value) != required_length:
        raise ValueError("Invalid length for {}, must be {}".format(label, required_length))

    # Elements must be numbers
    for x in value:
        if not isinstance(x, Number):
            raise TypeError("Must be a number: {}".format(x))

    return list(value)


def to_number(value, label = None, *, default = None):
    if isinstance(value, Number):
        return value
    elif value is None and default is not None:
        # TODO test
        return default
    else:
        raise TypeError(f"Invalid {label}: {value!r} ({type(value)}")
