from cadlib.util import Matrix

print("Empty matrix:")
print(Matrix())
print()

print("Full matrix:")
print(Matrix.from_rows([1, 0, 0, 0], [0, 22, 0, 0], [0, 0, 333, 0], [0, 0, 0, 1]))
