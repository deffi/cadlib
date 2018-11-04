from cadlib.object.primitives import Sphere, Cuboid, Cylinder
from cadlib.csg import Intersection
from cadlib.scad import ScadObject
from cadlib.util.vector import Z
from tests.unit_test import TestCase

class TestIntersection(TestCase):
    def test_str(self):
        self.assertStr(Intersection([]), "Intersection")

    def test_equality(self):
        sphere   = Sphere(11)
        cuboid   = Cuboid([11, 22, 33])
        cylinder = Cylinder(Z, 11, 22)
        objects = [sphere, cuboid, cylinder]

        # Same object
        self.assertEqualToItself(Intersection([]     ))
        self.assertEqualToItself(Intersection(objects))

        # Equal objects
        self.assertEqual(Intersection([]     ), Intersection([]     ))
        self.assertEqual(Intersection(objects), Intersection(objects))

        # Different objects
        self.assertNotEqual(Intersection(objects         ), Intersection([sphere, cuboid]))
        self.assertNotEqual(Intersection([cuboid, sphere]), Intersection([sphere, cuboid]))

        # Equal objects from different specifications
        self.assertEqual(Intersection.empty(), Intersection([]))

    def test_to_scad(self):
        sphere   = Sphere(2)
        cube     = Cuboid([10, 10, 10])
        cylinder = Cylinder(Z, 5, 5)

        self.assertEqual(Intersection([sphere, cube, cylinder]).to_scad(),
            ScadObject("intersection", None, None, [
                sphere  .to_scad(),
                cube    .to_scad(),
                cylinder.to_scad(),
        ]))
