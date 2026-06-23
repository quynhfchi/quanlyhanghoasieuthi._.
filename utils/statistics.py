class Statistics:

    def tong_so_hang(self, danh_sach):
        count = 0
        current = danh_sach.head

        while current:
            count += 1
            current = current.next

        return count

    def hang_dat_nhat(self, danh_sach):
        if not danh_sach or not danh_sach.head:
            return None

        current = danh_sach.head
        hang_dat_nhat = current.data

        while current:
            if current.data.get("gia_nhap", 0) > hang_dat_nhat.get("gia_nhap", 0):
                hang_dat_nhat = current.data

            current = current.next

        return hang_dat_nhat

    def hang_re_nhat(self, danh_sach):
        if not danh_sach or not danh_sach.head:
            return None

        current = danh_sach.head
        hang_re_nhat = current.data

        while current:
            if current.data.get("gia_nhap", 0) < hang_re_nhat.get("gia_nhap", 0):
                hang_re_nhat = current.data

            current = current.next

        return hang_re_nhat

    def hang_sap_het(self, danh_sach):
        ket_qua = []
        current = danh_sach.head

        while current:
            if current.data.get("so_luong", 0) <= 5:
                ket_qua.append(current.data)

            current = current.next

        return ket_qua

    def tong_so_luong_ton_kho(self, danh_sach):
        tong = 0
        current = danh_sach.head

        while current:
            tong += current.data.get("so_luong", 0)
            current = current.next

        return tong

    def tong_gia_tri_kho(self, danh_sach):
        tong = 0
        current = danh_sach.head

        while current:
            so_luong = current.data.get("so_luong", 0)
            gia_nhap = current.data.get("gia_nhap", 0)

            tong += so_luong * gia_nhap
            current = current.next

        return tong

    def hang_ban_chay(self, danh_sach):
        if not danh_sach or not danh_sach.head:
            return None

        current = danh_sach.head
        hang_ban_chay = current.data

        while current:
            if current.data.get("da_ban", 0) > hang_ban_chay.get("da_ban", 0):
                hang_ban_chay = current.data

            current = current.next

        return hang_ban_chay

    def hang_ton_dong(self, danh_sach):
        ket_qua = []
        current = danh_sach.head

        while current:
            so_luong = current.data.get("so_luong", 0)
            da_ban = current.data.get("da_ban", 0)

            if so_luong > 10 and da_ban == 0:
                ket_qua.append(current.data)

            current = current.next

        return ket_qua

    def canh_bao_nhap_hang(self, danh_sach):
        ket_qua = []
        current = danh_sach.head

        while current:
            so_luong = current.data.get("so_luong", 0)
            da_ban = current.data.get("da_ban", 0)

            if so_luong < 5 and da_ban > 20:
                ket_qua.append(current.data)

            current = current.next

        return ket_qua

    def thong_ke_theo_loai(self, danh_sach):
        ket_qua = {
            "ThucPham": 0,
            "DienMay": 0,
            "GiaDung": 0
        }

        current = danh_sach.head

        while current:
            loai = current.data.get("loai_hang")

            if loai in ket_qua:
                ket_qua[loai] += 1

            current = current.next

        return ket_qua

    def tao_dashboard_data(self, danh_sach):
        if not danh_sach or not danh_sach.head:
            return {
                "labels": [],
                "ton_kho": [],
                "da_ban": [],

                "tong_so_hang": 0,
                "tong_ton_kho": 0,
                "tong_gia_tri": 0,

                "sap_het_han_count": 0,
                "sap_het": [],               
                "hang_ton_dong": [],         

                "gia_max": 0,
                "gia_min": 0,

                "ban_chay": "Chưa có",
                "ban_it": "Chưa có",

                "canh_bao_nhap_hang": [],
                "thong_ke_loai": {
                    "ThucPham": 0,
                    "DienMay": 0,
                    "GiaDung": 0
                }
            }

        labels = []
        ton_kho = []
        da_ban = []

        current = danh_sach.head

        while current:
            item = current.data

            labels.append(item.get("ten_hang", "Không tên"))
            ton_kho.append(item.get("so_luong", 0))
            da_ban.append(item.get("da_ban", 0))

            current = current.next

        hang_dat = self.hang_dat_nhat(danh_sach)
        hang_re = self.hang_re_nhat(danh_sach)
        hang_banchay = self.hang_ban_chay(danh_sach)
        hang_tondong = self.hang_ton_dong(danh_sach)
        danh_sach_sap_het = self.hang_sap_het(danh_sach)

        return {
            "labels": labels,
            "ton_kho": ton_kho,
            "da_ban": da_ban,

            "tong_so_hang": self.tong_so_hang(danh_sach),
            "tong_ton_kho": self.tong_so_luong_ton_kho(danh_sach),
            "tong_gia_tri": self.tong_gia_tri_kho(danh_sach),

            "sap_het_han_count": len(danh_sach_sap_het),
            "sap_het": danh_sach_sap_het,      
            "hang_ton_dong": hang_tondong,      

            "gia_max": float(hang_dat.get("gia_nhap", 0)) if hang_dat else 0,
            "gia_min": float(hang_re.get("gia_nhap", 0)) if hang_re else 0,

            "ban_chay": (
                hang_banchay.get("ten_hang", "Chưa có")
                if hang_banchay else "Chưa có"
            ),

            "ban_it": (
                hang_tondong[0].get("ten_hang", "Chưa có")
                if hang_tondong else "Chưa có"
            ),

            "canh_bao_nhap_hang": self.canh_bao_nhap_hang(danh_sach),

            "thong_ke_loai": self.thong_ke_theo_loai(danh_sach)
        }