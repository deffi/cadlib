from cadlib.object.primitives import Sphere, Cube, Cylinder
from cadlib.csg import Difference
from cadlib.scad import ScadObject
from cadlib.util.vector import Z
from tests.unit_test import TestCase

class TestDifference(TestCase):
    def test_str(self):
        self.assertStr(Difference([]), "Difference")

    def test_equality(self):
        sphere   = Sphere(11)
        cube     = Cube([11, 22, 33])
        cylinder = Cylinder(Z, 11, 22)
        objects = [sphere, cube, cylinder]

        # Same object
        self.assertEqualToItself(Difference([]     ))
        self.assertEqualToItself(Difference(objects))

        # Equal objects
        self.assertEqual(Difference([]     ), Difference([]     ))
        self.assertEqual(Difference(objects), Difference(objects))

        # Different objects
        self.assertNotEqual(Difference(objects       ), Difference([sphere, cube]))
        self.assertNotEqual(Difference([cube, sphere]), Difference([sphere, cube]))

        # Equal objects from different specifications
        self.assertEqual(Difference.empty(), Difference([]))

    def test_to_scad(self):
        sphere   = Sphere(2)
        cube     = Cube([10, 10, 10])
        cylinder = Cylinder(Z, 5, 5)

        self.assertEqual(Difference([sphere, cube, cylinder]).to_scad(),
            ScadObject("difference", None, None, [
                sphere  .to_scad(),
                cube    .to_scad(),
                cylinder.to_scad(),
        ]))
