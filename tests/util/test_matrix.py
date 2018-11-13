from cadlib.util.matrix import Matrix
from tests.unit_test import TestCase
from cadlib.util.vector import Vector, X, Y, Z

class TestMatrix(TestCase):
    ####################
    ## Initialization ##
    ####################

    def test_construction(self):
        # Empty
        self.assertEqual(Matrix().row_values, [])  # 0x0

        # Rows - different dimensions
        self.assertEqual(Matrix(rows = [[1]                   ]).row_values, [[1]                   ])
        self.assertEqual(Matrix(rows = [[1, 2], [3, 4]        ]).row_values, [[1, 2], [3, 4]        ])
        self.assertEqual(Matrix(rows = [[1, 2, 3], [4, 5, 6]  ]).row_values, [[1, 2, 3], [4, 5, 6]  ])
        self.assertEqual(Matrix(rows = [[1, 2], [3, 4], [5, 6]]).row_values, [[1, 2], [3, 4], [5, 6]])

        # Columns - different dimensions
        self.assertEqual(Matrix(columns = [[1]                   ]).row_values, [[1]                   ])
        self.assertEqual(Matrix(columns = [[1, 2], [3, 4]        ]).row_values, [[1, 3], [2, 4]        ])
        self.assertEqual(Matrix(columns = [[1, 2, 3], [4, 5, 6]  ]).row_values, [[1, 4], [2, 5], [3, 6]])
        self.assertEqual(Matrix(columns = [[1, 2], [3, 4], [5, 6]]).row_values, [[1, 3, 5], [2, 4, 6]  ])

        # Rows - different types
        expected = [[1, 2, 3], [4, 5, 6]]
        # Lists/tuples
        self.assertEqual(Matrix(rows = [[1, 2, 3], [4, 5, 6]]).row_values, expected)
        self.assertEqual(Matrix(rows = [(1, 2, 3), (4, 5, 6)]).row_values, expected)
        self.assertEqual(Matrix(rows = ([1, 2, 3], [4, 5, 6])).row_values, expected)
        self.assertEqual(Matrix(rows = ((1, 2, 3), (4, 5, 6))).row_values, expected)
        # Generators
        self.assertEqual(Matrix(rows = [range(1, 4), range(4, 7)]).row_values, expected)
        r1 = [1, 2, 3]
        r2 = [4, 5, 6]
        self.assertEqual(Matrix(rows = (row for row in [r1, r2])).row_values, expected)
        # Vectors
        r1 = Vector(1, 2, 3)
        r2 = Vector(4, 5, 6)
        self.assertEqual(Matrix(rows = [r1, r2]).row_values, expected)

        # Columns - different types
        expected = [[1, 4], [2, 5], [3, 6]]
        # Lists/tuples
        self.assertEqual(Matrix(columns = [[1, 2, 3], [4, 5, 6]]).row_values, expected)
        self.assertEqual(Matrix(columns = [(1, 2, 3), (4, 5, 6)]).row_values, expected)
        self.assertEqual(Matrix(columns = ([1, 2, 3], [4, 5, 6])).row_values, expected)
        self.assertEqual(Matrix(columns = ((1, 2, 3), (4, 5, 6))).row_values, expected)
        # Generators
        self.assertEqual(Matrix(columns = [range(1, 4), range(4, 7)]).row_values, expected)
        c1 = [1, 2, 3]
        c2 = [4, 5, 6]
        self.assertEqual(Matrix(columns = (column for column in [c1, c2])).row_values, expected)
        # Vectors
        c1 = Vector(1, 2, 3)
        c2 = Vector(4, 5, 6)
        self.assertEqual(Matrix(columns = [c1, c2]).row_values, expected)

    def test_construction_invalid(self):
        # Rows and columns
        with self.assertRaises(ValueError): Matrix(rows = [[1]], columns = [[1]])

        # Rows - invalid
        with self.assertRaises(ValueError): Matrix(rows = [[]    , []       ])
        with self.assertRaises(ValueError): Matrix(rows = [[1, 2], []       ])
        with self.assertRaises(ValueError): Matrix(rows = [[1, 2], [3, 4, 5]])
        with self.assertRaises(TypeError): Matrix(rows = 1)
        with self.assertRaises(TypeError): Matrix(rows = [1])
        with self.assertRaises(TypeError): Matrix(rows = [[1, 2], [3, "x"]])
        with self.assertRaises(TypeError): Matrix(rows = [[1, 2], [3, None]])

        # Columns - invalid
        with self.assertRaises(ValueError): Matrix(columns = [[]    , []       ])
        with self.assertRaises(ValueError): Matrix(columns = [[1, 2], []       ])
        with self.assertRaises(ValueError): Matrix(columns = [[1, 2], [3, 4, 5]])
        with self.assertRaises(TypeError): Matrix(columns = 1)
        with self.assertRaises(TypeError): Matrix(columns = [1])
        with self.assertRaises(TypeError): Matrix(columns = [[1, 2], [3, "x"]])
        with self.assertRaises(TypeError): Matrix(columns = [[1, 2], [3, None]])

    def test_immutability(self):
        # Create a matrix from a list of lists and verify its row values
        values = [[1, 2], [3, 4]]
        m = Matrix(rows = values)
        self.assertEqual(m.row_values, [[1, 2], [3, 4]])

        # Change one item of the list of lists and one item of another of its items and verify that
        # the matrix values are unaffected
        values[0][0] = 0
        values[1] = [0, 0]
        self.assertEqual(m.row_values, [[1, 2], [3, 4]])

    def test_zero(self):
        self.assertEqual(Matrix.zero(0).row_values, [])
        self.assertEqual(Matrix.zero(1).row_values, [[0]])
        self.assertEqual(Matrix.zero(2).row_values, [[0, 0], [0, 0]])
        self.assertEqual(Matrix.zero(3).row_values, [[0, 0, 0], [0, 0, 0], [0, 0,0]])

    def test_identity(self):
        self.assertEqual(Matrix.identity(0).row_values, [])
        self.assertEqual(Matrix.identity(1).row_values, [[1]])
        self.assertEqual(Matrix.identity(2).row_values, [[1, 0], [0, 1]])
        self.assertEqual(Matrix.identity(3).row_values, [[1, 0, 0], [0, 1, 0], [0, 0,1]])

    def test_from_rows(self):
        # Valid
        self.assertEqual(Matrix.from_rows().row_values, [])
        self.assertEqual(Matrix.from_rows([1, 2, 3]).row_values, [[1, 2, 3]])
        self.assertEqual(Matrix.from_rows([1, 2, 3], [4, 5, 6]).row_values, [[1, 2, 3], [4, 5, 6]])

        # Invalid
        with self.assertRaises(ValueError): Matrix.from_rows([1, 2], [3, 4, 5])

        # Wrong type
        with self.assertRaises(TypeError): Matrix.from_rows(1)
        with self.assertRaises(TypeError): Matrix.from_rows(1, 2)

    def test_from_columns(self):
        # Valid
        self.assertEqual(Matrix.from_columns().row_values, [])
        self.assertEqual(Matrix.from_columns([1, 2, 3]).row_values, [[1], [2], [3]])
        self.assertEqual(Matrix.from_columns([1, 2, 3], [4, 5, 6]).row_values, [[1, 4], [2, 5], [3, 6]])

        # Invalid
        with self.assertRaises(ValueError): Matrix.from_columns([1, 2], [3, 4, 5])

        # Wrong type
        with self.assertRaises(TypeError): Matrix.from_columns(1)
        with self.assertRaises(TypeError): Matrix.from_columns(1, 2)


    ################
    ## Properties ##
    ################

    def test_equality(self):
        m1 = Matrix.from_rows([1, 2], [3, 4])
        m2 = Matrix.from_rows([1, 2], [3, 4])
        m3 = Matrix.from_rows([1, 2], [3, 5])

        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)
        self.assertNotEqual(m1, None)
        self.assertNotEqual(m1, 1)
        self.assertNotEqual(m1, "one")
        self.assertNotEqual(m1, [[1, 2], [3, 4]])

    def test_dimensions(self):
        m = Matrix()
        self.assertEqual(m.row_count, 0)
        self.assertEqual(m.column_count, 0)
        self.assertEqual(m.dimensions, (0, 0))

        m = Matrix.from_rows([1, 2, 3], [4, 5, 6])
        self.assertEqual(m.row_count, 2)
        self.assertEqual(m.column_count, 3)
        self.assertEqual(m.dimensions, (2, 3))

    def test_item(self):
        m = Matrix.from_rows([1, 2, 3], [4, 5, 6])

        # Positive index
        self.assertEqual(m[0, 0], 1)
        self.assertEqual(m[0, 1], 2)
        self.assertEqual(m[0, 2], 3)
        self.assertEqual(m[1, 0], 4)
        self.assertEqual(m[1, 1], 5)
        self.assertEqual(m[1, 2], 6)

        # Negative index counts from the end
        self.assertEqual(m[-2, -3], 1)
        self.assertEqual(m[-2, -2], 2)
        self.assertEqual(m[-2, -1], 3)
        self.assertEqual(m[-1, -3], 4)
        self.assertEqual(m[-1, -2], 5)
        self.assertEqual(m[-1, -1], 6)

        # Index out of range
        with self.assertRaises(IndexError): m[0, 3]
        with self.assertRaises(IndexError): m[2, 0]
        with self.assertRaises(IndexError): m[-3, 0]
        with self.assertRaises(IndexError): m[0, -4]

        # Error: single index
        with self.assertRaises(TypeError): m[0]

    def test_row_values_and_column_values(self):
        m = Matrix.from_rows([1, 2, 3], [4, 5, 6])

        self.assertEqual(m.row_values   , [[1, 2, 3], [4, 5, 6]])
        self.assertEqual(m.column_values, [[1, 4], [2, 5], [3, 6]])

        self.assertEqual(Matrix().row_values   , [])
        self.assertEqual(Matrix().column_values, [])


    #########
    ## I/O ##
    #########

    def test_repr(self):
        m = "Matrix(rows=[[1, 2, 3], [4, 5, 0]])"
        self.assertEqual(repr(eval(m)), m)

    def test_format(self):
        m = Matrix(rows=[[1, 2, 3], [-4, 5, 666]])
        self.assertLines(m.format(), [
            " 1 2   3",
            "-4 5 666",
        ])


    ################
    ## Arithmetic ##
    ################

    def test_transpose(self):
        m = Matrix.from_rows([1, 2, 3], [4, 5, 6])

        self.assertEqual(m.row_values                        , [[1, 2, 3], [4, 5, 6]])
        self.assertEqual(m.transpose().row_values            , [[1, 4], [2, 5], [3, 6]])
        self.assertEqual(m.transpose().transpose().row_values, [[1, 2, 3], [4, 5, 6]])

    def test_negation(self):
        m1 = Matrix.from_rows([1, 2, 3], [4, 5, 0])
        m2 = Matrix.from_rows([-1, -2, -3], [-4, -5, 0])
        self.assertEqual(-m1, m2)

    def test_matrix_addition(self):
        # Regular addition
        m1 = Matrix.from_rows([1, 2, 3], [4, 5, 6])
        m2 = Matrix.from_rows([7, 8, 9], [-1, -2, 0])
        m3 = Matrix.from_rows([8, 10, 12], [3, 3, 6])
        self.assertEqual(m1 + m2, m3)

        # Size mismatch
        m4 = Matrix.from_rows([1, 2], [3, 4], [5, 6])
        with self.assertRaises(ValueError): m1 + m4

    def test_matrix_subtraction(self):
        # Regular addition
        m1 = Matrix.from_rows([1, 2, 3], [4, 5, 6])
        m2 = Matrix.from_rows([7, 8, 9], [-1, -2, 0])
        m3 = Matrix.from_rows([-6, -6, -6], [5, 7, 6])
        self.assertEqual(m1 - m2, m3)

        # Size mismatch
        m4 = Matrix.from_rows([1, 2], [3, 4], [5, 6])
        with self.assertRaises(ValueError): m1 - m4

    def test_scalar_multiplication(self):
        m = Matrix.from_rows([1, 2, 3], [4, 5, 6])

        # Matrix * Number
        self.assertEqual(m * 1  , m)
        self.assertEqual(m * 2  , Matrix.from_rows([2, 4, 6], [8, 10, 12]))
        self.assertEqual(m * 0.5, Matrix.from_rows([0.5, 1, 1.5], [2, 2.5, 3]))
        self.assertEqual(m * 0  , Matrix.from_rows([0, 0, 0], [0, 0, 0]))

        # Number * Matrix
        self.assertEqual(1   * m, m)
        self.assertEqual(2   * m, Matrix.from_rows([2, 4, 6], [8, 10, 12]))
        self.assertEqual(0.5 * m, Matrix.from_rows([0.5, 1, 1.5], [2, 2.5, 3]))
        self.assertEqual(0   * m, Matrix.from_rows([0, 0, 0], [0, 0, 0]))

    def test_scalar_division(self):
        m = Matrix.from_rows([1, 2, 3], [4, 5, 6])

        # Matrix / Number
        self.assertEqual(m / 1  , m)
        self.assertEqual(m / 2  , Matrix.from_rows([0.5, 1, 1.5], [2, 2.5, 3]))
        self.assertEqual(m / 0.5, Matrix.from_rows([2, 4, 6], [8, 10, 12]))

        # Matrix / 0 is invalid
        with self.assertRaises(ZeroDivisionError): m / 0

        # Number / Matrix is undefined
        with self.assertRaises(TypeError): 1 / m

    def test_matrix_multiplication(self):
        m = Matrix.from_rows([1, 2], [3, 4])

        # Left and right multiplication with identity
        self.assertEqual(Matrix.identity(2) * m, m)
        self.assertEqual(m * Matrix.identity(2), m)

        # Left and right multiplication with zero
        self.assertEqual(Matrix.zero(2) * m, Matrix.zero(2))
        self.assertEqual(m * Matrix.zero(2), Matrix.zero(2))

        # Scaling by multiplication with scaled identity
        self.assertEqual((5 * Matrix.identity(2)) * m, 5 * m)
        self.assertEqual(m * (5 * Matrix.identity(2)), 5 * m)

        # Multiplications
        m1 = Matrix.from_rows([1, 2], [3, 4])
        m2 = Matrix.from_rows([5, 6], [7, 8])
        m3 = Matrix.from_rows([19, 22], [43, 50])
        flip = Matrix.from_rows([1, 0], [0, -1])
        turn = Matrix.from_rows([0, -1], [1, 0])

        self.assertEqual(flip * m1  , Matrix.from_rows([1, 2], [-3, -4])) # Invert y
        self.assertEqual(m1   * flip, Matrix.from_rows([1, -2], [3, -4]))
        self.assertEqual(turn * m1  , Matrix.from_rows([-3, -4], [1, 2])) # Rotate by 90 degrees
        self.assertEqual(m1   * m2  , m3) # Arbitrary

        # 2x3 * 3x2
        self.assertEqual(Matrix.from_rows([10, 11, 12], [13, 14, 15]) *
                         Matrix.from_rows([16, 17], [18, 19], [20, 21]),
                         Matrix.from_rows([598, 631], [760, 802]))

        # 3x2 * 2x3
        self.assertEqual(Matrix.from_rows([10, 11], [12, 13], [14, 15]) *
                         Matrix.from_rows([16, 17, 18], [19, 20, 21]),
                         Matrix.from_rows([369, 390, 411], [439, 464, 489], [509, 538, 567]))

        # 3x3
        self.assertEqual(Matrix.from_rows([10, 11, 12], [13, 14, 15], [16, 17, 18]) *
                         Matrix.from_rows([19, 20, 21], [22, 23, 24], [25, 26, 27]),
                         Matrix.from_rows([732, 765, 798], [930, 972, 1014], [1128, 1179, 1230]))

        # Dimensions mismatch
        with self.assertRaises(ValueError): Matrix.identity(3) * m
        with self.assertRaises(ValueError): m * Matrix.identity(3)
        with self.assertRaises(ValueError): (Matrix.from_rows([16, 17, 18], [19, 20, 21]) *
                                             Matrix.from_rows([10, 11], [12, 13]))

    def test_mixed_arithmetic(self):
        m1 = Matrix.from_rows([1, 2, 3], [4, 5, 6])
        m2 = Matrix.from_rows([7, 8, 9], [-1, -2, 0])
        self.assertEqual(m1 + (-m2), m1 - m2)
        self.assertEqual(m1 - (-m2), m1 + m2)

    def test_invalid_arithmetic(self):
        m = Matrix.from_rows([1, 2, 3], [4, 5, 6])

        for invalid in [0, None, ""]:
            with self.assertRaises(TypeError): m + invalid
            with self.assertRaises(TypeError): invalid + m
            with self.assertRaises(TypeError): m - invalid
            with self.assertRaises(TypeError): invalid - m

        for invalid in [None, ""]:
            with self.assertRaises(TypeError): m * invalid
            with self.assertRaises(TypeError): invalid * m
            with self.assertRaises(TypeError): m / invalid
            with self.assertRaises(TypeError): invalid / m
