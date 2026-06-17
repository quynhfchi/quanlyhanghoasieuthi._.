class Validator:
    def kiem_tra_ma_trung(self, danh_sach, ma_hang):
        for item in danh_sach:
            if item["ma_hang"] == ma_hang:
                return True

        return False

    def kiem_tra_so_duong(self, gia_tri):
        return gia_tri > 0