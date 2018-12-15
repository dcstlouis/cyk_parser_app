class Tree:

    def __init__(self, root):
        self.root = root

    def serialize(self):
        return self.root.serialize()


class Node:

    def __init__(self, label="Empty", left=None, right=None):
        self._label = label
        self._left = left
        self._right = right

    def __str__(self):
        return f"{self._label}"

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def children(self):
        return [self._left, self._right]

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @left.setter
    def left(self, node):
        self._left = node

    @right.setter
    def right(self, node):
        self._right = node

    def serialize(self):
        serialization = {}
        if self._left == None and self._right == None:
            serialization.update({'name':self._label})
        elif self._left == None:
            right = self._right.serialize()
            serialization.update({'name': self._label, 'children':[right]})
        elif self._right == None:
            left = self._left.serialize()
            serialization.update({'name': self._label, 'children': [left]})
        else:
            left = self._left.serialize()
            right = self._right.serialize()
            serialization.update({'name': self._label,'children': [left, right]})

        return serialization
