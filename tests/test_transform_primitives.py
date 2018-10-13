from cadlib.transform.primitives.rotate_axis_agle import RotateAxisAngle
from cadlib.transform.primitives.rotate_xyz import RotateXyz
from cadlib.transform.primitives.rotate_ypr import RotateYpr
from cadlib.transform.primitives.scale import Scale
from cadlib.transform.primitives.translate import Translate
from tests.unit_test import TestCase
from cadlib.util.number import to_number, to_list_of_numbers
from cadlib.geometry import Vector, to_vector

class TestTransformPrimitives(TestCase):
    # TODO move to test_vector
    def test_to_vector_helper(self):
        # Regular call without length check
        self.assertEqual(to_vector(Vector(1, 2, 3), "dummy", None), Vector(1, 2, 3)) # From Vector
        self.assertEqual(to_vector(      [1, 2, 3], "dummy", None), Vector(1, 2, 3)) # From list
        self.assertEqual(to_vector(      (1, 2, 3), "dummy", None), Vector(1, 2, 3)) # From tuple

        # Empty
        self.assertEqual(to_vector([], "dummy", None), Vector())

        # Length check
        self.assertEqual(                   to_vector([1, 2, 3], "dummy", 3), Vector(1, 2, 3)) # Success
        with self.assertRaises(ValueError): to_vector([1, 2, 3], "dummy", 4)                   # Failure

        # Invalid values
        with self.assertRaises(TypeError ): to_vector(None       , "dummy", None)
        with self.assertRaises(TypeError ): to_vector(1          , "dummy", None)
        with self.assertRaises(TypeError ): to_vector(""         , "dummy", None)
        with self.assertRaises(TypeError ): to_vector("123"      , "dummy", None)
        with self.assertRaises(TypeError ): to_vector([1, 2, "3"], "dummy", None)

    # TODO move to test_number
    def test_to_list_of_numbers_helper(self):
        # Regular call without length check
        self.assertEqual(to_list_of_numbers(Vector(1, 2, 3), "dummy", None), [1, 2, 3]) # From Vector
        self.assertEqual(to_list_of_numbers(      [1, 2, 3], "dummy", None), [1, 2, 3]) # From list
        self.assertEqual(to_list_of_numbers(      (1, 2, 3), "dummy", None), [1, 2, 3]) # From tuple

        # Empty
        self.assertEqual(to_list_of_numbers([], "dummy", None), [])

        # Length check
        self.assertEqual(                   to_list_of_numbers([1, 2, 3], "dummy", 3), [1, 2, 3]) # Success
        with self.assertRaises(ValueError): to_list_of_numbers([1, 2, 3], "dummy", 4)             # Failure

        # Invalid values
        with self.assertRaises(TypeError ): to_list_of_numbers(None       , "dummy", None)
        with self.assertRaises(TypeError ): to_list_of_numbers(1          , "dummy", None)
        with self.assertRaises(TypeError ): to_list_of_numbers(""         , "dummy", None)
        with self.assertRaises(TypeError ): to_list_of_numbers("123"      , "dummy", None)
        with self.assertRaises(TypeError ): to_list_of_numbers([1, 2, "3"], "dummy", None)

    # TODO move to test_number
    def test_to_number_helper(self):
        self.assertEqual(to_number(42 , None, "dummy", []), 42 ) # Int
        self.assertEqual(to_number(4.2, None, "dummy", []), 4.2) # Float

        self.assertEqual(to_number(None, 999, "dummy"), 999) # Default value

        with self.assertRaises(TypeError): to_number(None, 999, "dummy", []) # No default value

        # Invalid values
        with self.assertRaises(TypeError): to_number(""  , 999, "dummy")
        with self.assertRaises(TypeError): to_number([]  , 999, "dummy")


    def test_construction(self):
        # Rotate
        RotateAxisAngle(Vector(1, 2, 3), 45)
        self.assertEqual(RotateAxisAngle([1, 2, 3], 45), RotateAxisAngle(Vector(1, 2, 3), 45)) # list vs. Vector
        with self.assertRaises(ValueError): RotateAxisAngle(Vector(0, 0, 0), 45)

        RotateXyz(10, 20, 30)
        with self.assertRaises(TypeError): RotateXyz(1, 2, "3")

        RotateYpr(10, 20, 30)
        with self.assertRaises(TypeError): RotateYpr(1, 2, "3")


        # Scale
        Scale([1, 2, 3])
        with self.assertRaises(TypeError): Scale([1, 2, "3"])


        # Translate
        Translate([1, 2, 3])
        with self.assertRaises(TypeError): Translate([1, 2, "3"])

    def test_self_equality(self):
        # Rotate
        self.assertEqualToItself(RotateAxisAngle(Vector(1, 2, 3), 45))
        self.assertEqualToItself(RotateXyz(10, 20, 30))
        self.assertEqualToItself(RotateYpr(10, 20, 30))

        # Scale
        self.assertEqualToItself(Scale([1, 2, 3]))

        # Translate
        self.assertEqualToItself(Translate([1, 2, 3]))

    def test_equality(self):
        # Rotate
        self.assertEqual   (RotateAxisAngle(Vector(1, 2, 3), 45), RotateAxisAngle(Vector(1, 2, 3), 45)) # Equal
        self.assertNotEqual(RotateAxisAngle(Vector(1, 2, 3), 45), RotateAxisAngle(Vector(1, 2, 4), 45)) # Different axis
        self.assertNotEqual(RotateAxisAngle(Vector(1, 2, 3), 45), RotateAxisAngle(Vector(1, 2, 3), 46)) # Different angle
        self.assertEqual   (RotateXyz(10, 20, 30), RotateXyz(10, 20, 30)) # Equal
        self.assertNotEqual(RotateXyz(10, 20, 30), RotateXyz(10, 20, 40)) # Different values
        self.assertEqual   (RotateYpr(10, 20, 30), RotateYpr(10, 20, 30)) # Equal
        self.assertNotEqual(RotateYpr(10, 20, 30), RotateYpr(10, 20, 40)) # Different values
        self.assertNotEqual(RotateXyz(10, 20, 30), RotateYpr(10, 20, 30)) # Different class

        # Scale
        self.assertEqual   (Scale([1, 2, 3]), Scale([1, 2, 3]))
        self.assertNotEqual(Scale([1, 2, 3]), Scale([1, 2, 4]))

        # Translate
        self.assertEqual   (Translate([1, 2, 3]), Translate([1, 2, 3]))
        self.assertNotEqual(Translate([1, 2, 3]), Translate([1, 2, 4]))

        # Different
        self.assertNotEqual(Scale([1, 2, 3]), Translate([1, 2, 3])) # Different class

    def test_to_scad_code(self):
        # Axis/angle rotate
        self.assertScadCode(RotateAxisAngle([1, 2, 3], 45), "rotate(a = 45, v = [1, 2, 3]);")

        # XYZ rotate
        self.assertScadCode(RotateXyz(1, 2, 3), "rotate([1, 2, 3]);")

        # YPR rotate
        self.assertScadCode(RotateYpr(1, 2, 3), "rotate([0, 0, 1]) rotate([2, 0, 0]) rotate([0, 3, 0]);")
        self.assertScadCode(RotateYpr(0, 2, 3), "rotate([2, 0, 0]) rotate([0, 3, 0]);")
        self.assertScadCode(RotateYpr(1, 0, 3), "rotate([0, 0, 1]) rotate([0, 3, 0]);")
        self.assertScadCode(RotateYpr(1, 2, 0), "rotate([0, 0, 1]) rotate([2, 0, 0]);")
        self.assertScadCode(RotateYpr(1, 0, 0), "rotate([0, 0, 1]);")
        self.assertScadCode(RotateYpr(0, 2, 0), "rotate([2, 0, 0]);")
        self.assertScadCode(RotateYpr(0, 0, 3), "rotate([0, 3, 0]);")
        self.assertScadCode(RotateYpr(0, 0, 0), "rotate([0, 0, 0]);")

        # Scale
        self.assertScadCode(Scale    ([1, 2, 3]), "scale([1, 2, 3]);")

        # Translate
        self.assertScadCode(Translate([1, 2, 3]), "translate([1, 2, 3]);")
