import os
import json
from datetime import date
from data_structures.doubly_linked_list import DoublyLinkedList
from utils.exceptions import FileStorageError

class QuanLyHangHoa:
    def __init__(self, file_path="data/kho_hang.json"):
        self.kho_hang = DoublyLinkedList()
        self.file_path = file_path
        self._doc_du_lieu_tu_file()

    def _doc_du_lieu_tu_file(self):
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            self._khoi_tao_mac_dinh()
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.kho_hang.clear()
                for item in data: self.kho_hang.append(item)
        except: raise FileStorageError("File dữ liệu bị hỏng!")

    def _ghi_du_lieu_vao_file(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.kho_hang.to_list(), f, ensure_ascii=False, indent=4)
        except: raise FileStorageError("Không thể ghi dữ liệu!")

    def _khoi_tao_mac_dinh(self):
        du_lieu_mau = [
            {"ma_hang": "TP01", "ten_hang": "Sữa tươi", "loai_hang": "ThucPham", "so_luong": 100, "gia_nhap": 30000, "da_ban": 85, "ngay_nhap": "2026-06-01", "han_su_dung": "2026-06-25"},
            {"ma_hang": "DM01", "ten_hang": "Tủ lạnh", "loai_hang": "DienMay", "so_luong": 5, "gia_nhap": 12000000, "da_ban": 3, "ngay_nhap": "2026-05-10", "han_su_dung": None}
        ]
        for item in du_lieu_mau: self.kho_hang.append(item)
        self._ghi_du_lieu_vao_file()

    def them_moi(self, item):
        node = self.kho_hang.find_node_by_id(item["ma_hang"])
        if node:
            node.data["so_luong"] = int(node.data["so_luong"]) + int(item["so_luong"])
        else:
            item["ngay_nhap"] = date.today().strftime("%Y-%m-%d")
            self.kho_hang.append(item)
        self._ghi_du_lieu_vao_file()

    def cap_nhat_san_pham(self, ma_hang, new_data):
        node = self.kho_hang.find_node_by_id(ma_hang)
        if node:
            d = node.data
            d["ten_hang"] = new_data.get("ten_hang", d["ten_hang"])
            d["gia_nhap"] = float(new_data.get("gia_nhap", d["gia_nhap"]))
            d["so_luong"] = int(d["so_luong"]) + int(new_data.get("nhap_them", 0)) - int(new_data.get("xuat_ban", 0))
            d["da_ban"] = int(d.get("da_ban", 0)) + int(new_data.get("xuat_ban", 0))
            self._ghi_du_lieu_vao_file()
            return True
        return False

    def xoa_san_pham(self, ma_hang):
        if self.kho_hang.delete_by_id(ma_hang):
            self._ghi_du_lieu_vao_file()
            return True
        return False

    def sap_xep(self, key, reverse=False):
        def cleanup_key(item):
            val = item.get(key, "")
            if key in ["gia_nhap", "so_luong"]:
                try:
                    return float(str(val).replace(",", "").replace(".", ""))
                except (ValueError, TypeError):
                    return 0.0
            return str(val).lower() if val else ""
            
        self.kho_hang.sort(key=cleanup_key, reverse=reverse)
        return self.kho_hang.to_list()
    
    def tim_kiem_don_gian(self, tu_khoa, tieu_chi):
        ket_qua = []
        danh_sach = self.kho_hang.to_list()
        tu_khoa = tu_khoa.lower()

        for item in danh_sach:
            ma_hang = str(item.get("ma_hang", "")).lower()
            ten_hang = str(item.get("ten_hang", "")).lower()
            loai_hang = item.get("loai_hang", "")

            match_keyword = (tu_khoa in ma_hang or tu_khoa in ten_hang)
            match_criteria = (tieu_chi == "all" or loai_hang == tieu_chi)

            if match_keyword and match_criteria:
                ket_qua.append(item)
        return ket_qua