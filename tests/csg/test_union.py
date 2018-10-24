from cadlib.object.primitives import Sphere, Cube, Cylinder
from cadlib.csg import Union
from cadlib.scad import ScadObject
from cadlib.util.vector import Z
from tests.unit_test import TestCase

class TestUnion(TestCase):
    def test_construction(self):
        sphere   = Sphere(11)
        cube     = Cube([11, 22, 33])
        cylinder = Cylinder(Z, 11, 22)
        objects = [sphere, cube, cylinder]

        self.assertEqual(Union.empty(), Union([]))

    def test_equality(self):
        sphere   = Sphere(11)
        cube     = Cube([11, 22, 33])
        cylinder = Cylinder(Z, 11, 22)
        objects = [sphere, cube, cylinder]

        # Same object
        self.assertEqualToItself(Union([]     ))
        self.assertEqualToItself(Union(objects))

        # Equal objects
        self.assertEqual(Union([]     ), Union([]     ))
        self.assertEqual(Union(objects), Union(objects))

        # Different objects
        self.assertNotEqual(Union(objects       ), Union([sphere, cube]))
        self.assertNotEqual(Union([cube, sphere]), Union([sphere, cube]))

    def test_to_scad(self):
        sphere   = Sphere(2)
        cube     = Cube([10, 10, 10])
        cylinder = Cylinder(Z, 5, 5)

        self.assertEqual(Union([sphere, cube, cylinder]).to_scad(),
            ScadObject("union", None, None, [
                sphere  .to_scad(),
                cube    .to_scad(),
                cylinder.to_scad(),
        ]))

    def test_sum(self):
        sphere   = Sphere(2)
        cube     = Cube([10, 10, 10])
        cylinder = Cylinder(Z, 5, 5)
        objects = [sphere, cube, cylinder]

        self.assertEqual(sum(objects, Union.empty()), Union(objects))
