class Node:
    """A tree (node).

    All nodes (not just leaf nodes) can have data.
    """

    def __init__(self, data, children = None):
        """Create a tree node with the specified data and children.

        All children must be instances of Node. Data is arbitrary.
        """
        children = children or []

        for child in children:
            if not isinstance(child, Node):
                raise TypeError("Children for tree nodes must be tree nodes.")

        self._data     = data
        self._children = children

    def __repr__(self):
        return f"Node({self._data}, {self._children})"

    def __eq__(self, other):
        """Nodes are equal if both their data and children are equal."""
        return (isinstance(other, Node)
                and self._data     == other._data
                and self._children == other._children)

    def lines(self, indent = None, top_indent = ""):
        """Format the tree as a list of strings, one string for each node.

        If indent is None, the lines are prefixed with a line drawing of the
        tree structure. Otherwise, each level is prefixed with the corresponding
        number of copies of indent. In any case, each line is prefixed with
        top_indent.
        """
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
        """Format the tree as a single string.

        See the lines method for the interpretation of the parameters.
        """
        return "\n".join(self.lines(indent, top_indent))
