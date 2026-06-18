import json
import os
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
                if not isinstance(data, list):
                    raise FileStorageError()
                self.kho_hang.clear()
                for item in data:
                    self.kho_hang.append(item)
        except (json.JSONDecodeError, KeyError):
            raise FileStorageError("File dữ liệu bị hỏng, không đúng định dạng cấu trúc hàng hóa!")

    def _ghi_du_lieu_vao_file(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.kho_hang.to_list(), f, ensure_ascii=False, indent=4)
        except Exception:
            raise FileStorageError("Không thể ghi dữ liệu mới cập nhật xuống thiết bị lưu trữ!")

    def _khoi_tao_mac_dinh(self):
        du_lieu_mau = [
            {"ma_hang": "TP01", "ten_hang": "Sữa tươi tiệt trùng", "loai_hang": "ThucPham", "so_luong": 100, "gia_nhap": 30000, "da_ban": 85, "ngay_nhap": "2026-06-01", "han_su_dung": "2026-06-25"},
            {"ma_hang": "DM01", "ten_hang": "Tủ lạnh Inverter", "loai_hang": "DienMay", "so_luong": 5, "gia_nhap": 12000000, "da_ban": 3, "ngay_nhap": "2026-05-10", "han_su_dung": None},
            {"ma_hang": "GD01", "ten_hang": "Chảo chống dính Kangaroo", "loai_hang": "GiaDung", "so_luong": 0, "gia_nhap": 250000, "da_ban": 2, "ngay_nhap": "2026-06-14", "han_su_dung": None}
        ]
        for item in du_lieu_mau:
            self.kho_hang.append(item)
        self._ghi_du_lieu_vao_file()

    def lay_tat_ca(self):
        return self.kho_hang.to_list()

    def them_moi(self, item):
        danh_sach = self.kho_hang.to_list()
        for x in danh_sach:
            if x["ma_hang"].strip().lower() == item["ma_hang"].strip().lower():
                raise DuplicateIDError(item["ma_hang"])
        
        self.kho_hang.append(item)
        self._ghi_du_lieu_vao_file()

    def sap_xep(self, key, reverse=False):
        self.kho_hang.sort(key=key, reverse=reverse)
        self._ghi_du_lieu_vao_file()
        return self.kho_hang.to_list()

    def tim_kiem_tuyen_tinh(self, tu_khoa, tieu_chi="all"):
        tu_khoa = tu_khoa.lower().strip()
        danh_sach_goc = self.kho_hang.to_list()
        if not tu_khoa:
            return danh_sach_goc

        ket_qua = []
        for item in danh_sach_goc:
            if tieu_chi == "ten_hang" and tu_khoa in item.get("ten_hang", "").lower():
                ket_qua.append(item)
            elif tieu_chi == "loai_hang" and tu_khoa in item.get("loai_hang", "").lower():
                ket_qua.append(item)
            elif tieu_chi == "all":
                if (tu_khoa in item.get("ma_hang", "").lower() or 
                    tu_khoa in item.get("ten_hang", "").lower() or 
                    tu_khoa in item.get("loai_hang", "").lower()):
                    ket_qua.append(item)
        return ket_qua

    def tim_kiem_nhi_phan_theo_ma(self, ma_can_tim):
        ma_can_tim = ma_can_tim.strip().lower()
        self.kho_hang.sort(key="ma_hang", reverse=False)
        danh_sach_da_sort = self.kho_hang.to_list()

        left = 0
        right = len(danh_sach_da_sort) - 1

        while left <= right:
            mid = (left + right) // 2
            ma_mid = danh_sach_da_sort[mid]["ma_hang"].strip().lower()

            if ma_mid == ma_can_tim:
                return [danh_sach_da_sort[mid]]
            elif ma_mid < ma_can_tim:
                left = mid + 1
            else:
                right = mid - 1
        return []