from cadlib.geometry.matrix import Matrix
from tests.unit_test import TestCase

class TestMatrix(TestCase):
    ####################
    ## Initialization ##
    ####################

    def test_construction(self):
        # Empty
        Matrix()                       # 0x0

        # Construct from lists
        l1 = Matrix([1])                    # 1x1
        l2 = Matrix([1, 2], [3, 4.0])       # 2x2
        l3 = Matrix([1, 2, 3], [4, 5, 6])   # 2x3
        l4 = Matrix([1, 2], [3, 4], [5, 6]) # 3x2

        # Construct from tuples
        t1 = Matrix((1, ))                  # 1x1
        t2 = Matrix((1, 2), (3, 4))         # 2x2
        t3 = Matrix((1, 2, 3), (4, 5, 6))   # 2x3
        t4 = Matrix((1, 2), (3, 4), (5, 6)) # 3x2

        self.assertEqual(t1, l1)
        self.assertEqual(t2, l2)
        self.assertEqual(t3, l3)
        self.assertEqual(t4, l4)

        with self.assertRaises(ValueError): Matrix([], [])
        with self.assertRaises(ValueError): Matrix([1, 2], [3, 4, 5])
        with self.assertRaises(ValueError): Matrix([1, 2, 3], [4, 5])
        with self.assertRaises(TypeError): Matrix(1)
        with self.assertRaises(TypeError): Matrix([1, 2], [3, "x"])
        with self.assertRaises(TypeError): Matrix([1, 2], [3, None])

    def test_construction_immutability(self):
        values = [[1, 2], [3, 4]]
        m = Matrix(*values)
        self.assertEqual(m.row_values, [[1, 2], [3, 4]])
        values[0][0] = 0
        values[1] = [0, 0]
        self.assertEqual(m.row_values, [[1, 2], [3, 4]])

    def test_zero(self):
        self.assertEqual(Matrix.zero(0), Matrix())
        self.assertEqual(Matrix.zero(1), Matrix([0]))
        self.assertEqual(Matrix.zero(2), Matrix([0, 0], [0, 0]))
        self.assertEqual(Matrix.zero(3), Matrix([0, 0, 0], [0, 0, 0], [0, 0,0]))

    def test_identity(self):
        self.assertEqual(Matrix.identity(0), Matrix())
        self.assertEqual(Matrix.identity(1), Matrix([1]))
        self.assertEqual(Matrix.identity(2), Matrix([1, 0], [0, 1]))
        self.assertEqual(Matrix.identity(3), Matrix([1, 0, 0], [0, 1, 0], [0, 0,1]))


    ################
    ## Properties ##
    ################

    def test_dimensions(self):
        m = Matrix([1, 2, 3], [4, 5, 6])   # 2x3
        self.assertEqual(m.row_count, 2)
        self.assertEqual(m.column_count, 3)
        self.assertEqual(m.dimensions, (2, 3))

        self.assertEqual(Matrix().dimensions, (0, 0))

    def test_item(self):
        m = Matrix([1, 2, 3], [4, 5, 6])   # 2x3

        # Positive index
        self.assertEqual(m[0, 0], 1)
        self.assertEqual(m[0, 1], 2)
        self.assertEqual(m[0, 2], 3)
        self.assertEqual(m[1, 0], 4)
        self.assertEqual(m[1, 1], 5)
        self.assertEqual(m[1, 2], 6)

        # Negative index counts from the end
        self.assertEqual(m[0, -1], 3)
        self.assertEqual(m[-1, 0], 4)
        self.assertEqual(m[-1, -1], 6)

        # Index out of range
        with self.assertRaises(IndexError): m[0, 3]
        with self.assertRaises(IndexError): m[2, 0]

        # Single index
        with self.assertRaises(TypeError): m[0]

    def test_vectors(self):
        m = Matrix([1, 2, 3], [4, 5, 6])   # 2x3

        self.assertEqual(m.row_values, [[1, 2, 3], [4, 5, 6]])
        self.assertEqual(m.column_values, [[1, 4], [2, 5], [3, 6]])

        self.assertEqual(Matrix().row_values   , [])
        self.assertEqual(Matrix().column_values, [])

    def test_vectors_immutability(self):
        m = Matrix([1, 2], [3, 4])

        self.assertEqual(m.row_values, [[1, 2], [3, 4]])
        rows = m.row_values
        rows[0][0] = 0
        rows[1] = [0, 0]
        self.assertEqual(m.row_values, [[1, 2], [3, 4]])

        self.assertEqual(m.column_values, [[1, 3], [2, 4]])
        columns = m.column_values
        columns[0][0] = 0
        rows[1] = [0, 0]
        self.assertEqual(m.column_values, [[1, 3], [2, 4]])


    #########
    ## I/O ##
    #########

    def test_repr(self):
        m = Matrix([1, 2, 3], [4, 5, 0])   # 2x3

        self.assertEqual(repr(m), "Matrix([1, 2, 3], [4, 5, 0])")


    ################
    ## Arithmetic ##
    ################

    def test_transpose(self):
        m = Matrix([1, 2, 3], [4, 5, 0])   # 2x3

        self.assertEqual(m.transpose(), Matrix([1, 4], [2, 5], [3, 0]))
        self.assertEqual(m.transpose().transpose(), m)

    def test_equality(self):
        m1 = Matrix([1, 2], [3, 4])
        m2 = Matrix([1, 2], [3, 4])
        m3 = Matrix([1, 2], [3, 5])

        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)
        self.assertNotEqual(m1, None)
        self.assertNotEqual(m1, 1)
        self.assertNotEqual(m1, "one")
        self.assertNotEqual(m1, [[1, 2], [3, 4]])

    def test_negation(self):
        m1 = Matrix([1, 2, 3], [4, 5, 0])   # 2x3
        self.assertEqual(-m1, Matrix([-1, -2, -3], [-4, -5, 0]))

    def test_matrix_addition(self):
        m1 = Matrix([1, 2, 3], [4, 5, 6])   # 2x3
        m2 = Matrix([7, 8, 9], [-1, -2, 0])   # 2x3
        m3 = Matrix([7, 8], [-1, -2])   # 2x3

        self.assertEqual(m1 + m2, Matrix([8, 10, 12], [3, 3, 6]))
        with self.assertRaises(ValueError): m1 + m3

    def test_matrix_subtraction(self):
        m1 = Matrix([1, 2, 3], [4, 5, 6])   # 2x3
        m2 = Matrix([7, 8, 9], [-1, -2, 0])   # 2x3
        m3 = Matrix([7, 8], [-1, -2])   # 2x3

        self.assertEqual(m1 - m2, Matrix([-6, -6, -6], [5, 7, 6]))
        with self.assertRaises(ValueError): m1 - m3

    def test_invalid_addition_subtraction(self):
        m = Matrix([1, 2, 3], [4, 5, 6])   # 2x3

        for invalid in [0, None, ""]:
            with self.assertRaises(TypeError): m + invalid
            with self.assertRaises(TypeError): invalid + m
            with self.assertRaises(TypeError): m - invalid
            with self.assertRaises(TypeError): invalid - m

    def test_scalar_multiplication(self):
        m = Matrix([1, 2, 3], [4, 5, 6])   # 2x3

        # Matrix * Number
        self.assertEqual(m * 1  , m)
        self.assertEqual(m * 2  , Matrix([2, 4, 6], [8, 10, 12]))
        self.assertEqual(m * 0.5, Matrix([0.5, 1, 1.5], [2, 2.5, 3]))
        self.assertEqual(m * 0  , Matrix([0, 0, 0], [0, 0, 0]))

        # Number * Matrix
        self.assertEqual(1   * m, m)
        self.assertEqual(2   * m, Matrix([2, 4, 6], [8, 10, 12]))
        self.assertEqual(0.5 * m, Matrix([0.5, 1, 1.5], [2, 2.5, 3]))
        self.assertEqual(0   * m, Matrix([0, 0, 0], [0, 0, 0]))

    def test_matrix_multiplication(self):
        m = Matrix([1, 2], [3, 4])

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
        self.assertEqual(Matrix([1, 0], [0, -1]) * Matrix([1, 2], [3, 4]), Matrix([1, 2], [-3, -4])) # Invert y
        self.assertEqual(Matrix([1, 2], [3, 4]) * Matrix([1, 0], [0, -1]), Matrix([1, -2], [3, -4]))
        self.assertEqual(Matrix([0, -1], [1, 0]) * Matrix([1, 2], [3, 4]), Matrix([-3, -4], [1, 2])) # Rotate by 90 degrees
        self.assertEqual(Matrix([1, 2], [3, 4]) * Matrix([5, 6], [7, 8]), Matrix([19, 22], [43, 50])) # Arbitrary

        # 2x3 * 3x2
        self.assertEqual(Matrix([10, 11, 12], [13, 14, 15]) *
                         Matrix([16, 17], [18, 19], [20, 21]),
                         Matrix([598, 631], [760, 802]))

        # 3x2 * 2x3
        self.assertEqual(Matrix([10, 11], [12, 13], [14, 15]) *
                         Matrix([16, 17, 18], [19, 20, 21]),
                         Matrix([369, 390, 411], [439, 464, 489], [509, 538, 567]))

        # 3x3
        self.assertEqual(Matrix([10, 11, 12], [13, 14, 15], [16, 17, 18]) *
                         Matrix([19, 20, 21], [22, 23, 24], [25, 26, 27]),
                         Matrix([732, 765, 798], [930, 972, 1014], [1128, 1179, 1230]))

        # Dimensions mismatch
        with self.assertRaises(ValueError): Matrix.identity(3) * m
        with self.assertRaises(ValueError): m * Matrix.identity(3)
        with self.assertRaises(ValueError): Matrix([16, 17, 18], [19, 20, 21]) * Matrix([10, 11], [12, 13])

    def test_scalar_division(self):
        m = Matrix([1, 2, 3], [4, 5, 6])   # 2x3

        # Matrix / Number
        self.assertEqual(m / 1  , m)
        self.assertEqual(m / 2  , Matrix([0.5, 1, 1.5], [2, 2.5, 3]))
        self.assertEqual(m / 0.5, Matrix([2, 4, 6], [8, 10, 12]))

        # Matrix / 0 is invalid
        with self.assertRaises(ZeroDivisionError): m / 0

        # Number / Matrix is undefined
        with self.assertRaises(TypeError): 1 / m

    def test_invalid_multiplication_division(self):
        m = Matrix([1, 2, 3], [4, 5, 6])   # 2x3

        for invalid in [None, ""]:
            with self.assertRaises(TypeError): m * invalid
            with self.assertRaises(TypeError): invalid * m
            with self.assertRaises(TypeError): m / invalid
            with self.assertRaises(TypeError): invalid / m
