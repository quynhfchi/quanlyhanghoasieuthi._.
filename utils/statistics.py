class Statistics:
    def tong_so_hang(self, danh_sach):
        return len(danh_sach)

    def hang_dat_nhat(self, danh_sach):
        return max(danh_sach, key=lambda x: x["gia"])

    def hang_re_nhat(self, danh_sach):
        return min(danh_sach, key=lambda x: x["gia"])

    def hang_sap_het(self, danh_sach):
        ket_qua = []

        for item in danh_sach:
            if item["so_luong"] <= 5:
                ket_qua.append(item)

        return ket_qua