class Node:
    def __init__(self, data, children = None):
        children = children or []

        for child in children:
            if not isinstance(child, Node):
                raise TypeError("Children for tree nodes must be tree nodes.")

        self._data     = data
        self._children = children

    def __repr__(self):
        return f"Node({self._data}, {self._children})"

    def __eq__(self, other):
        return (isinstance(other, Node)
                and self._data     == other._data
                and self._children == other._children)

    def lines(self, indent = None, top_indent = ""):
        '''Indent: indent string per level, or None for pretty-printing'''
        result = []
        result.append(top_indent + str(self._data))

        if indent is None:
            # Pretty printing:
            #   * Last child:     first line "'-", other lines "  "
            #   * Other children: first line "|-", other lines "| "
            for child in self._children[:-1]: # All children except the last
                lines = child.lines()
                for line in lines[:1]: result.append(top_indent + "|-- " + line) # First line
                for line in lines[1:]: result.append(top_indent + "|   " + line) # Other lines
            for child in self._children[-1:]: # Last child
                lines = child.lines()
                for line in lines[:1]: result.append(top_indent + "'-- " + line) # First line
                for line in lines[1:]: result.append(top_indent + "    " + line) # Other lines
        else:
            # Simple indenting
            result += list(top_indent + indent + line for child in self._children for line in child.lines(indent))

        return result

    def format(self, indent = None, top_indent = ""):
        '''Indent: indent string per level, or None for pretty-printing'''
        return "\n".join(self.lines(indent, top_indent))
