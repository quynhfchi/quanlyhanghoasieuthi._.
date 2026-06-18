from flask import Flask, render_template, request, jsonify
from datetime import datetime
from services.quan_ly_hang import QuanLyHangHoa
from utils.exceptions import DuplicateIDError, FileStorageError

app = Flask(__name__)

try:
    quan_ly_kho = QuanLyHangHoa()
except Exception as e:
    print(f"Loi khoi tao: {str(e)}")
    exit(1)

@app.route('/api/hang-hoa', methods=['POST'])
def them_hang_hoa():
    try:
        data = request.get_json()
        quan_ly_kho.them_moi(data)
        return jsonify({"success": True, "message": "Thêm sản phẩm thành công"})
    except DuplicateIDError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/hang-hoa/<ma_hang>', methods=['PUT'])
def sua_hang_hoa(ma_hang):
    try:
        data = request.get_json()
        if quan_ly_kho.cap_nhat_san_pham(ma_hang, data):
            return jsonify({"success": True, "message": "Cập nhật thành công"})
        return jsonify({"success": False, "message": "Không tìm thấy sản phẩm"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
        
@app.route('/api/hang-hoa/<ma_hang>', methods=['DELETE'])
def xoa_hang_hoa(ma_hang):
    try:
        if quan_ly_kho.xoa_san_pham(ma_hang):
            return jsonify({"success": True, "message": "Xóa thành công"})
        return jsonify({"success": False, "message": "Không tìm thấy sản phẩm"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/')
def home():
    danh_sach = quan_ly_kho.lay_tat_ca()
    ngay_hien_tai = datetime.now().date()

    so_luong_sap_het_han = 0
    gia_cao_nhat = 0
    gia_thap_nhat = float('inf') if danh_sach else 0
    mat_hang_ban_chay = "Chưa có"
    mat_hang_ban_it = "Chưa có"
    max_ban = -1
    min_ban = float('inf') if danh_sach else 0

    for item in danh_sach:
        item["sap_het_han"] = False
        item["het_hang"] = (int(item.get("so_luong", 0)) == 0)

        if item.get("loai_hang") == "ThucPham" and item.get("han_su_dung"):
            try:
                hsd = datetime.strptime(str(item["han_su_dung"]), "%Y-%m-%d").date()
                if 0 <= (hsd - ngay_hien_tai).days <= 30:
                    item["sap_het_han"] = True
                    so_luong_sap_het_han += 1
            except ValueError:
                pass

        gia = float(item.get("gia_nhap", 0))
        if gia > gia_cao_nhat: gia_cao_nhat = gia
        if gia < gia_thap_nhat: gia_thap_nhat = gia

        da_ban = int(item.get("da_ban", 0))
        if da_ban > max_ban:
            max_ban = da_ban
            mat_hang_ban_chay = item["ten_hang"]
        if da_ban < min_ban:
            min_ban = da_ban
            mat_hang_ban_it = item["ten_hang"]

    if not danh_sach: gia_thap_nhat = 0

    thong_ke_data = {
        "labels": [item.get("ten_hang", "Không tên") for item in danh_sach],
        "ton_kho": [item.get("so_luong", 0) for item in danh_sach],
        "da_ban": [item.get("da_ban", 0) for item in danh_sach],
        "sap_het_han_count": so_luong_sap_het_han,
        "gia_max": gia_cao_nhat,
        "gia_min": gia_thap_nhat,
        "ban_chay": mat_hang_ban_chay,
        "ban_it": mat_hang_ban_it
    }

    return render_template('index.html', danh_sach=danh_sach, thong_ke=thong_ke_data)

@app.route('/api/sap-xep-tim-kiem', methods=['POST'])
def handling_features():
    data = request.get_json()
    action = data.get('action')

    if action == 'sort':
        tieu_chi = data.get('tieu_chi')
        kieu_sap_xep = data.get('kieu')
        ket_qua = quan_ly_kho.sap_xep(tieu_chi, reverse=(kieu_sap_xep == 'desc'))
        return jsonify({"success": True, "data": ket_qua})

    elif action == 'search':
        tu_khoa = data.get('keyword', '')
        tieu_chi = data.get('criteria', 'all')
        if tieu_chi == "ma_hang":
            ket_qua = quan_ly_kho.tim_kiem_nhi_phan_theo_ma(tu_khoa)
        else:
            ket_qua = quan_ly_kho.tim_kiem_tuyen_tinh(tu_khoa, tieu_chi)
        return jsonify({"success": True, "data": ket_qua})

    return jsonify({"success": False, "message": "Action không hợp lệ"}), 400

if __name__ == '__main__':
    app.run(debug=True)