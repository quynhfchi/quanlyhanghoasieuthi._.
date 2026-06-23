from flask import Flask, render_template, request, jsonify
from datetime import datetime
from services.quan_ly_hang import QuanLyHangHoa
from utils.exceptions import DuplicateIDError, FileStorageError
from utils.statistics import Statistics 
app = Flask(__name__)

try:
    quan_ly_kho = QuanLyHangHoa()
    thong_ke_tool = Statistics() 
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
    danh_sach_dll = quan_ly_kho.kho_hang
    danh_sach_hien_thi = danh_sach_dll.to_list()
    
    thong_ke_data = thong_ke_tool.tao_dashboard_data(danh_sach_dll)
    if thong_ke_data is None:
        thong_ke_data = {"labels": [], "ton_kho": [], "da_ban": [], "tong_so_hang": 0}

    return render_template(
        'index.html',
        danh_sach=danh_sach_hien_thi,
        thong_ke=thong_ke_data
    )
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
        tu_khoa = data.get('keyword', '').strip()
        tieu_chi = data.get('criteria', 'all')
        
        if not tu_khoa and tieu_chi == 'all':
            ket_qua = quan_ly_kho.lay_tat_ca()
        else:
            if tieu_chi == "ma_hang":
                ket_qua = quan_ly_kho.tim_kiem_nhi_phan_theo_ma(tu_khoa)
            else:
                ket_qua = quan_ly_kho.tim_kiem_tuyen_tinh(tu_khoa, tieu_chi)
        
        return jsonify({"success": True, "data": ket_qua if ket_qua else []})

    return jsonify({"success": False, "message": "Action không hợp lệ"}), 400

if __name__ == '__main__':
    app.run(debug=True)