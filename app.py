from flask import Flask, render_template
from services.quan_ly_hang import QuanLyHang
from entities.thuc_pham import ThucPham

app = Flask(__name__)

quan_ly = QuanLyHang()

hang1 = ThucPham(
    "TP01",
    "Sữa",
    30000,
    10,
    "12/12/2026"
)

quan_ly.them_hang(hang1)

@app.route('/')
def home():
    danh_sach = quan_ly.hien_thi_hang()
    return render_template(
        'index.html',
        danh_sach=danh_sach
    )

if __name__ == '__main__':
    app.run(debug=True)