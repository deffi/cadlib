import math
from numbers import Number
from cadlib.util.table import Table
from cadlib.util import Matrix
from cadlib.util import number

class Vector:
    """An immutable vector with basic arithmetic.

    Note that __len__, like the dimensions property, returns the number of
    elements. The length property returns the vector's magnitude.

    Despite mathematical considerations, Vector does not inherit Matrix:
      * Vectors are subscripted with a single value (vector[i] rather than
        matrix[i, 0])
      * The size of a vector is a single value (vector.dimensions == 3 rather
        than matrix.dimensions == (3, 0))
      * Since arithmetic operations such as (Vector + Vector) and (Matrix
        * Vector) are supposed to return a vector, the corresponding methods
        would have to be overridden to convert the result to a vector.
      * Calling.transpose().transpose() on a Vector would change the type to
        Matrix.
      * Matrices are initialized from an iterable of iterables; vectors can be
        initialized from individual values because the distinction between
        initialization by row and by column is not required.
    """

    ####################
    ## Initialization ##
    ####################

    def __init__(self, *values):
        """Create a vector from individual values.

        The specified values must be numeric. A 0-dimensional vector can be
        created by passing no values."""
        for value in values:
            if not number.valid(value):
                raise TypeError("Vectors must consist of numeric values")

        self._values = list(values)

    @classmethod
    def zero(cls, size):
        """Create a vector of all-zeros with the specified size."""
        values = [0] * size
        return cls(*values)

    @classmethod
    def valid_type(cls, value):
        """Determine whether the specified value can be converted to a vector.

        Types that can be converted are Vector, list, and tuple.
        """
        return isinstance(value, (Vector, list, tuple))

    @classmethod
    def convert(cls, value, label, *, required_length = None):
        """Convert the specified value to a Vector.

        If the value cannot be converted to a vector (according to the
        valid_type class method), TypeError is raised. If required_length is
        specified and does not match the actual length, ValueError is raised.

        The label is used in the message of exceptions.
        """

        # Make sure the type can be converted to a vector
        if not cls.valid_type(value):
            raise TypeError(f"Invalid vector for {label}: {value}")

        # If a required length is specified, check that the length is correct
        if required_length is not None and len(value) != required_length:
            raise ValueError(f"Invalid length for {label}, must be {required_length}")

        # We can return vectors directly
        if isinstance(value, Vector):
            return value

        # All others, we convert
        return Vector(*value)


    ################
    ## Properties ##
    ################

    @property
    def dimensions(self):
        """Return the dimensions (i. e., the number of elements)"""
        return len(self._values)

    @property
    def is_zero(self):
        """Return true if all elements of the vector are 0."""
        return all(x == 0 for x in self._values)

    def __len__(self):
        """The length is the number of elements in the vector."""
        return len(self._values)

    def __getitem__(self, index):
        return self._values[index]


    ################
    ## Comparison ##
    ################

    def __eq__(self, other):
        """Vectors are equal if their values are equal."""
        return (isinstance(other, Vector)
            and self._values == other._values)


    ################
    ## Arithmetic ##
    ################

    def __add__(self, other):
        """Vectors are added element-wise. The dimensions must match."""
        if isinstance(other, Vector):
            if other.dimensions != self.dimensions:
                raise ValueError("Dimension mismatch: {} + {}".format(other.dimensions, self.dimensions))
            else:
                return Vector(*[x1 + x2 for x1, x2 in zip(self._values, other._values)])
        else:
            return NotImplemented

    def __sub__(self, other):
        """Vectors are subtract element-wise. The dimensions must match."""
        if isinstance(other, Vector):
            return self + (-other)
        else:
            return NotImplemented

    def __neg__(self):
        """Vectors are negated by scalar multiplication with -1."""
        return (-1) * self

    def __mul__(self, other):
        """Vectors can be multiplied with scalars."""
        if isinstance(other, Number):
            return Vector(*[x * other for x in self._values])
        else:
            return NotImplemented

    def __rmul__(self, other):
        """Vectors can be right-multiplied with scalars or matrices.

        For multiplication with a matrix, the dimensions of the matrix must be
        compatible with this vector.
        """

        if isinstance(other, Number):
            return self.__mul__(other)

        elif isinstance(other, Matrix):
            if self.dimensions != other.column_count:
                raise ValueError("Dimension mismatch: {} x {}".format(other.dimensions, self.dimensions))

            values = [sum(x1 * x2 for x1, x2 in zip(matrix_row, self._values)) for matrix_row in other.row_values]

            return Vector(*values)

        else:
            return NotImplemented

    def __truediv__(self, other):
        """Division is only possible with scalars."""
        if isinstance(other, Number):
            return Vector(*[x / other for x in self._values])
        else:
            return NotImplemented

    def dot(self, other):
        """Calculate the dot product between two vectors.

        The dimensions of the vectors must match.
        """
        if not isinstance(other, Vector):
            raise TypeError("Dot product is only defined for vectors")

        if other.dimensions != self.dimensions:
            raise ValueError("Dimension mismatch: {} · {}".format(other.dimensions, self.dimensions))

        return sum(a * b for a, b in zip(self._values, other._values))

    def cross(self, other):
        """Calculate the cross product between 3-vectors."""

        if not isinstance(other, Vector):
            raise TypeError("Cross product is only defined for vectors")

        if other.dimensions != 3 or self.dimensions != 3:
            raise ValueError("Cross product is only defined for 3-dimensional vectors")

        a = self._values
        b = other._values

        values = [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0],
        ]

        return Vector(*values)


    ##############
    ## Geometry ##
    ##############

    def angle(self, other):
        """Calculate the angle between two 3-vectors in radians."""

        # While mathematically correct, this performs poorly due to rounding
        # errors:
        #   * Vector(2, 3.4).angle(Vector(2, 3.4)) is only equal to 0.0 within 5
        #     decimal places
        #   * Vector(1, 1, 1).angle(Vector(-1, -1, -1)) fails because the
        #     argument of acos is -1.0000000000000002.
        # return math.acos(self.dot(other) / (self.length * other.length)) / degree

        # This is better
        # Source: https://math.stackexchange.com/questions/1143354/numerically-stable-method-for-angle-between-3d-vectors
        u = self
        v = other
        return 2 * math.atan2((v.length*u - u.length*v).length, (v.length*u + u.length*v).length)

    @property
    def length_squared(self):
        """Calculate the square of the magnitude."""
        return sum(x ** 2 for x in self._values)

    @property
    def length(self):
        """Calculate the magnitude."""
        return math.sqrt(self.length_squared)

    def normalized(self):
        """Calculate a vector with the same direction and magnitude 1.

        This will fail for zero-magnitude vectors.
        """
        return self / self.length

    def normal(self):
        """Calculate a normal for this vector.

        If there is no normal, ValueError is raised. If the normal is ambiguous,
        an arbitrary normal will be returned.

        The vector must have at least 2 dimensions and non-zero magnitude.
        """

        # Invalid operation for empty, one-dimensional, and zero-length vectors
        if len(self) == 0: raise ValueError("Empty vectors don't have normals")
        if len(self) == 1: raise ValueError("One-dimensional vectors don't have normals")
        if self.is_zero  : raise ValueError("Zero vectors don't have normals")

        # Algorithm: find any two values, at least one of which is not zero.
        # Swap them and negate one of them. Set all other values to zero. Note
        # that it is permissible for the negated value to be zero.

        # Find the index of the first non-zero value and the index of following value (wrapping around if necessary).
        i1 = next((index for index, value in enumerate(self._values) if value != 0), None)
        i2 = (i1 + 1) % len(self._values)

        # Create a list of zeros. Copy the values from index i1 and i2, inverting one of them.
        values = [0] * len(self._values)
        values[i1] = -self._values[i2]
        values[i2] =  self._values[i1]

        # Create a vector from the values
        return Vector(*values)

    def collinear(self, other):
        """Determine whether two vectors are collinear."""
        return self.dot(other) ** 2 == self.length_squared * other.length_squared

    def snap_to_axis(self):
        """Calculate the projection of this vector to the nearest axis."""

        _, index = max((abs(v), i) for i, v in enumerate(self._values))
        result_values = [0] * len(self)
        result_values[index] = self._values[index]
        return Vector(*result_values)

    def closest_axis(self):
        """Find the nearest (positive or negative) unit vector."""

        _, index = max((abs(v), i) for i, v in enumerate(self._values))
        result_values = [0] * len(self)
        result_values[index] = math.copysign(1, self._values[index])
        return Vector(*result_values)

    def replace(self, value, replacement):
        """Replace all items that have the specified value with the specified
        replacement.
        """
        values = [replacement if v == value else v for v in self._values]
        return Vector(*values)


    #########
    ## I/O ##
    #########

    def __str__(self):
        """Example: <1, 2, 3>"""
        return "<" + ", ".join(map(str, self._values)) + ">"

    def __repr__(self):
        return "Vector({})".format(", ".join(str(value) for value in self._values))

    def format(self):
        """Format the vector for human consumption"""
        return Table([[v] for v in self._values]).format(alignment="r")


    ##########
    ## Misc ##
    ##########

	# TODO remove? better name?
    def extend(self): # TODO unit test
        return Vector(*(self._values + [1]))

    def unextend(self): # TODO unit test
        if self._values[-1] != 1:
            raise ValueError(f"Expect 1 for last component, got {self._values[-1]}")
        return Vector(*self._values[:-1])

# Important constants
origin = Vector(0, 0, 0)
X = Vector(1, 0, 0)
Y = Vector(0, 1, 0)
Z = Vector(0, 0, 1)
