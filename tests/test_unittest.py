from tests.unit_test import TestCase
from cadlib.object.primitives.sphere import Sphere
from cadlib.scad import ScadObject

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
