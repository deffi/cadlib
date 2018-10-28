from unittest import TestCase as OriginalTestCase
from cadlib.transform import Transform
from contextlib import contextmanager
from cadlib.scad import ScadObject
from cadlib.object import Object
from cadlib.util import Matrix

class TestCase(OriginalTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ignore_scad_comments = False

    def assertEqualToItself(self, x):
        self.assertEqual(x, x)

    @contextmanager
    def assertNothingRaised(self):
        """
        Similar to assertRaises, this method will raise the original exception, if any is raised.
        """

        # ...this makes the implementation very simple:
        yield


    def assertScadObject(self, thing, id, parameters, kw_parameters, children = None):
        actual = thing.to_scad()
        expected = ScadObject(id, parameters, kw_parameters, children)
        self.assertEqual(actual, expected)

    def assertScadObjectTarget(self, thing, target, id, parameters, kw_parameters, children = None):
        actual = thing.to_scad(target)
        expected = ScadObject(id, parameters, kw_parameters, children)
        self.assertEqual(actual, expected)

    def assertScadCode(self, thing, code):
        if isinstance(thing, Transform):
            self.assertEqual(thing.to_scad(None).to_code(inline=True, simplify=True), code)
        else:
            self.assertEqual(thing.to_scad().to_code(inline=True, simplify=True), code)

    def assertEqual(self, first, second, msg=None):
        if self.ignore_scad_comments:
            if isinstance(first, ScadObject):
                first = first.clear_comment(recursive=True)
            if isinstance(second, ScadObject):
                second = second.clear_comment(recursive=True)

        super().assertEqual(first, second, msg)

    def assertRepr(self, thing, expected):
        self.assertEqual(repr(thing), expected)

    def assertStr(self, thing, expected):
        self.assertEqual(str(thing), expected)

    def assertInverse(self, a, b, symmetric = True):
        self.assertEqual(a.inverse(), b)
        if symmetric:
            self.assertEqual(b.inverse(), a)

        self.assertAlmostEqual(a.to_matrix() * b.to_matrix(), Matrix.identity(4))
        self.assertAlmostEqual(b.to_matrix() * a.to_matrix(), Matrix.identity(4))

    def assertAlmostEqual(self, first, second, places=None, msg=None, delta=None):
        if isinstance(first, Matrix) and isinstance(second, Matrix):
            self.assertEqual(first.dimensions, second.dimensions)
            for r in range(first.row_count):
                for c in range(first.column_count):
                    super().assertAlmostEqual(first[r, c], second[r, c], places, msg, delta)
        elif isinstance(first, list) and isinstance(second, list):
            self.assertEqual(len(first), len(second))
            for a, b in zip(first, second):
                self.assertAlmostEqual(a, b)
        else:
            super().assertAlmostEqual(first, second, places, msg, delta)

    def assertOrthogonal(self, matrix):
        self.assertEqual(matrix.row_count, matrix.column_count)
        self.assertAlmostEqual(matrix * matrix.transpose(), matrix.identity(matrix.row_count))
        self.assertAlmostEqual(matrix.transpose() * matrix, matrix.identity(matrix.row_count))

    def assertSquare(self, matrix):
        self.assertEqual(matrix.row_count, matrix.column_count)

    def assertIdentity(self, matrix):
        self.assertSquare(matrix)
        self.assertAlmostEqual(matrix, Matrix.identity(matrix.row_count))
