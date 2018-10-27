from tests.unit_test import TestCase
from cadlib.scad import ScadObject
from cadlib.util import Matrix

class Foo(Exception):
    pass

class Bar(Exception):
    pass

class TestUnitTest(TestCase):
    def test_assertRaises(self):
        # Expected raise
        with self.assertRaises(Foo):
            raise Foo

        # Nothing raised
        with self.assertRaises(AssertionError):
            with self.assertRaises(Foo):
                pass

        # Wrong exception raised
        with self.assertRaises(Bar):
            with self.assertRaises(Foo):
                raise Bar

    def test_assertNothingRaised(self):
        # Expected nothing
        with self.assertNothingRaised():
            pass

        # Unexpected raise
        with self.assertRaises(Foo):
            with self.assertNothingRaised():
                raise Foo

    def test_ignore_scad_comments(self):
        scad1 = ScadObject("scad", None, None, None).comment("comment 1")
        scad2 = ScadObject("scad", None, None, None).comment("comment 2")

        # Ordinarily, the objects are considered different
        with self.assertRaises(AssertionError):
            self.assertEqual(scad1, scad2)

        # When ignoring comments, the objects are considered equal
        self.ignore_scad_comments = True
        self.assertEqual(scad1, scad2)

        # Ordinarily, the objects are considered different
        self.ignore_scad_comments = False
        with self.assertRaises(AssertionError):
            self.assertEqual(scad1, scad2)

    def test_assert_almost_equal_list(self):
        epsilon = 1e-8

        # Almost equal
        self.assertAlmostEqual([1], [1 + epsilon])
        self.assertAlmostEqual([1, 2], [1 + epsilon, 2 + epsilon])
        self.assertAlmostEqual([[1, 2], [3, 4]], [[1 + epsilon, 2 + epsilon], [3 + epsilon, 4 + epsilon]])

        # Not almost equal
        with self.assertRaises(AssertionError):
            self.assertAlmostEqual([1, 2], [1.1, 2.1])

        # Not if the dimensions are different
        with self.assertRaises(AssertionError):
            self.assertAlmostEqual([1, 2], [1, 2, 3])

    def test_assert_almost_equal_matrix(self):
        epsilon = 1e-8
        delta   = 0.1

        m1 = Matrix.from_rows([1, 2], [3, 4])
        m2 = Matrix.from_rows([1 + epsilon, 2 + epsilon], [3 + epsilon, 4 + epsilon])
        m3 = Matrix.from_rows([1 + delta  , 2 + delta  ], [3 + delta  , 4 + delta  ])
        m4 = Matrix.from_rows([1, 2], [3, 4], [5, 6])

        # Almost equal
        self.assertAlmostEqual(m1, m1)
        self.assertAlmostEqual(m1, m2)

        # Not almost equal
        with self.assertRaises(AssertionError):
            self.assertAlmostEqual(m1, m3)

        # Not if the dimensions are different
        with self.assertRaises(AssertionError):
            self.assertAlmostEqual(m1, m4)

