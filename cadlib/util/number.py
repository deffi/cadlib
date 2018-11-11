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


def to_number2(value, label = None):
    if isinstance(value, Number):
        return value
    else:
        raise TypeError(f"Invalid {label}: {value!r} ({type(value)}")


# TODO remove and rename to_number2 to to_number
def to_number(value, default, label, default_values = [None]):
    if value in default_values:
        return default
    elif isinstance(value, Number):
        return value
    else:
        raise TypeError("Invalid {}: {} ({})".format(label, repr(value), type(value)))
