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

    print(f"DEBUG DATA: {type(thong_ke_data)} - {thong_ke_data}")

    return render_template(
        'index.html',
        danh_sach=danh_sach_hien_thi,
        thong_ke=thong_ke_data
    )

@app.route('/api/sap-xep-tim-kiem', methods=['POST'])
def handling_features():
    data = request.get_json()
    sort_type = data.get('sort_type', '') 
    ket_qua = quan_ly_kho.tim_kiem_don_gian(data.get('keyword', ''), data.get('criteria', 'all'))
    print (f"DEBUG: Dữ liệu nhận từ tim_kiem_don_gian: {ket_qua[:2]}"
           )
    if sort_type == 'gia_asc':
        ket_qua = sorted(ket_qua, key=lambda x: float(x.get('gia_nhap', 0)), reverse=False)
    elif sort_type == 'gia_desc':
        ket_qua = sorted(ket_qua, key=lambda x: float(x.get('gia_nhap', 0)), reverse=True)
    elif sort_type == 'sl_desc':
        ket_qua = sorted(ket_qua, key=lambda x: float(x.get('so_luong', 0)), reverse=True)
            
    return jsonify({"success": True, "data": ket_qua})

if __name__ == '__main__':
    app.run(debug=True)