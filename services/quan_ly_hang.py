import os
import json
from datetime import date
from data_structures.doubly_linked_list import DoublyLinkedList
from utils.exceptions import DuplicateIDError, FileStorageError

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
                if not isinstance(data, list): raise FileStorageError()
                self.kho_hang.clear()
                for item in data:
                    self.kho_hang.append(item)
        except (json.JSONDecodeError, KeyError):
            raise FileStorageError("File dữ liệu bị hỏng!")

    def _ghi_du_lieu_vao_file(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.kho_hang.to_list(), f, ensure_ascii=False, indent=4)
        except Exception:
            raise FileStorageError("Không thể ghi dữ liệu!")

    def _khoi_tao_mac_dinh(self):
        du_lieu_mau = [
            {"ma_hang": "TP01", "ten_hang": "Sữa tươi", "loai_hang": "ThucPham", "so_luong": 100, "gia_nhap": 30000, "da_ban": 85, "ngay_nhap": "2026-06-01", "han_su_dung": "2026-06-25"},
            {"ma_hang": "DM01", "ten_hang": "Tủ lạnh", "loai_hang": "DienMay", "so_luong": 5, "gia_nhap": 12000000, "da_ban": 3, "ngay_nhap": "2026-05-10", "han_su_dung": None},
            {"ma_hang": "GD01", "ten_hang": "Chảo", "loai_hang": "GiaDung", "so_luong": 0, "gia_nhap": 250000, "da_ban": 2, "ngay_nhap": "2026-06-14", "han_su_dung": None}
        ]
        for item in du_lieu_mau:
            self.kho_hang.append(item)
        self._ghi_du_lieu_vao_file()

    def generate_ma_hang(self, loai_hang):
        prefix = "TP" if loai_hang == "ThucPham" else ("DM" if loai_hang == "DienMay" else "GD")
        max_num = 0
        danh_sach = self.kho_hang.to_list()
        for item in danh_sach:
            if item["ma_hang"].startswith(prefix):
                try:
                    num = int(item["ma_hang"][2:])
                    if num > max_num: max_num = num
                except: pass
        return f"{prefix}{max_num + 1:02d}"

    def lay_tat_ca(self):
        return self.kho_hang.to_list()

    def them_moi(self, item):
        danh_sach = self.kho_hang.to_list()
        for x in danh_sach:
            if x["ma_hang"].strip().lower() == item["ma_hang"].strip().lower():
                x["so_luong"] = int(x["so_luong"]) + int(item["so_luong"])
                self._ghi_du_lieu_vao_file()
                return
        
        item["ma_hang"] = self.generate_ma_hang(item["loai_hang"])
        item["ngay_nhap"] = date.today().strftime("%Y-%m-%d")
        if "da_ban" not in item: item["da_ban"] = 0
        self.kho_hang.append(item)
        self._ghi_du_lieu_vao_file()

    def cap_nhat_san_pham(self, ma_hang, new_data):
        danh_sach = self.kho_hang.to_list()
        for item in danh_sach:
            if item["ma_hang"].lower() == ma_hang.lower():
                item["ten_hang"] = new_data.get("ten_hang", item["ten_hang"])
                item["gia_nhap"] = float(new_data.get("gia_nhap", item["gia_nhap"]))
                
                nhap_them = int(new_data.get("nhap_them", 0))
                xuat_ban = int(new_data.get("xuat_ban", 0))
                
                item["so_luong"] = int(item["so_luong"]) + nhap_them - xuat_ban
                item["da_ban"] = int(item.get("da_ban", 0)) + xuat_ban
                
                if "han_su_dung" in new_data and new_data["han_su_dung"]:
                    item["han_su_dung"] = new_data["han_su_dung"]
                
                self.kho_hang.update_by_id(ma_hang, item)
                self._ghi_du_lieu_vao_file()
                return True
        return False

    def xoa_san_pham(self, ma_hang):
        if self.kho_hang.delete_by_id(ma_hang):
            self._ghi_du_lieu_vao_file()
            return True
        return False

    def sap_xep(self, key, reverse=False):
        self.kho_hang.sort(key=key, reverse=reverse)
        self._ghi_du_lieu_vao_file()
        return self.kho_hang.to_list()

    def tim_kiem_tuyen_tinh(self, tu_khoa, tieu_chi="all"):
        tu_khoa = tu_khoa.lower().strip()
        danh_sach = self.kho_hang.to_list()
        if not tu_khoa: return danh_sach
        ket_qua = []
        for item in danh_sach:
            if tieu_chi == "all":
                if tu_khoa in item.get("ma_hang", "").lower() or tu_khoa in item.get("ten_hang", "").lower():
                    ket_qua.append(item)
            elif tu_khoa in str(item.get(tieu_chi, "")).lower():
                ket_qua.append(item)
        return ket_qua

    def tim_kiem_nhi_phan_theo_ma(self, ma_can_tim):
        self.kho_hang.sort(key="ma_hang", reverse=False)
        danh_sach = self.kho_hang.to_list()
        left, right = 0, len(danh_sach) - 1
        while left <= right:
            mid = (left + right) // 2
            if danh_sach[mid]["ma_hang"].lower() == ma_can_tim.lower():
                return [danh_sach[mid]]
            elif danh_sach[mid]["ma_hang"].lower() < ma_can_tim.lower():
                left = mid + 1
            else:
                right = mid - 1
        return []