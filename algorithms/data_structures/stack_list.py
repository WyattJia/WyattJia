class StackUnderflow(ValueError):
    pass


class Stack(object):

    def __init__(self):
        self.elems = []

    def is_empty(self):
        return self.elems == []

    def top(self):
        if self.elems == []:
            raise StackUnderflow
        return self.elems[len(self.elems)-1]

    def push(self, elem):
        self.elems.append(elem)

    def pop(self):
        if self.elems == []:
            raise StackUnderflow
        return self.elems.pop()


if __name__ == '__main__':
    s = Stack()
    s.push(1)
    s.push(5)
    print(s.pop())
    print(s.top())
    print(s.pop())
    print(s.is_empty())
    s.top()

