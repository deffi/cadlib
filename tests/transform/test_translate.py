from tests.unit_test import TestCase
from cadlib.transform.primitives import Translate

class TestTranslate(TestCase):
    def test_construction(self):
        # Valid
        Translate([1, 2, 3])

        # Invalid
        with self.assertRaises(TypeError): Translate([1, 2, "3"])

    def test_equality(self):
        # Same object
        self.assertEqualToItself(Translate([60, 30, 15]))

        # Equal objects
        self.assertEqual(Translate([60, 30, 15]), Translate([60, 30, 15]))

        # Different objects
        self.assertNotEqual(Translate([60, 30, 15]), Translate([60, 30, 16]))

    def test_inverse(self):
        self.assertInverse(Translate([1, 2, -3]), Translate([-1, -2, 3]))

    def test_to_scad(self):
        t = Translate([30, 20, 10])

        self.assertScadObjectTarget(t, None, "translate", [[30, 20, 10]], None, None)

    def test_repr(self):
        self.assertRepr(Translate([10, 20, 30]), "Translate(Vector(10, 20, 30))")
