from numbers import Number

def valid(value):
    """Return true if the value is a valid number."""
    return isinstance(value, Number)


def convert(value, label = None, *, default = None):
    """Return a numeric value and handle non-numeric values.

    If value is not a number and default is specified, then default is returned.
    If value is not a number and default is not specified, then a TypeError is
    raised.
    """
    if valid(value):
        return value
    elif value is None and default is not None:
        return default
    else:
        # TODO None label
        raise TypeError(f"Invalid {label}: {value!r} ({type(value)}")


# def to_list_of_numbers(value, label = None, required_length = None):
#     # Value must be one of the supported types
#     if not Vector.valid_type(value):
#         raise TypeError("Not a valid list of numbers: {}".format(value))
#
#     # Value must have the correct length, if specified
#     if required_length is not None and len(value) != required_length:
#         raise ValueError("Invalid length for {}, must be {}".format(label, required_length))
#
#     # Elements must be numbers
#     for x in value:
#         if not valid(x):
#             raise TypeError("Must be a number: {}".format(x))
#
#     return list(value)


