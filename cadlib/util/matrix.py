from numbers import Number
from cadlib.util.table import Table

class Matrix:
    """An immutable matrix with basic arithmetic."""

    ####################
    ## Initialization ##
    ####################

    def __init__(self, rows = None, columns = None):
        """Create a matrix from either rows or columns

        The specified rows or columns must be non-empty iterables of non-empty
        iterables with identical length and numeric values. Either rows or
        columns, but not both, can be specified. If neither rows nor columns are
        specified, the resulting matrix will be empty.

        The matrix is not required to be square.
        """
        self._row_count    = 0
        self._column_count = 0
        self._rows = []

        if rows is not None and columns is not None:
            raise TypeError("rows and columns cannot be specified together")

        elif rows is not None:
            rows = list(rows)
            if len(rows) > 0:
                self._row_count    = len(rows)
                self._column_count = len(rows[0])

                # Check the rows
                for row in rows:
                    if len(row) == 0                 : raise ValueError("rows can't be empty")
                    if len(row) != self._column_count: raise ValueError("rows must have the same size")

                # Convert to list of lists
                self._rows = [list(row) for row in rows]

        elif columns is not None:
            columns = list(columns)
            if len(columns) > 0:
                self._column_count = len(columns)
                self._row_count    = len(columns[0])

                # Check the columns
                for column in columns:
                    if len(column) == 0              : raise ValueError("columns can't be empty")
                    if len(column) != self._row_count: raise ValueError("columns must have the same size")

                # Convert to list of lists
                self._rows = [list(row) for row in zip(*columns)]

        # TODO error if rows and columns are both None

        for row in self._rows:
            # Make sure that all values are numeric
            for value in row:
                if not isinstance(value, Number):
                    raise TypeError("Matrices must consist of numeric values")

    # TODO remove
    @classmethod
    def from_rows(cls, *rows):
        return cls(rows = rows)

    # TODO remove
    @classmethod
    def from_columns(cls, *columns):
        return cls(columns = columns)

    @classmethod
    def identity(cls, size):
        """Create an identity matrix.

        The created matrix will be square with the specified size, ones on the
        main diagonal, and zeros everywhere else."""

        rows = []
        for i in range(size):
            row = [0] * size
            row[i] = 1
            rows.append(row)

        return cls(rows = rows)

    @classmethod
    def zero(cls, size):
        """Create a square zero matrix."""

        rows = [[0] * size for i in range(size)]
        return cls(rows = rows)


    ################
    ## Properties ##
    ################

    @property
    def row_count(self):
        """Return the number of rows in the matrix."""
        return self._row_count

    @property
    def column_count(self):
        """Return the number of columns in the matrix."""
        return self._column_count

    @property
    def dimensions(self):
        """Return the dimensions as a tuple of (rows, columns)."""
        return (self._row_count, self._column_count)

    def __getitem__(self, item):
        """Return the value at the position specified by (row, column)"""
        row = item[0]
        column = item[1]
        return self._rows[row][column]

    @property
    def row_values(self):
        """Return a copy of the matrix values as list of lists, row-wise."""

        # Make a copy so the caller can't change our values
        return list(list(row) for row in self._rows)

    @property
    def column_values(self):
        """Return a copy of the matrix values as list of lists, column-wise."""

        if len(self._rows) == 0:
            return []
        else:
            # Make a copy so the caller can't change our values
            return list(list(column) for column in zip(*self._rows))


    ################
    ## Comparison ##
    ################

    def __eq__(self, other):
        """Two matrices are identical if all of their values are identical."""
        return (isinstance(other, Matrix)
            and self._rows == other._rows)


    ################
    ## Arithmetic ##
    ################

    def transpose(self):
        """Create a new matrix that is this matrix transposed"""
        return Matrix(columns = self._rows)

    def __add__(self, other):
        """Matrices are added element-wise. The dimensions must be identical."""

        if isinstance(other, Matrix):
            if other.dimensions != self.dimensions:
                raise ValueError("Dimension mismatch: {} + {}".format(self.dimensions, other.dimensions))
            else:
                return Matrix.from_rows(*[[x1 + x2 for x1, x2 in zip(r1, r2)] for r1, r2 in zip(self._rows, other._rows)])
        else:
            return NotImplemented

    def __sub__(self, other):
        """Matrices are subtracted element-wise. The dimensions must be identical."""
        if isinstance(other, Matrix):
            return self + (-other)
        else:
            return NotImplemented

    def __neg__(self):
        """Matrices are negated by scalar multiplication with -1."""
        return (-1) * self

    def __mul__(self, other):
        """Matrices can be multiplied with scalars or other matrices.

        For matrix multiplication, the dimensions of the matrices must be
        compatible.

        Multiplication of Matrix and Vector is implemented in Vector.__rmul__.
        """
        if isinstance(other, Number):
            return Matrix(rows = [[x * other for x in row] for row in self._rows])

        elif isinstance(other, Matrix):
            if self.column_count != other.row_count:
                raise ValueError("Dimension mismatch: {} x {}".format(self.dimensions, other.dimensions))

            rows = [[sum(x1 * x2 for x1, x2 in zip(row, column)) for column in zip(*other._rows)] for row in self._rows]

            return Matrix(rows = rows)

        else:
            return NotImplemented

    def __rmul__(self, other):
        """Reverse multiplication is only relevant for scalars."""

        if isinstance(other, Number):
            return self.__mul__(other)
        else:
            # Multiplying Matrix with anything but a number is not commutative.
            # Note that for Vector*Matrix, Vector.__mul__ returns NotImplemented and this method (Matrix.__rmul__) is
            # called. We *might* get away with calling Matrix.__mul__ in this case, because that method returns
            # NotImplemented  to defer to Vector.__rmul__, but it would also be possible for Matrix.__mul__ to *call*
            # Vector.__rmul__ (or perform the multiplication itself), and in this case we would end up with Matrix *
            # Vector, which is not the intended result of TypeError. We therefore return NotImplemented here of other is
            # a Vector.
            raise NotImplemented

    def __truediv__(self, other):
        """Matrix division is only possible with scalars."""
        if isinstance(other, Number):
            return Matrix(rows = [[x / other for x in row] for row in self._rows])
        else:
            return NotImplemented


    #########
    ## I/O ##
    #########

    def __repr__(self):
        # TODO !r?
        return f"Matrix(rows={self.row_values})"

    def format(self):
        """Pretty-print the matrix as a multi-line string."""
        return Table(self._rows).format(alignment="r")
