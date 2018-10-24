from cadlib.object.primitives import Sphere, Cube, Cylinder
from cadlib.csg import Intersection
from cadlib.scad import ScadObject
from cadlib.util.vector import Z
from tests.unit_test import TestCase

class TestIntersection(TestCase):
    def test_construction(self):
        sphere   = Sphere(11)
        cube     = Cube([11, 22, 33])
        cylinder = Cylinder(Z, 11, 22)
        objects = [sphere, cube, cylinder]

        self.assertEqual(Intersection.empty(), Intersection([]))

    def test_equality(self):
        sphere   = Sphere(11)
        cube     = Cube([11, 22, 33])
        cylinder = Cylinder(Z, 11, 22)
        objects = [sphere, cube, cylinder]

        # Same object
        self.assertEqualToItself(Intersection([]     ))
        self.assertEqualToItself(Intersection(objects))

        # Equal objects
        self.assertEqual(Intersection([]     ), Intersection([]     ))
        self.assertEqual(Intersection(objects), Intersection(objects))

        # Different objects
        self.assertNotEqual(Intersection(objects       ), Intersection([sphere, cube]))
        self.assertNotEqual(Intersection([cube, sphere]), Intersection([sphere, cube]))

    def test_to_scad(self):
        sphere   = Sphere(2)
        cube     = Cube([10, 10, 10])
        cylinder = Cylinder(Z, 5, 5)

        self.assertEqual(Intersection([sphere, cube, cylinder]).to_scad(),
            ScadObject("intersection", None, None, [
                sphere  .to_scad(),
                cube    .to_scad(),
                cylinder.to_scad(),
        ]))