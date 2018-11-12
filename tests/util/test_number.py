import unittest
from cadlib.util.vector import Vector
from cadlib.util.number import to_number, to_list_of_numbers

class TestNumber(unittest.TestCase):
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

    def test_to_number_helper(self):
        self.assertEqual(to_number(42, "dummy"), 42) # Int
        self.assertEqual(to_number(4.2, "dummy"), 4.2) # Float

        self.assertEqual(to_number(None, "dummy", default=999), 999) # Default value

        # TODO re-enable or remove
        #with self.assertRaises(TypeError): to_number2(None, 999, "dummy", []) # No default value

        # Invalid values
        with self.assertRaises(TypeError): to_number("", "dummy", default=999)
        with self.assertRaises(TypeError): to_number([], "dummy", default=999)
