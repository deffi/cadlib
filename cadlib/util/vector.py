import math
from numbers import Number
from cadlib.util.table import Table
from cadlib.util import Matrix


def to_vector(value, label = None, required_length = None):
    if required_length is not None and len(value) != required_length:
        raise ValueError("Invalid length for {}, must be {}".format(label, required_length))

    if isinstance(value, Vector):
        return value
    elif isinstance(value, (list, tuple)):
        return Vector(*value)
    else:
        raise TypeError("Invalid vector: {}".format(label, value))


class Vector:
    '''
    Note that __len__, like the dimensions property, returns the number of elements. The length property returns the
    vector's magnitude.

    Despite mathematical considerations, Vector does not inherit Matrix because its interface is different:
      * Vectors are subscripted with a single value (vector[i] rather than matrix[i, 0])
      * The size of a vector is a single value (vector.dimensions == 3 rather than matrix.dimensions == (3, 0))
    Besides, since arithmetic operations such as Vector+Vector and Matrix*Vector are supposed to return a vector, the
    corresponding methods would have to be overridden to convert the result to a vector. Finally, calling
    .transpose().transpose() on a Vector would change the type to Matrix.
    '''

    ####################
    ## Initialization ##
    ####################

    def __init__(self, *values):
        for value in values:
            if not isinstance(value, Number):
                raise TypeError("Vectors must consist of numeric values")

        # TODO convert all to float
        self._values = list(values)

    @classmethod
    def zero(cls, size):
        values = [0] * size
        return cls(*values)


    ################
    ## Properties ##
    ################

    @property
    def values(self):
        # Make a copy so the caller can't change our values
        return list(self._values)

    @property
    def dimensions(self):
        return len(self._values)

    def __len__(self):
        return len(self._values)

    def __getitem__(self, index):
        return self._values[index]

    ################
    ## Comparison ##
    ################

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False

        return self._values == other._values


    ################
    ## Arithmetic ##
    ################

    def __add__(self, other):
        if isinstance(other, Vector):
            if other.dimensions != self.dimensions:
                raise ValueError("Dimensions don't match")
            else:
                return Vector(*[x1 + x2 for x1, x2 in zip(self._values, other._values)])
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector):
            return self + (-other)
        else:
            return NotImplemented

    def __neg__(self):
        return (-1) * self

    def __mul__(self, other):
        if isinstance(other, Number):
            return Vector(*[x * other for x in self._values])
        else:
            return NotImplemented

    def __rmul__(self, other):
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
        if isinstance(other, Number):
            return Vector(*[x / other for x in self._values])
        else:
            return NotImplemented

    def dot(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Dot product is only defined for vectors")

        if other.dimensions != self.dimensions:
            raise ValueError("Vectors must have the same dimensions")

        return sum(a * b for a, b in zip(self._values, other._values))

    def cross(self, other):
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
        from cadlib.util import degree

        # While mathematically correct, this performs poorly due to rounding errors:
        #     Vector(2, 3.4).angle(Vector(2, 3.4)) is only equal to 0.0 within 5 decimal places
        #     Vector(1, 1, 1).angle(Vector(-1, -1, -1)) fails because the argument of acos is -1.0000000000000002.
        # return math.acos(self.dot(other) / (self.length * other.length)) / degree

        # This is better
        # Source: https://math.stackexchange.com/questions/1143354/numerically-stable-method-for-angle-between-3d-vectors
        u = self
        v = other
        return 2 * math.atan2((v.length*u - u.length*v).length, (v.length*u + u.length*v).length) / degree

    @property
    def length_squared(self):
        return sum(x ** 2 for x in self._values)

    @property
    def length(self):
        return math.sqrt(self.length_squared)

    def normalized(self):
        return self / self.length

    def normal(self):
        # Invalid operation for empty, one-dimensional, and zero-length vectors
        if len(self) == 0:           raise ValueError("Empty vectors don't have normals")
        if len(self) == 1:           raise ValueError("One-dimensional vectors don't have normals")
        if self.length_squared == 0: raise ValueError("Zero vectors don't have normals")

        # Algorithm: find any two values, at least one of which is not zero. Swap them and invert one of them. Set all
        # other values to zero. Note that it is permissible for the inverted value to be zero.

        # Find the index of the first non-zero value and the index of following value (wrapping around if necessary).
        i1 = next((index for index, value in enumerate(self._values) if value != 0), None)
        i2 = (i1 + 1) % len(self._values)

        # Create a list of zeros. Copy the values from index i1 and i2, inverting one of them.
        values = [0] * len(self._values)
        values[i1] = -self._values[i2]
        values[i2] =  self._values[i1]

        # Create a vector from the values
        return Vector(*values)


    #########
    ## I/O ##
    #########

    def __str__(self):
        return Table([[v] for v in self._values]).format(alignment="r")

    def __repr__(self):
        return "Vector({})".format(", ".join(str(value) for value in self._values))


X = Vector(1, 0, 0)
Y = Vector(0, 1, 0)
Z = Vector(0, 0, 1)

if __name__ == "__main__":
    print(Vector())
    print(Vector(1, 2, 3))