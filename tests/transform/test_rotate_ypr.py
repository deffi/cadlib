from tests.unit_test import TestCase
from cadlib.transform.primitives import RotateYpr
from cadlib.scad import ScadObject

class TestRotateYpr(TestCase):
    def test_construction(self):
        # Valid
        RotateYpr(10, 20, 30)

        # Invalid
        with self.assertRaises(TypeError): RotateYpr(1, 2, "3")

    def test_equality(self):
        # Same object
        self.assertEqualToItself(RotateYpr(10, 20, 30))

        # Equal objects
        self.assertEqual   (RotateYpr(10, 20, 30), RotateYpr(10, 20, 30)) # Equal

        # Different objects
        self.assertNotEqual(RotateYpr(10, 20, 30), RotateYpr(10, 20, 40)) # Different values

    def test_to_scad(self):
        self.ignore_scad_comments = True

        # Since OpenSCAD does not have YPR rotations, they have to translated to
        # corresponding XYZ rotations.

        # A zero YPR transform is a zero XYZ transform.
        self.assertEqual(RotateYpr(0, 0, 0).to_scad(None),
            ScadObject("rotate", [[0, 0, 0]], None, None))

        # A single-axis YPR rotation can be expressed as a single-axis YPR
        # rotation.
        # Yaw - Z axis
        self.assertEqual(RotateYpr(1, 0, 0).to_scad(None),
            ScadObject("rotate", [[0, 0, 1]], None, None))
        # Pitch - X axis
        self.assertEqual(RotateYpr(0, 2, 0).to_scad(None),
            ScadObject("rotate", [[2, 0, 0]], None, None))
        # Roll - Y axis
        self.assertEqual(RotateYpr(0, 0, 3).to_scad(None),
            ScadObject("rotate", [[0, 3, 0]], None, None))

        # A dual-axis YPR rotation must be expressed as a chain of two single-
        # axis XYZ rotations.
        self.assertEqual(RotateYpr(0, 2, 3).to_scad(None),
            ScadObject("rotate", [[2, 0, 0]], None, [
            ScadObject("rotate", [[0, 3, 0]], None, None)]))
        self.assertEqual(RotateYpr(1, 0, 3).to_scad(None),
            ScadObject("rotate", [[0, 0, 1]], None, [
            ScadObject("rotate", [[0, 3, 0]], None, None)]))
        self.assertEqual(RotateYpr(1, 2, 0).to_scad(None),
            ScadObject("rotate", [[0, 0, 1]], None, [
            ScadObject("rotate", [[2, 0, 0]], None, None)]))

        # A tripel-axis YPR rotation must be expressed as a chain of three
        # single-axis XYZ rotations.
        self.assertEqual(RotateYpr(1, 2, 3).to_scad(None),
            ScadObject("rotate", [[0, 0, 1]], None, [
            ScadObject("rotate", [[2, 0, 0]], None, [
            ScadObject("rotate", [[0, 3, 0]], None, None)])]))

    def test_repr(self):
        self.assertRepr(RotateYpr(1, 2, 3), "RotateYpr(1, 2, 3)")