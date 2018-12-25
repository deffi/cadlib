class Table:
    """A table that can be pretty-printed."""

    def __init__(self, rows = None):
        """Initialize the table with the specified rows.

        The rows must be specified as iterable of iterables.
        """
        rows = rows or []

        self._rows = rows

    def format(self, column_sep = " ", row_sep = "\n", row_prefix = "", row_suffix = "", alignment = "l"):
        """Pretty-print the table.

        All columns are padded to equal length, according to the alignment
        parameter (which can be "l" or "r"). Columns are separated by column_sep
        and rows are separated by row_set. Additionally, each row is prefixed
        with row_prefix and suffixed with row_suffix.

        Rows do not have to be the same size. Incomplete rows will be filled
        with empty values.

        Limitations:
          * There is only one alignment parameter and all columns have the same
            alignment.
        """

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
