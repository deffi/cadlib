class Table:
    def __init__(self, rows = None):
        rows = rows or []

        self._rows = rows

    def format(self, column_sep = " ", row_sep = "\n", row_prefix = "", row_suffix = "", alignment = "l"):
        if len(self._rows) == 0:
            return "" # No rows, not even an empty row

        # Determine the total number of columns (i. e. the maximum length of any
        # row)
        column_count = max(len(row) for row in self._rows)

        # Converts a cell value to a string
        def format_cell(value):
            if value is None:
                return ""
            else:
                return str(value)

        # Pads a row to the maximum row length with None values
        def pad_row(row):
            return row + [None] * (column_count - len(row))

        # Create a list of lists with cell strings and equal-length rows
        rows = [[format_cell(value) for value in pad_row(row)] for row in self._rows]

        # Determine the column lengths
        lengths = [[len(cell) for cell in row] for row in rows]
        column_lengths = [max(lengths_by_column) for lengths_by_column in zip(*lengths)]

        # Pad the values
        def pad(value, length):
            if alignment == "l":
                return value.ljust(length)
            elif alignment == "r":
                return value.rjust(length)
            else:
                return value
        padded = [[pad(cell, length) for cell,length in zip(row, column_lengths)] for row in rows]

        row_strings = [row_prefix + column_sep.join(row) + row_suffix for row in padded]
        return row_sep.join(row_strings)

if __name__ == "__main__":
    table = Table([
        ["x", "y", "z"], # Shorter row
        [1, 222, 33, 4.5],
        [11, 2, 333, 45.67],
        ["aaa", "bb", "c"], # Shorter row
    ])

    print(table.format())
    print()
    print(table.format(column_sep="|", row_prefix = "(", row_suffix = ")"))


