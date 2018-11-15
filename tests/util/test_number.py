import unittest
from cadlib.util.vector import Vector
from cadlib.util import number

class TestNumber(unittest.TestCase):
    # def test_to_list_of_numbers_helper(self):
    #     # Regular call without length check
    #     self.assertEqual(number.to_list_of_numbers(Vector(1, 2, 3), "dummy", None), [1, 2, 3]) # From Vector
    #     self.assertEqual(number.to_list_of_numbers(      [1, 2, 3], "dummy", None), [1, 2, 3]) # From list
    #     self.assertEqual(number.to_list_of_numbers(      (1, 2, 3), "dummy", None), [1, 2, 3]) # From tuple
    #
    #     # Empty
    #     self.assertEqual(number.to_list_of_numbers([], "dummy", None), [])
    #
    #     # Length check
    #     self.assertEqual(                   number.to_list_of_numbers([1, 2, 3], "dummy", 3), [1, 2, 3]) # Success
    #     with self.assertRaises(ValueError): number.to_list_of_numbers([1, 2, 3], "dummy", 4)             # Failure
    #
    #     # Invalid values
    #     with self.assertRaises(TypeError ): number.to_list_of_numbers(None       , "dummy", None)
    #     with self.assertRaises(TypeError ): number.to_list_of_numbers(1          , "dummy", None)
    #     with self.assertRaises(TypeError ): number.to_list_of_numbers(""         , "dummy", None)
    #     with self.assertRaises(TypeError ): number.to_list_of_numbers("123"      , "dummy", None)
    #     with self.assertRaises(TypeError ): number.to_list_of_numbers([1, 2, "3"], "dummy", None)

    def test_to_number_helper(self):
        self.assertEqual(number.convert(42, "dummy"), 42) # Int
        self.assertEqual(number.convert(4.2, "dummy"), 4.2) # Float

        # Default
        self.assertEqual(number.convert(1, "dummy", default=999), 1)
        self.assertEqual(number.convert(None, "dummy", default=999), 999) # Default value

        # Invalid values (a default does not help)
        with self.assertRaises(TypeError): number.convert("", "dummy", default=999)
        with self.assertRaises(TypeError): number.convert([], "dummy", default=999)
