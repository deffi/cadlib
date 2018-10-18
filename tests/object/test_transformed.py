from tests.unit_test import TestCase
from cadlib.object.transformed import Transformed
from cadlib.transform.chained import Chained
# from cadlib.util.vector import X, Y, Z
from cadlib.scad.scad import ScadObject
from cadlib.object.primitives.cube import Cube
from cadlib.object.primitives.sphere import Sphere
from cadlib.transform.primitives.scale_xyz import ScaleXyz
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
        scale1a = ScaleXyz(1)
        scale1b = ScaleXyz(1)
        scale2  = ScaleXyz(2)

        cube1a = Cube(1)
        cube1b = Cube(1)
        cube2  = Cube(2)

        self.assertEqual   (Transformed(scale1a, cube1a), Transformed(scale1a, cube1b)) # Equal objects
        self.assertEqual   (Transformed(scale1a, cube1a), Transformed(scale1b, cube1a)) # Equal transform
        self.assertNotEqual(Transformed(scale1a, cube1a), cube1a)                       # Transformed / original
        self.assertNotEqual(Transformed(scale1a, cube1a), Transformed(scale2 , cube1a)) # Different transform
        self.assertNotEqual(Transformed(scale1a, cube1a), Transformed(scale1a, cube2 )) # Different objects

    def test_to_scad(self):
        r = RotateXyz(60, 30, 15)
        s = ScaleXyz([1, 2, -1])
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
