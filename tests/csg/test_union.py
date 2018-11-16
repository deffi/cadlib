from cadlib.object.primitives import Sphere, Cuboid, Frustum
from cadlib.csg import Union
from cadlib.scad import ScadObject
from cadlib.util.vector import Z, origin
from tests.unit_test import TestCase

class TestUnion(TestCase):
    def test_str(self):
        self.assertStr(Union([]), "Union")

    def test_equality(self):
        sphere   = Sphere(11)
        cuboid   = Cuboid([11, 22, 33])
        cylinder = Frustum(origin, Z, 11, 11)
        objects = [sphere, cuboid, cylinder]

        # Same object
        self.assertEqualToItself(Union([]     ))
        self.assertEqualToItself(Union(objects))

        # Equal objects
        self.assertEqual(Union([]     ), Union([]     ))
        self.assertEqual(Union(objects), Union(objects))

        # Different objects
        self.assertNotEqual(Union(objects         ), Union([sphere, cuboid]))
        self.assertNotEqual(Union([cuboid, sphere]), Union([sphere, cuboid]))

        # Equal objects from different specifications
        self.assertEqual(Union.empty(), Union([]))

    def test_to_scad(self):
        sphere   = Sphere(2)
        cube     = Cuboid([10, 10, 10])
        cylinder = Frustum(origin, Z, 11, 11)

        self.assertEqual(Union([sphere, cube, cylinder]).to_scad(),
            ScadObject("union", None, None, [
                sphere  .to_scad(),
                cube    .to_scad(),
                cylinder.to_scad(),
        ]))

        # Empty
        self.assertEqual(Union([]).to_scad(), ScadObject("union", None, None, None))

    def test_sum(self):
        sphere   = Sphere(2)
        cube     = Cuboid([10, 10, 10])
        cylinder = Frustum(origin, Z, 11, 11)
        objects = [sphere, cube, cylinder]

        self.assertEqual(sum(objects, Union.empty()), Union(objects))
