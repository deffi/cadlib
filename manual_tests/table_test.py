from cadlib.util.table import Table

table = Table([
    ["x", "y", "z"],  # Shorter row
    [1, 222, 33, 4.5],
    [11, 2, 333, 45.67],
    ["aaa", "bb", "c"],  # Shorter row
])

print(table.format())
print()
print(table.format(column_sep="|", row_prefix="(", row_suffix=")"))


