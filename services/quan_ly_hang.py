from data_structures.doubly_linked_list import DoublyLinkedList

class QuanLyHang:
    def __init__(self):
        self.danh_sach = DoublyLinkedList()

    def them_hang(self, hang):
        self.danh_sach.append(hang)

    def hien_thi_hang(self):
        return self.danh_sach.display()