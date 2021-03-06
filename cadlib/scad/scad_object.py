from cadlib.util.tree import Node
from numbers import Number
from cadlib.scad.scad_file import ScadFile

def render_to_file(target, file_name, fn = None):
    ScadFile(target, fn).write(file_name)

class ScadObject():
    """
    Note that Vector is not supported as a type to enforce consistent value types. Use list instead.
    """

    def __init__(self, id, parameters, kw_parameters, children, comment = None):
        # Default values
        parameters    = parameters    or []
        kw_parameters = kw_parameters or []
        children      = children      or []

        # Parameter check
        if id is None:
            if parameters != []:
                raise ValueError("An empty ScadObject cannot have parameters")
            if kw_parameters != []:
                raise ValueError("An empty ScadObject cannot have keyword parameters")
        elif not isinstance(id, str):
            raise TypeError("id must be a string")
        elif id == "":
            raise ValueError("id must be a non-empty string")

        # Make sure that all keyword parameters are tuples of string and one other element
        for kw_parameter in kw_parameters:
            if not isinstance(kw_parameter, tuple) or len(kw_parameter) != 2 or not isinstance(kw_parameter[0], str):
                raise TypeError("Keyword parameters must be 2-tuples of (key, value), where key is a string")

        # Make sure that all children are instances of ScadObject
        for child in children:
            if not isinstance(child, ScadObject):
                raise TypeError("Children of SCAD objects must be SCAD objects.")

        self._id            = id
        self._parameters    = parameters
        self._kw_parameters = kw_parameters
        self._children      = children
        self._comment       = comment

    def replace_comment(self, comment):
        return ScadObject(self._id, self._parameters, self._kw_parameters, self._children, comment)

    def clear_comment(self, recursive = False):
        children = self._children
        if recursive:
            children = [child.clear_comment(True) for child in self._children]

        return ScadObject(self._id, self._parameters, self._kw_parameters, children, None)

    def comment(self, prepend = None, append = None, sep = "\n"):
        parts = (part for part in [prepend, self._comment, append] if part is not None)
        comment = sep.join(parts)
        return self.replace_comment(comment)



    def __eq__(self, other):
        return (isinstance(other, ScadObject)
            and other._id            == self._id
            and other._parameters    == self._parameters
            and other._kw_parameters == self._kw_parameters
            and other._children      == self._children
            and other._comment       == self._comment)

    def __repr__(self):
        if self._comment is None:
            return "ScadObject({}, {}, {}, {})".format(
                repr(self._id),
                repr(self._parameters),
                repr(self._kw_parameters),
                repr(self._children))
        else:
            return "ScadObject({}, {}, {}, {}, {})".format(
                repr(self._id),
                repr(self._parameters),
                repr(self._kw_parameters),
                repr(self._children),
                repr(self._comment))

    def to_tree(self):
        children_nodes = [child.to_tree() for child in self._children]

        return Node(self._head(), children_nodes)

    @staticmethod
    def render_value(value):
        if isinstance(value, Number):
            return str(value)

        elif isinstance(value, str):
            bs = "\\"  # Single backslash
            dq = '"'   # Double quote

            # The backslash is escaped first so we don't escape the backslashes that are part of an escape sequence.
            value = value.replace(bs  , bs + bs )  # \   -> \\
            value = value.replace('"' , bs + dq )  # "   -> \"
            value = value.replace('\n', bs + "n")  # LF  -> \n
            value = value.replace('\r', bs + "r")  # CR  -> \r
            value = value.replace('\t', bs + "t")  # TAB -> \t
            return dq + value + dq # Wrap in double-quotes

        elif isinstance(value, list):
            if len(value) == 0:
                raise ValueError("Value is an empty list")
            else:
                return "[" + ", ".join(ScadObject.render_value(x) for x in value) + "]"

        else:
            raise TypeError("Unknown value type")

    def _head(self):
        all_parameters  = [              self.render_value(parameter) for parameter  in self._parameters   ]
        all_parameters += [key + " = " + self.render_value(value)     for key, value in self._kw_parameters]

        if self._id is None:
            return "";
        else:
            return "{}({})".format(self._id, ", ".join(all_parameters))

    def _lines(self, indent, top_indent, simplify, include_comments):
        result = []

        if include_comments and self._comment is not None:
            for line in self._comment.split("\n"):
                result.append(top_indent + "// " + line)

        # Head line and start of block
        head_line = self._head()
        if len(self._children) == 0:
            head_line += ";"
            foot_line = None
        elif simplify and len(self._children) == 1:
            foot_line = None
        else:
            if head_line != "":
                head_line += " "
            head_line += "{"
            foot_line = "}"

        result.append(top_indent + head_line)

        # Children
        for child in self._children:
            for line in child._lines(indent, "", simplify, include_comments):
                result.append(top_indent + indent + line)

        # End of block
        if foot_line is not None:
            result.append(top_indent + foot_line)

        return result

    def to_scad(self):
        return self

    def to_code(self, indent = "    ", top_indent = "", inline = False, simplify = False):
        if inline:
            # Inline code does not contain comments
            return " ".join(self._lines("", "", simplify, False))
        else:
            return "\n".join(self._lines(indent, top_indent, simplify, True))
