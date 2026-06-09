from data_structures.node import Node

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return

        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node

    def display(self):
        current = self.head
        items = []

        while current:
            items.append(current.data.to_dict())
            current = current.next

        return items