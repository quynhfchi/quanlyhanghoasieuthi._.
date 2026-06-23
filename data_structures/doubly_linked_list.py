from data_structures.node import Node

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return
        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def clear(self):
        self.head = None
        self.tail = None

    def _get_middle(self, head):
        if not head:
            return head
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def _sorted_merge(self, a, b, key, reverse=False):
        if not a: return b
        if not b: return a

        val_a = a.data.get(key)
        val_b = b.data.get(key)

        if isinstance(val_a, str) and isinstance(val_b, str):
            val_a = val_a.lower()
            val_b = val_b.lower()

        condition = (val_a > val_b) if reverse else (val_a <= val_b)

        if condition:
            result = a
            result.next = self._sorted_merge(a.next, b, key, reverse)
            if result.next:
                result.next.prev = result
            result.prev = None
        else:
            result = b
            result.next = self._sorted_merge(a, b.next, key, reverse)
            if result.next:
                result.next.prev = result
            result.prev = None
        return result

    def _merge_sort(self, head, key, reverse=False):
        if not head or not head.next:
            return head

        middle = self._get_middle(head)
        next_to_middle = middle.next
        middle.next = None
        if next_to_middle:
            next_to_middle.prev = None

        left = self._merge_sort(head, key, reverse)
        right = self._merge_sort(next_to_middle, key, reverse)

        return self._sorted_merge(left, right, key, reverse)

    def sort(self, key, reverse=False):
        if not self.head or not self.head.next:
            return
        self.head = self._merge_sort(self.head, key, reverse)
        current = self.head
        while current and current.next:
            current = current.next
        self.tail = current
    def delete_by_id(self, ma_hang):
        current = self.head
        while current:
            if current.data.get("ma_hang") == ma_hang:
                # Nếu là node đầu
                if current == self.head:
                    self.head = current.next
                    if self.head: self.head.prev = None
                # Nếu là node cuối
                elif current == self.tail:
                    self.tail = current.prev
                    self.tail.next = None
                # Nếu ở giữa
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                return True
            current = current.next
        return False

    def update_by_id(self, ma_hang, new_data):
        current = self.head
        while current:
            if current.data.get("ma_hang") == ma_hang:
                current.data = new_data
                return True
            current = current.next
        return False
    
    def update_by_id(self, ma_hang, new_data):
        current = self.head
        while current:
            if current.data.get("ma_hang") == ma_hang:
                current.data = new_data
                return True
            current = current.next
        return False