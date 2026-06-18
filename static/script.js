document.getElementById('addForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Ngăn việc tải lại trang mặc định của form

    // 1. Thu thập dữ liệu từ các ô nhập liệu bằng ID
    const productData = {
        ma_hang: document.getElementById('ma_hang').value,
        ten_hang: document.getElementById('ten_hang').value,
        loai_hang: document.getElementById('loai_hang').value,
        so_luong: parseInt(document.getElementById('so_luong').value),
        gia_nhap: parseFloat(document.getElementById('gia_nhap').value)
    };

    // 2. Gửi request API POST tới Flask
    fetch('/api/hang-hoa', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(productData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Thêm hàng hóa thành công!');
            window.location.reload(); // Tải lại trang để cập nhật bảng mới
        } else {
            alert('Lỗi từ hệ thống: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Không thể kết nối đến server Backend!');
    });
});