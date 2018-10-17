from tests.unit_test import TestCase
from cadlib.object.primitives import Sphere
# from cadlib.util.vector import X, Y, Z
# from cadlib.scad.scad import ScadObject

class TestSphere(TestCase):
    def test_construction(self):
        # Radius/diameter
        with self.assertNothingRaised(): sphere = Sphere(11)
        # TODO diameter
#
    def test_equality(self):
        # Same object
        self.assertEqualToItself(Sphere(11))

        # Equal object
        self.assertEqual (Sphere(11), Sphere(11))

        # Different objects
        self.assertNotEqual (Sphere(11), Sphere(22))

        # Equal objects from different specifications
        # TODO

    def test_to_scad(self):
        # Primitives
        self.assertScadObject(Sphere (11), "sphere", [11], None, None)
