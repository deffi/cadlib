from tests.unit_test import TestCase
from cadlib.object.primitives import Sphere


class TestSphere(TestCase):
    def test_construction(self):
        # Radius/diameter
        with self.assertNothingRaised(): sphere = Sphere(1)
        with self.assertNothingRaised(): sphere = Sphere(r = 1)
        with self.assertNothingRaised(): sphere = Sphere(d = 2)

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
