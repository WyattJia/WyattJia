class StackUnderflow(ValueError):

    pass



class Node():

    def __init__(self, elem, _next):
        self.elem = elem
        self._next = _next

    def __call__(self):
        return self.elem


class Stack():

    def __init__(self):
        self.top = None

    def is_empty(self):
        return self.top is None

    def top(self):
        if self.top is None:
            raise StackUnderflow
        return self.top.elem

    def push(self, elem):
        self.top = Node(elem, self.top)

    def pop(self):
        if self.top is None:
            raise StackUnderflow
        e = self.top.elem
        self.top = self.top._next
        return e


if __name__ == '__main__':
    st = Stack()
    st.push(1)
    st.push(5)
    print(st.pop())
    print(st.top())
    print(st.pop())
    print(st.is_empty())
    print(st.top())
