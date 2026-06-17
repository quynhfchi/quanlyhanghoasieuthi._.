import json
import os

class FileHandler:
    def __init__(self, file_path='data/inventory.json'):
        self.file_path = file_path

    def load_data(self):
        if not os.path.exists(self.file_path):
            return []
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            danh_sach = json.load(f)
            return danh_sach

    def save_data(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add_item(self, hang_moi):
        danh_sach = self.load_data()
        danh_sach.append(hang_moi)
        self.save_data(danh_sach)

    def delete_item(self, ma_hang_can_xoa):
        danh_sach = self.load_data()
        danh_sach_moi = [item for item in danh_sach if item['ma_hang'] != ma_hang_can_xoa]
        self.save_data(danh_sach_moi)