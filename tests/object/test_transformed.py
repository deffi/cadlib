from tests.unit_test import TestCase
from cadlib.object.transformed import Transformed
from cadlib.transform.chained import Chained
# from cadlib.util.vector import X, Y, Z
from cadlib.scad.scad import ScadObject
from cadlib.object.primitives.cube import Cube
from cadlib.object.primitives.sphere import Sphere
from cadlib.transform.primitives.scale import Scale
from cadlib.transform.primitives.translate import Translate
from cadlib.transform.primitives.rotate_xyz import RotateXyz

class TestTransformed(TestCase):
    def test_construction(self):
        # Transformed objects can also be created by multiplying a transform with an object. This is
        # tested in test_object.py, as it concerns the operators defined by Object.

        # Transformed object
        t = Translate([10, 20, 30])
        cube = Cube(1)

        with self.assertNothingRaised(): Transformed(t, cube)

        with self.assertRaises(TypeError): Transformed(t, t)
        with self.assertRaises(TypeError): Transformed(cube, cube)
        with self.assertRaises(TypeError): Transformed(t, None)
        with self.assertRaises(TypeError): Transformed(None, cube)

    def test_equality(self):
        # TODO use only one type of transform and object
        r1 = RotateXyz(60, 30, 15)
        r2 = RotateXyz(60, 30, 15)
        t  = Translate([60, 30, 15])
        cube1 = Cube(11)
        cube2 = Cube(11)
        sphere = Sphere(11)
        self.assertEqual   (Transformed(r1, cube1), Transformed(r1, cube2))  # Equal objects
        self.assertEqual   (Transformed(r1, cube1), Transformed(r2, cube1))  # Equal transform
        self.assertNotEqual(Transformed(r1, cube1), cube1)                   # Transformed / original
        self.assertNotEqual(Transformed(r1, cube1), Transformed(t, cube1))   # Different transform
        self.assertNotEqual(Transformed(r1, cube1), Transformed(r1, sphere)) # Different objects

    def test_to_scad(self):
        r = RotateXyz(60, 30, 15)
        s = Scale([1, 2, -1])
        cube = Cube(11)

        # Simple transform
        self.assertEqual(Transformed(r, cube).to_scad(),
            ScadObject("rotate", [[60, 30, 15]], None, [
                ScadObject("cube", [[11, 11, 11]], None, None),
            ])
        )

        # Chained transform
        self.assertEqual(Transformed(Chained([r, s]), cube).to_scad(),
            ScadObject("rotate", [[60, 30, 15]], None, [
                ScadObject("scale", [[1, 2, -1]], None, [
                    ScadObject("cube", [[11, 11, 11]], None, None),
                ])
            ])
        )
