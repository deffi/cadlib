from cadlib.util import Vector

class Anchor:
    def __init__(self, object, name, position): # TODO remove name?
        self._object = object
        self._name = name
        self._position = Vector.convert(position, "position", required_length=3)

    @property
    def object(self):
        return self._object

    # @property
    # def name(self):
    #     return self._name

    @property
    def position(self):
        return self._position

    def at(self, reference):
        return self.object.translate(reference.position - self.position)
