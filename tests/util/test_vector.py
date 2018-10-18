from cadlib.util.vector import Vector, to_vector, X, Y, Z
from cadlib.util.matrix import Matrix
from tests.unit_test import TestCase

class TestVector(TestCase):
    ####################
    ## Initialization ##
    ####################

    def test_construction(self):
        # Empty
        self.assertEqual(Vector().values, [])

        # Non-empty
        self.assertEqual(Vector(1)      .values, [1])
        self.assertEqual(Vector(1, 2)   .values, [1, 2])
        self.assertEqual(Vector(1, 2, 3).values, [1, 2, 3])

        with self.assertRaises(TypeError): Vector([1, 2])
        with self.assertRaises(TypeError): Vector([1, "2"])
        with self.assertRaises(TypeError): Vector([1, None])

    def test_construction_immutability(self):
        values = [1, 2, 3]
        v = Vector(*values)
        self.assertEqual(v.values, [1, 2, 3])
        values[0] = 0
        self.assertEqual(v.values, [1, 2, 3]) # Still

    def test_zero(self):
        self.assertEqual(Vector.zero(0).values, [])
        self.assertEqual(Vector.zero(1).values, [0])
        self.assertEqual(Vector.zero(2).values, [0, 0])
        self.assertEqual(Vector.zero(3).values, [0, 0, 0])


    ################
    ## Properties ##
    ################

    def test_dimensions(self):
        self.assertEqual(Vector()       .dimensions, 0)
        self.assertEqual(Vector(1)      .dimensions, 1)
        self.assertEqual(Vector(1, 2, 3).dimensions, 3)

    def test_len(self):
        self.assertEqual(len(Vector()       ), 0)
        self.assertEqual(len(Vector(1)      ), 1)
        self.assertEqual(len(Vector(1, 2, 3)), 3)

    def test_is_zero(self):
        self.assertTrue(Vector()       .is_zero)
        self.assertTrue(Vector(0)      .is_zero)
        self.assertTrue(Vector(0, 0)   .is_zero)
        self.assertTrue(Vector(0, 0, 0).is_zero)

        self.assertFalse(Vector(1)      .is_zero)
        self.assertFalse(Vector(1, 0)   .is_zero)
        self.assertFalse(Vector(1, 0, 0).is_zero)

    def test_values(self):
        self.assertEqual(Vector(1, 2, 3).values, [1, 2, 3])

    def test_valuse_immutability(self):
        v = Vector(1, 2, 3)

        self.assertEqual(v.values, [1, 2, 3])
        values = v.values
        values[0] = 0
        self.assertEqual(v.values, [1, 2, 3])

    def test_item(self):
        v = Vector(1, 2, 3)

        # Positive index
        self.assertEqual(v[0], 1)
        self.assertEqual(v[1], 2)
        self.assertEqual(v[2], 3)

        # Negative index counts from the end
        self.assertEqual(v[-1], 3)
        self.assertEqual(v[-2], 2)
        self.assertEqual(v[-3], 1)

        # Index out of range
        with self.assertRaises(IndexError): v[4]

        # Multi-index
        with self.assertRaises(TypeError): v[2, 0]

    def test_iteration(self):
        v = Vector(1, 2, 3)
        self.assertEqual(list(v), [1, 2, 3])


    #########
    ## I/O ##
    #########

    def test_repr(self):
        v = Vector(1, 2, 3)

        self.assertEqual(repr(v), "Vector(1, 2, 3)")


    ################
    ## Arithmetic ##
    ################

    def test_equality(self):
        v = Vector(1, 2, 3)

        self.assertEqual(v, Vector(1, 2, 3))
        self.assertNotEqual(v, Vector(1, 2, 3, 4))
        self.assertNotEqual(v, Vector(1, 2))
        self.assertNotEqual(v, Vector(1, 2, 4))
        self.assertNotEqual(v, None)
        self.assertNotEqual(v, [1, 2, 3])
        self.assertNotEqual(v, (1, 2, 3))
        self.assertNotEqual(v, "one")

    def test_negation(self):
        v = Vector(1, 2, 3)
        self.assertEqual(-v, Vector(-1, -2, -3))

    def test_vector_addition(self):
        self.assertEqual(Vector(1, 2, 3) + Vector(4, 5, 6), Vector(5, 7, 9))
        with self.assertRaises(ValueError): Vector(1, 2, 3) + Vector(4, 5)

    def test_vector_subtraction(self):
        self.assertEqual(Vector(1, 2, 3) - Vector(4, 5, 6), Vector(-3, -3, -3))
        with self.assertRaises(ValueError): Vector(1, 2, 3) - Vector(4, 5)

    def test_invalid_addition_subtraction(self):
        v = Vector(1, 2, 3)

        for invalid in [0, None, ""]:
            with self.assertRaises(TypeError): v + invalid
            with self.assertRaises(TypeError): invalid + v
            with self.assertRaises(TypeError): v - invalid
            with self.assertRaises(TypeError): invalid - v

    def test_scalar_multiplication(self):
        v = Vector(1, 2, 3)

        # Vector * Number
        self.assertEqual(v * 1  , Vector(1, 2, 3))
        self.assertEqual(v * 2  , Vector(2, 4, 6))
        self.assertEqual(v * 0.5, Vector(0.5, 1, 1.5))
        self.assertEqual(v * 0  , Vector(0, 0, 0))

        # Number * Vector
        self.assertEqual(1   * v, Vector(1, 2, 3))
        self.assertEqual(2   * v, Vector(2, 4, 6))
        self.assertEqual(0.5 * v, Vector(0.5, 1, 1.5))
        self.assertEqual(0   * v, Vector(0, 0, 0))

    def test_scalar_division(self):
        v = Vector(1, 2, 3)

        # Vector / Number
        self.assertEqual(v / 1  , Vector(1, 2, 3))
        self.assertEqual(v / 2  , Vector(0.5, 1, 1.5))
        self.assertEqual(v / 0.5, Vector(2, 4, 6))

        # Vector / 0 is invalid
        with self.assertRaises(ZeroDivisionError): v / 0

        # Number / Vector is undefined
        with self.assertRaises(TypeError): 1 / v

    def test_matrix_multiplication(self):
        # Identity * Vector
        self.assertEqual(Matrix.identity(3) * Vector(1, 3, 10), Vector(1, 3, 10))
        with self.assertRaises(ValueError): Matrix.identity(4) * Vector(1, 2, 3)

        # Zero * Vector
        self.assertEqual(Matrix.zero(3) * Vector(1, 2, 3), Vector(0, 0, 0))

        # (Square) Matrix * Vector
        m = Matrix(
            [1, 1, 1],
            [0, 1, 1],
            [0, 0, 1])
        self.assertEqual(m * Vector(0, 0, 0), Vector(0, 0, 0))
        self.assertEqual(m * Vector(1, 2, 3), Vector(6, 5, 3))
        with self.assertRaises(ValueError): m * Vector(1, 2, 3, 4)

        # (Non-square) Matrix * Vector
        m = Matrix(
            [1, 1, 1],
            [0, 2, 2],
            [0, 3, 0],
            [0, 0, 4])
        self.assertEqual(m * Vector(0, 0, 0), Vector(0, 0, 0, 0))
        self.assertEqual(m * Vector(1, 2, 3), Vector(6, 10, 6, 12))
        with self.assertRaises(ValueError): m * Vector(1, 2, 3, 4)

        # Scaling by multiplication with scaled identity
        self.assertEqual((5 * Matrix.identity(3)) * Vector(1, 2, 3), Vector(5, 10, 15))

        # Vector * Matrix is invalid
        with self.assertRaises(TypeError): Vector(1, 2, 3) * Matrix.identity(3)

    def test_invalid_multiplication_division(self):
        v = Vector(1, 2, 3)

        for invalid in [None, ""]:
            with self.assertRaises(TypeError): v * invalid
            with self.assertRaises(TypeError): invalid * v
            with self.assertRaises(TypeError): v / invalid
            with self.assertRaises(TypeError): invalid / v

    def test_dot_product(self):
        self.assertEqual(Vector(1, 2, 3).dot(Vector(0, 0, 0)), 0) # Zero vector right
        self.assertEqual(Vector(0, 0, 0).dot(Vector(1, 2, 3)), 0) # Zero vector left
        self.assertEqual(Vector(1, 2, 3).dot(Vector(4, 5, -6)), -4) # Non-zero vectors

        # Perpendicular
        self.assertEqual(Vector(0, 1).dot(Vector(2, 0)), 0)
        self.assertEqual(Vector(1, 2).dot(Vector(-3, 1.5)), 0)

        with self.assertRaises(ValueError): Vector(1, 2, 3).dot(Vector(1, 2)) # Dimension mismatch

        # Invalid type
        with self.assertRaises(TypeError): Vector(1, 2, 3).dot(None)
        with self.assertRaises(TypeError): Vector(1, 2, 3).dot(0)
        with self.assertRaises(TypeError): Vector(1, 2, 3).dot("")

    def test_cross_product(self):
        self.assertEqual(Vector(1, 2, 3).cross(Vector(0, 0, 0)), Vector(0, 0, 0))      # Null vector right
        self.assertEqual(Vector(0, 0, 0).cross(Vector(1, 2, 3)), Vector(0, 0, 0))      # Null vector left
        self.assertEqual(Vector(1, 2, 3).cross(Vector(-1, -2, -3)), Vector(0, 0, 0))   # Opposite vectors
        self.assertEqual(Vector(1, 2, 3).cross(Vector(-7, 8, 9)), Vector(-6, -30, 22)) # Regular vectors

        with self.assertRaises(ValueError): Vector(1, 2, 3).cross(Vector(1, 2)   ) # Length mismatch
        with self.assertRaises(ValueError): Vector(1, 2)   .cross(Vector(1, 2, 3)) # Length mismatch
        with self.assertRaises(ValueError): Vector(1, 2)   .cross(Vector(1, 2)   ) # Only defined for 3-vectors

        with self.assertRaises(TypeError): Vector(1, 2, 3).cross(None)
        with self.assertRaises(TypeError): Vector(1, 2, 3).cross(0)
        with self.assertRaises(TypeError): Vector(1, 2, 3).cross("")

    def test_length_squared(self):
        self.assertEqual(Vector().length_squared, 0)

        self.assertEqual(Vector(2).length_squared,  4)

        self.assertEqual(Vector( 2,  0).length_squared,  4)
        self.assertEqual(Vector( 0,  2).length_squared,  4)
        self.assertEqual(Vector(-2,  0).length_squared,  4)
        self.assertEqual(Vector( 0, -2).length_squared,  4)

        self.assertEqual(Vector(3, 4)    .length_squared, 25)
        self.assertEqual(Vector(2, 3, 6) .length_squared, 49)
        self.assertEqual(Vector(2, 6, -3).length_squared, 49)
        self.assertEqual(Vector(0, 0, 0) .length_squared,  0)

    def test_length(self):
        self.assertEqual(Vector().length, 0)

        self.assertEqual(Vector(2).length,  2)

        self.assertEqual(Vector( 2,  0).length,  2)
        self.assertEqual(Vector( 0,  2).length,  2)
        self.assertEqual(Vector(-2,  0).length,  2)
        self.assertEqual(Vector( 0, -2).length,  2)

        self.assertEqual(Vector(3, 4)    .length, 5)
        self.assertEqual(Vector(2, 3, 6) .length, 7)
        self.assertEqual(Vector(2, 6, -3).length, 7)
        self.assertEqual(Vector(0, 0, 0) .length, 0)

    def test_normalized(self):
        # 1D
        self.assertEqual(Vector( 2).normalized(), Vector( 1))
        self.assertEqual(Vector(-2).normalized(), Vector(-1))

        # 2D
        self.assertEqual(Vector( 3, 4).normalized(), Vector( 0.6, 0.8))
        self.assertEqual(Vector(-3, 4).normalized(), Vector(-0.6, 0.8))

        # 3D
        self.assertEqual(Vector( 9,  12, 20).normalized(), Vector( 0.36,  0.48, 0.8))
        self.assertEqual(Vector(-9, -12, 20).normalized(), Vector(-0.36, -0.48, 0.8))

        # Linear 3D
        self.assertEqual(Vector( 2, 0, 0).normalized(), Vector( 1, 0, 0))
        self.assertEqual(Vector(-2, 0, 0).normalized(), Vector(-1, 0, 0))

        # Planar 3D
        self.assertEqual(Vector( 3, 4, 0).normalized(), Vector( 0.6, 0.8, 0))
        self.assertEqual(Vector(-3, 4, 0).normalized(), Vector(-0.6, 0.8, 0))

    def test_angle(self):
        # Colinear 2D
        self.assertAlmostEqual(Vector( 1, 0  ).angle(Vector( 1, 0  )),   0.0)
        self.assertAlmostEqual(Vector( 2, 3.4).angle(Vector( 2, 3.4)),   0.0)

        # Generic 2D
        self.assertAlmostEqual(Vector( 1, 0).angle(Vector( 1, 1)),  45.0)
        self.assertAlmostEqual(Vector( 1, 0).angle(Vector( 0, 2)),  90.0)
        self.assertAlmostEqual(Vector( 1, 0).angle(Vector(-1, 1)), 135.0)
        self.assertAlmostEqual(Vector( 1, 0).angle(Vector(-1, 0)), 180.0)
        self.assertAlmostEqual(Vector( 1, 0).angle(Vector(-2, 0)), 180.0)
        self.assertAlmostEqual(Vector( 1, 1).angle(Vector(-1, 1)),  90.0)

        # Colinear 3D
        self.assertAlmostEqual(Vector(1, 0  ,  0   ).angle(Vector(1, 0  ,  0   )), 0.0)
        self.assertAlmostEqual(Vector(2, 3.4,  0   ).angle(Vector(2, 3.4,  0   )), 0.0)
        self.assertAlmostEqual(Vector(2, 3.4, -5.67).angle(Vector(2, 3.4, -5.67)), 0.0)

        # Planar 3D
        self.assertAlmostEqual(Vector(1, 0, 0).angle(Vector( 1, 0, 0)),   0.0)
        self.assertAlmostEqual(Vector(1, 0, 0).angle(Vector( 1, 1, 0)),  45.0)
        self.assertAlmostEqual(Vector(1, 0, 0).angle(Vector( 0, 2, 0)),  90.0)
        self.assertAlmostEqual(Vector(1, 0, 0).angle(Vector(-1, 1, 0)), 135.0)
        self.assertAlmostEqual(Vector(1, 0, 0).angle(Vector(-1, 0, 0)), 180.0)
        self.assertAlmostEqual(Vector(1, 0, 0).angle(Vector(-2, 0, 0)), 180.0)

        # Generic 3D
        self.assertAlmostEqual(Vector(1, 1, 1).angle(Vector(-1, -1, -1)), 180.0)

    def test_normal(self):
        test_values = [
            # Different lengths
            Vector(1, 2      ),
            Vector(1, 2, 3   ),
            Vector(1, 2, 3, 4),

            # Different orders
            Vector(1, 2, 3),
            Vector(1, 3, 2),
            Vector(2, 1, 3),
            Vector(2, 3, 1),
            Vector(3, 1, 2),
            Vector(3, 2, 1),

            # Unit vectors (only one non-zero component)
            Vector(1, 0, 0),
            Vector(0, 1, 0),
            Vector(0, 0, 1),

            # Identical components
            Vector(1, 2, 2),
            Vector(2, 1, 2),
            Vector(2, 2, 1),
            Vector(2, 1, 1),
            Vector(1, 2, 1),
            Vector(1, 1, 2),
            Vector(1, 1, 1),
        ]

        for value in test_values:
            normal = value.normal()
            self.assertEqual(len(normal), len(value))
            self.assertNotEqual(normal.length, 0)
            self.assertNotEqual(value, normal)
            self.assertEqual(value.dot(normal), 0)

        # Invalid
        with self.assertRaises(ValueError): Vector()       .normal()
        with self.assertRaises(ValueError): Vector(1)      .normal()
        with self.assertRaises(ValueError): Vector(0, 0, 0).normal()

    def test_collinear(self):
        # Same vector
        self.assertTrue(X.collinear(X))
        self.assertTrue(Y.collinear(Y))
        self.assertTrue(Z.collinear(Z))

        # Reverse direction
        self.assertTrue(X.collinear(-X))
        self.assertTrue(Y.collinear(-Y))
        self.assertTrue(Z.collinear(-Z))

        # Scaled
        self.assertTrue(X.collinear(2 * X))
        self.assertTrue(Y.collinear(2 * Y))
        self.assertTrue(Z.collinear(2 * Z))

        # Orthogonal
        self.assertFalse(X.collinear(Y))
        self.assertFalse(Y.collinear(Z))
        self.assertFalse(Z.collinear(X))

        # Arbitrary collinear
        self.assertTrue(Vector(1, 2, 3).collinear(Vector( 1,  2,  3)))
        self.assertTrue(Vector(1, 2, 3).collinear(Vector(-1, -2, -3)))
        self.assertTrue(Vector(1, 2, 3).collinear(Vector( 2,  4,  6)))
        self.assertTrue(Vector(1, 2, 3).collinear(Vector(-2, -4, -6)))

        # With zero
        self.assertTrue(Vector(1, 2, 0).collinear(Vector( 1,  2,  0)))
        self.assertTrue(Vector(1, 2, 0).collinear(Vector( 2,  4,  0)))

        # Arbitrary non-collinear
        self.assertFalse(Vector(1, 2, 3).collinear(Vector( 1,  2,  4)))
        self.assertFalse(Vector(1, 2, 3).collinear(Vector( 1,  2,  0)))

    def test_closest_axis(self):
        # Axis vectors (2D)
        self.assertEqual(Vector( 1,  0).closest_axis(), Vector( 1,  0))
        self.assertEqual(Vector( 0,  1).closest_axis(), Vector( 0,  1))
        self.assertEqual(Vector(-1,  0).closest_axis(), Vector(-1,  0))
        self.assertEqual(Vector( 0, -1).closest_axis(), Vector( 0, -1))

        # Arbitrary vectors (2D)
        self.assertEqual(Vector( 1,   2).closest_axis(), Vector(0,  1))
        self.assertEqual(Vector(-1,   2).closest_axis(), Vector(0,  1))
        self.assertEqual(Vector( 1,  -2).closest_axis(), Vector(0, -1))
        self.assertEqual(Vector(-1,  -2).closest_axis(), Vector(0, -1))

        # Vectors along axis (3D)
        self.assertEqual(Vector(1, 0, 0).closest_axis(), X)
        self.assertEqual(Vector(0, 2, 0).closest_axis(), Y)
        self.assertEqual(Vector(0, 0, 3).closest_axis(), Z)
        self.assertEqual(Vector(-1,  0,  0).closest_axis(), -X)
        self.assertEqual(Vector( 0, -2,  0).closest_axis(), -Y)
        self.assertEqual(Vector( 0,  0, -3).closest_axis(), -Z)

        # Arbitrary vectors (3D)
        self.assertEqual(Vector(1, 2, 3).closest_axis(), Z)
        self.assertEqual(Vector(1, 3, 2).closest_axis(), Y)
        self.assertEqual(Vector(2, 1, 3).closest_axis(), Z)
        self.assertEqual(Vector(2, 3, 1).closest_axis(), Y)
        self.assertEqual(Vector(3, 1, 2).closest_axis(), X)
        self.assertEqual(Vector(3, 2, 1).closest_axis(), X)


    #############
    ## Helpers ##
    #############

    def test_to_vector(self):
        # Regular call without length check
        self.assertEqual(to_vector(Vector(1, 2, 3), "dummy", None), Vector(1, 2, 3)) # From Vector
        self.assertEqual(to_vector(      [1, 2, 3], "dummy", None), Vector(1, 2, 3)) # From list
        self.assertEqual(to_vector(      (1, 2, 3), "dummy", None), Vector(1, 2, 3)) # From tuple

        # Empty
        self.assertEqual(to_vector([], "dummy", None), Vector())

        # Length check
        self.assertEqual(                   to_vector([1, 2, 3], "dummy", 3), Vector(1, 2, 3)) # Success
        with self.assertRaises(ValueError): to_vector([1, 2, 3], "dummy", 4)                   # Failure

        # Invalid values
        with self.assertRaises(TypeError ): to_vector(None       , "dummy", None)
        with self.assertRaises(TypeError ): to_vector(1          , "dummy", None)
        with self.assertRaises(TypeError ): to_vector(""         , "dummy", None)
        with self.assertRaises(TypeError ): to_vector("123"      , "dummy", None)
        with self.assertRaises(TypeError ): to_vector([1, 2, "3"], "dummy", None)
