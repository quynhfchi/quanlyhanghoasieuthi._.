class Statistics:
    def tao_dashboard_data(self, danh_sach):
        
        if not danh_sach or not danh_sach.head:
            return {
                "tong_so_hang": 0, "hang_dat_nhat": "Chưa có", "gia_dat_nhat": 0,
                "hang_re_nhat": "Chưa có", "gia_re_nhat": 0, "sap_het_han_count": 0, "sap_het": [],
                "tong_ton_kho": 0, "tong_gia_tri": 0, "ban_chay": "Chưa có",
                "ban_it": "Chưa có", "hang_ton_dong": [],
                "labels": [], "ton_kho": [], "da_ban": []
            }

 
        tong_so_hang = tong_ton_kho = tong_gia_tri = 0
        sap_het, ton_dong = [], []
        labels, ton_kho_chart, da_ban_chart = [], [], []
        
      
        max_gia = -1
        min_gia = float('inf')
        hang_dat = hang_re = None
        max_da_ban = -1
        hang_ban_chay = None

        current = danh_sach.head

        while current:
            item = current.data
            sl = int(item.get("so_luong", 0))
            gia = float(item.get("gia_nhap", 0))
            da_ban = int(item.get("da_ban", 0))
            ten = item.get("ten_hang", "Không tên")

           
            tong_so_hang += 1
            if sl <= 5:
                sap_het.append(item)
            
            if gia > max_gia:
                max_gia = gia
                hang_dat = item
            if gia < min_gia:
                min_gia = gia
                hang_re = item

         
            tong_ton_kho += sl
            tong_gia_tri += (sl * gia)
            
            if da_ban > max_da_ban:
                max_da_ban = da_ban
                hang_ban_chay = item
                
            if sl > 10 and da_ban == 0:
                ton_dong.append(item)

           
            labels.append(ten)
            ton_kho_chart.append(sl)
            da_ban_chart.append(da_ban)

            
            current = current.next

      
        if min_gia == float('inf'): min_gia = 0

        
        return {
           
            "tong_so_hang": tong_so_hang,
            "hang_dat_nhat": hang_dat.get("ten_hang") if hang_dat else "Chưa có",
            "gia_dat_nhat": max_gia,
            "hang_re_nhat": hang_re.get("ten_hang") if hang_re else "Chưa có",
            "gia_re_nhat": min_gia,
            "sap_het_han_count": len(sap_het),
            "sap_het": sap_het,
            
           
            "tong_ton_kho": tong_ton_kho,
            "tong_gia_tri": tong_gia_tri,
            "ban_chay": hang_ban_chay.get("ten_hang") if hang_ban_chay else "Chưa có",
            "ban_it": ton_dong[0].get("ten_hang") if ton_dong else "Chưa có",
            "hang_ton_dong": ton_dong,
            
           
            "labels": labels,
            "ton_kho": ton_kho_chart,
            "da_ban": da_ban_chart
        }