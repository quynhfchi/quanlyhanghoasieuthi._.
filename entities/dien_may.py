from entities.hang_hoa import HangHoa

class DienMay(HangHoa):
    def __init__(self, ma_hang, ten_hang, gia, so_luong, bao_hanh):
        super().__init__(ma_hang, ten_hang, gia, so_luong)
        self.bao_hanh = bao_hanh

    def to_dict(self):
        data = super().to_dict()
        data["bao_hanh"] = self.bao_hanh
        return data