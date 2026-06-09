from entities.hang_hoa import HangHoa

class GiaDung(HangHoa):
    def __init__(self, ma_hang, ten_hang, gia, so_luong, chat_lieu):
        super().__init__(ma_hang, ten_hang, gia, so_luong)
        self.chat_lieu = chat_lieu

    def to_dict(self):
        data = super().to_dict()
        data["chat_lieu"] = self.chat_lieu
        return data