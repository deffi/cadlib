from cadlib.util.tree import Node

# /
# |- home
# |  |- waldo
# |  '- fred
# |- tmp
# '- var
#    '- lib

lib = Node("lib")
var = Node("var", [lib])
tmp = Node("tmp")
fred = Node("fred")
waldo = Node("waldo")
home = Node("home", [waldo, fred])
root = Node("/", [home, tmp, var])

print("Simple:")
print(root.format(indent="  ", top_indent="...."))
print("Pretty:")
print(root.format(indent=None, top_indent="...."))
