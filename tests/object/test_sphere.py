from tests.unit_test import TestCase
from cadlib.object.primitives import Sphere


class TestSphere(TestCase):
    def test_construction(self):
        # Radius/diameter
        with self.assertNothingRaised(): sphere = Sphere(1)
        with self.assertNothingRaised(): sphere = Sphere(r = 1)
        with self.assertNothingRaised(): sphere = Sphere(d = 2)

        # Zero size
        with self.assertWarnsRegex(UserWarning, r'radius is 0')  : Sphere(0)
        with self.assertWarnsRegex(UserWarning, r'diameter is 0'): Sphere(d=0)

        # Erroneous
        with self.assertRaises(ValueError): Sphere()
        with self.assertRaises(ValueError): Sphere(r=1.0, d=2.0)


    def test_equality(self):
        # Same object
        self.assertEqualToItself(Sphere(11))

        # Equal object
        self.assertEqual (Sphere(11), Sphere(11))

        # Different objects
        self.assertNotEqual (Sphere(11), Sphere(22))

        # Equal objects from different specifications
        self.assertEqual(Sphere(1)  , Sphere(r=1))
        self.assertEqual(Sphere(d=2), Sphere(r=1))

    def test_to_scad(self):
        # Primitives
        self.assertScadObject(Sphere (11), "sphere", [11], None, None)

    def test_repr(self):
        self.assertRepr(Sphere(11), "Sphere(r=11)")
        self.assertRepr(Sphere(d=44), "Sphere(r=22.0)")

    def test_str(self):
        self.assertStr(Sphere(11), "Sphere with radius 11")
        self.assertStr(Sphere(d=44), "Sphere with radius 22.0")