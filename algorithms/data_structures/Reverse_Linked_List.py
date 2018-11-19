class Node:

    def __init__(self, value):
        self.data = value
        self._next = None


# 循环

def reverse(head):

    next_node = head._next
    prev = head

    # 第一个节点变成最后一个节点
    prev._next = None

    while True:
        head = next_node
        next_node = head._next

        # 反转
        head._next = prev

        if next_node == None:
            break
        prev = head_node
    return head


# 递归

def recursive_reverse(reversed_node, new_node):
    if new_node == None:
        print(reversed_node)
        return reversed_node

    next_node = new_node._next
    new_node.next = reversed_node
    return recursive_reverse(new_node, next_node)


if __name__ == '__main__':

    head_node = Node(0)
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)

    head_node.next = node1
    node1.next = node2
    node2.next = node3
    node3.next = node4

    # 循环法
    # head_node = reverse(head_node)

    # 递归法
    new_node = head_node.next
    head_node.next = None
    head_node = recursive_reverse(head_node, new_node)

    # 打印反转后的链表
    while head_node != None:
        print(head_node.data)
        head_node = head_node.next

