from tests.unit_test import TestCase
from cadlib.object.primitives import Sphere


class TestSphere(TestCase):
    def test_construction(self):
        # Radius/diameter
        with self.assertNothingRaised(): sphere = Sphere(1)

        # Zero size
        with self.assertWarnsRegex(UserWarning, r'radius is 0')  : Sphere(0)

    def test_equality(self):
        # Same object
        self.assertEqualToItself(Sphere(11))

        # Equal object
        self.assertEqual (Sphere(11), Sphere(11))

        # Different objects
        self.assertNotEqual (Sphere(11), Sphere(22))

    def test_to_scad(self):
        # Primitives
        self.assertScadObject(Sphere (11), "sphere", [11], None, None)

    def test_repr(self):
        self.assertRepr(Sphere(11), "Sphere(r=11)")

    def test_str(self):
        self.assertStr(Sphere(11), "Sphere with radius 11")
