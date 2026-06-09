class HangHoa:
    def __init__(self, ma_hang, ten_hang, gia, so_luong):
        self.ma_hang = ma_hang
        self.ten_hang = ten_hang
        self.gia = gia
        self.so_luong = so_luong

    def to_dict(self):
        return {
            "ma_hang": self.ma_hang,
            "ten_hang": self.ten_hang,
            "gia": self.gia,
            "so_luong": self.so_luong
        }