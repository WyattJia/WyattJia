class QueueUnderflow(ValueError):
    pass


class QueueNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class Queue():

    """Linked list based queue.
    """

    def __init__(self):
        self.size = 0
        self._head = None
        self._tail = None

    def __iter__(self):
        p = self._head
        while True:
            if  p is None:
                return
            yield p.value
            p = p.next


    def is_empty(self):
        return self.size == 0

    def peek(self):
        """Return the head element of queue.
        """
        if self.is_empty():
            raise QueueUnderflow

    def enqueue(self, value):
        node = QueueNode(value)
        if self._head is None:
            self._head = node
            self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self.size = self.size + 1

    def dequeue(self):
        if self.is_empty():
            raise QueueUnderflow
        value = self._head.value
        if self._head is self._tail:
            self._head = None
            self._tail = None
        else:
            self._head = self._head.next
        self.size = self.size - 1
        return value


if __name__ == '__main__':
    from random import randint
    q = Queue()
    for j in range(20):
        for i in range(randint(1, 20)):
            q.enqueue(i*3)

        for i in range(randint(1, 20)):
            if not q.is_empty():
                q.dequeue()
                # print(q.dequeue())
                # print('x' * 20)

    print('aaaa' * 100)
    for i in q:
        print(i)
    print('1' * 100)
    for i in range(0, q.size):
        print(q.dequeue())
    print('2' * 100)
    for i in q:
        print(i)

    q.enqueue(100)
    while not q.is_empty():
        print(q.dequeue())
