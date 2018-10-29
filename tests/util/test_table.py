import unittest

from cadlib.util.table import Table

class TestTable(unittest.TestCase):
    def test_construction(self):
        self.assertEqual(Table(    )._rows, [])
        self.assertEqual(Table(None)._rows, [])
        self.assertEqual(Table([]  )._rows, [])

    def test_format(self):
        self.assertEqual(Table().format(), "")

        values = [
            [1, 2, 3],
            [444, 555],
            [None, 66],
        ]

        self.assertEqual(Table(values).format(column_sep="|", row_sep="\n", row_prefix="(", row_suffix=")", alignment="r"),
            "(  1|  2|3)\n"
            "(444|555| )\n"
            "(   | 66| )"
        )
        self.assertEqual(Table(values).format(column_sep="|", row_sep="\n", row_prefix="(", row_suffix=")", alignment="l"),
            "(1  |2  |3)\n"
            "(444|555| )\n"
            "(   |66 | )"
        )
        self.assertEqual(Table(values).format(column_sep="|", row_sep="\n", row_prefix="(", row_suffix=")", alignment=""),
            "(1|2|3)\n"
            "(444|555|)\n"
            "(|66|)"
         )
