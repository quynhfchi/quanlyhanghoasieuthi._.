// 1. Xử lý thêm sản phẩm mới
document.getElementById('addProductForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const messageBox = document.getElementById('messageBox');
    
    const data = {
        ma_hang: document.getElementById('ma_hang').value,
        ten_hang: document.getElementById('ten_hang').value,
        loai_hang: document.getElementById('loai_hang').value,
        so_luong: parseInt(document.getElementById('so_luong').value) || 0,
        gia_nhap: parseFloat(document.getElementById('gia_nhap').value) || 0,
        han_su_dung: document.getElementById('han_su_dung').value || null
    };

    try {
        const response = await fetch('/api/hang-hoa', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            messageBox.style.color = "green";
            messageBox.innerText = "✅ " + result.message;
            setTimeout(() => { location.reload(); }, 1500);
        } else {
            messageBox.style.color = "red";
            messageBox.innerText = "❌ Lỗi: " + result.message;
        }
    } catch (error) {
        messageBox.style.color = "red";
        messageBox.innerText = "❌ Không thể kết nối tới máy chủ!";
    }
});

// 2. Hàm chuyển tab
function switchTab(tabId, element) {
    document.querySelectorAll('.tab-section').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.menu-item').forEach(m => m.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    if(element) element.classList.add('active');
}

// 3. Hàm xử lý hiển thị ô HSD
function handleTypeChange(value) {
    const container = document.getElementById('hsd_container');
    if (container) {
        container.style.display = (value === 'ThucPham') ? 'block' : 'none';
    }
}

// 4. Hàm mở Modal Sửa
function openEditModal(ma, ten, gia, loai) {
    document.getElementById('edit_ma_hang').value = ma;
    document.getElementById('edit_ten').value = ten;
    document.getElementById('edit_gia').value = gia;
    document.getElementById('edit_hsd_container').style.display = (loai === 'ThucPham') ? 'block' : 'none';
    document.getElementById('editModal').style.display = 'block';
}

// 5. Hàm Lưu Sửa
async function luuSua() {
    const ma = document.getElementById('edit_ma_hang').value;
    const data = {
        ten_hang: document.getElementById('edit_ten').value,
        gia_nhap: parseFloat(document.getElementById('edit_gia').value) || 0,
        nhap_them: parseInt(document.getElementById('edit_nhap_them').value) || 0,
        xuat_ban: parseInt(document.getElementById('edit_xuat_ban').value) || 0
    };

    const response = await fetch(`/api/hang-hoa/${ma}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    
    const res = await response.json();
    if(res.success) {
        alert("Cập nhật thành công!");
        location.reload();
    } else {
        alert("Lỗi: " + res.message);
    }
}

// 6. Hàm mở Modal Xóa
function xoaHangHoa(ma) {
    document.getElementById('delete_ma_hang_text').innerText = ma;
    document.getElementById('delete_ma_hang_val').value = ma;
    document.getElementById('deleteModal').style.display = 'block';
}

// 7. Hàm Thực hiện Xóa
async function thucHienXoa() {
    const ma = document.getElementById('delete_ma_hang_val').value;
    const response = await fetch(`/api/hang-hoa/${ma}`, { method: 'DELETE' });
    const res = await response.json();
    if(res.success) {
        location.reload();
    } else {
        alert("Lỗi: " + res.message);
    }
}