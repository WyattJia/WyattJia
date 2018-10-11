class NodeError(ValueError):
    pass


class Node(object):

    def __init__(self, data, left, right):
        self.data = data
        self.left = left
        self.right = right



class Tree(object):

    def __init__(self):
        self._root = None

    def is_empty(self):
        return self._root == None

    def set_root(self, root_node):
        self._root = root_node

    def set_left(self, left):
        self._root.left = left

    def set_right(self, right):
        self._root.right = right

    def root(self):
        return self._root

    def left(self):
        return self._root.left

    def right(self):
        return self._root.right

