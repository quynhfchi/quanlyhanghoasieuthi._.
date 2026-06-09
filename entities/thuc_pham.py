from entities.hang_hoa import HangHoa

class ThucPham(HangHoa):
    def __init__(self, ma_hang, ten_hang, gia, so_luong, han_su_dung):
        super().__init__(ma_hang, ten_hang, gia, so_luong)
        self.han_su_dung = han_su_dung

    def to_dict(self):
        data = super().to_dict()
        data["han_su_dung"] = self.han_su_dung
        return data