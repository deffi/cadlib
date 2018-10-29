import unittest

from cadlib.util.tree import Node

class TestTree(unittest.TestCase):
    def test_construction(self):
        Node(0, None)
        Node(0, [])
        Node(0, [Node(1)])

        with self.assertRaises(TypeError): Node(0, Node(1))
        with self.assertRaises(TypeError): Node(0, [1])
        with self.assertRaises(TypeError): Node(0, [""])

    def test_equality(self):
        # Same object
        n = Node(0, None)     ; self.assertEqual(n, n)
        n = Node(0, [Node(1)]); self.assertEqual(n, n)

        # Equal object
        self.assertEqual(Node(0, None), Node(0, None))
        self.assertEqual(Node(0, [Node(1)]), Node(0, [Node(1)]))


        # Different data
        self.assertNotEqual(Node(0, None), Node(1, None))
        self.assertNotEqual(Node(0, [Node(1)]), Node(0, [Node(2)]))


    def test_repr(self):
        string = "Node(0, [Node(1, []), Node(2, [])])"
        self.assertEqual(repr(eval(string)), string)

    def test_format(self):
        tree = Node(1, [
            Node(2, [
                Node(3),
                Node(4),
            ]),
            Node(5, [
                Node(6)
            ]),
        ]);

        self.assertEqual(tree.format("  ", "    "),
            "    1\n"
            "      2\n"
            "        3\n"
            "        4\n"
            "      5\n"
            "        6"
         )

        self.assertEqual(tree.format(None, "    "),
            "    1\n"
            "    |-- 2\n"
            "    |   |-- 3\n"
            "    |   '-- 4\n"
            "    '-- 5\n"
            "        '-- 6"
         )
