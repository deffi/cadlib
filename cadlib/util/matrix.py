from numbers import Number
from cadlib.util.table import Table

class Matrix:
    ####################
    ## Initialization ##
    ####################

    def __init__(self, rows = None, columns = None):
        self._row_count    = 0
        self._column_count = 0
        self._rows = []

        if rows is not None and columns is not None:
            raise ValueError("rows and columns cannot be specified together")

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

        for row in self._rows:
            # Make sure that all values are numeric
            for value in row:
                if not isinstance(value, Number):
                    raise TypeError("Matrices must consist of numeric values")

    @classmethod
    def from_rows(cls, *rows):
        return cls(rows = rows)

    @classmethod
    def from_columns(cls, *columns):
        return cls(columns = columns)

    @classmethod
    def identity(cls, size):
        rows = []
        for i in range(size):
            row = [0] * size
            row[i] = 1
            rows.append(row)

        return cls(rows = rows)

    @classmethod
    def zero(cls, size):
        rows = [[0] * size for i in range(size)]
        return cls(rows = rows)


    ################
    ## Properties ##
    ################

    @property
    def row_count(self):
        return self._row_count

    @property
    def column_count(self):
        return self._column_count

    @property
    def dimensions(self):
        return (self._row_count, self._column_count)

    def __getitem__(self, item):
        row = item[0]
        column = item[1]
        return self._rows[row][column]

    @property
    def row_values(self):
        # Make a copy so the caller can't change our values
        return list(list(row) for row in self._rows)

    @property
    def column_values(self):
        if len(self._rows) == 0:
            return []
        else:
            # Make a copy so the caller can't change our values
            return list(list(column) for column in zip(*self._rows))


    ################
    ## Comparison ##
    ################

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False

        return self._rows == other._rows


    ################
    ## Arithmetic ##
    ################

    def transpose(self):
        return Matrix(columns = self._rows)

    def __add__(self, other):
        if isinstance(other, Matrix):
            if other.dimensions != self.dimensions:
                raise ValueError("Dimensions don't match")
            else:
                return Matrix.from_rows(*[[x1 + x2 for x1, x2 in zip(r1, r2)] for r1, r2 in zip(self._rows, other._rows)])
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Matrix):
            return self + (-other)
        else:
            return NotImplemented

    def __neg__(self):
        return (-1) * self

    def __mul__(self, other):
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
        if isinstance(other, Number):
            return Matrix(rows = [[x / other for x in row] for row in self._rows])
        else:
            return NotImplemented


    #########
    ## I/O ##
    #########

    def __repr__(self):
        #return "Matrix(rows={})".format(", ".join((str(row) for row in self._rows)))
        return f"Matrix(rows={self.row_values})"

    def format(self):
        return Table(self._rows).format(alignment="r")
