class DuplicateIDError(Exception):
    def __init__(self, ma_hang):
        self.ma_hang = ma_hang
        super().__init__(f"Lỗi: Mã hàng hóa '{ma_hang}' đã tồn tại trong hệ thống!")

class FileStorageError(Exception):
    def __init__(self, message="Lỗi cấu trúc hoặc không thể truy cập file dữ liệu kho hàng!"):
        super().__init__(message)