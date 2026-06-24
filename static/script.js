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
function openDeleteModal(ma_hang) {
    document.getElementById('delete_ma_hang_text').innerText = ma_hang;
    document.getElementById('deleteModal').style.display = 'block';
    window.currentDeleteID = ma_hang; // Lưu tạm để gọi hàm xóa
}

// 5. Hàm Lưu Sửa
function luuSua() {
    const ma_hang = document.getElementById('edit_ma_hang').value;
    const data = {
        ten_hang: document.getElementById('edit_ten').value,
        gia_nhap: document.getElementById('edit_gia').value,
        loai_hang: document.getElementById('edit_loai_hang').value,
        nhap_them: document.getElementById('edit_nhap_them').value || 0,
        xuat_ban: document.getElementById('edit_xuat_ban').value || 0
    };

    fetch(`/api/hang-hoa/${ma_hang}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => {
        if(result.success) {
            location.reload(); // Tải lại trang để cập nhật danh sách
        } else {
            alert(result.message);
        }
    });
}
// 6. Hàm mở Modal Xóa
function xoaHangHoa(ma, ten) {

    document.getElementById('delete_ma_hang_val').value = ma;

    document.getElementById('delete_ma_hang_text').innerText =
        ma + " - " + ten;

    document.getElementById('deleteModal').style.display = 'block';
}

// 7. Hàm Thực hiện Xóa
function thucHienXoa() {

    const ma_hang =
        document.getElementById('delete_ma_hang_val').value;

    fetch(`/api/hang-hoa/${ma_hang}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(data => {

        if(data.success) {

            document.getElementById('deleteModal').style.display = 'none';

            location.reload();

        } else {

            alert(data.message);

        }
    })
    .catch(error => {

        console.error(error);

        alert("Lỗi kết nối server");

    });
}
// Hàm lọc dữ liệu
async function locDuLieu() {
    const searchInput = document.getElementById('searchInput').value;
    const typeFilter = document.getElementById('typeFilter').value;
    const tbody = document.querySelector('#resultTable tbody');

    tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Đang tải...</td></tr>';

    try {
        const response = await fetch('/api/sap-xep-tim-kiem', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                action: 'sort',
                keyword: searchInput,
                criteria: typeFilter || 'all',
                sort_type: document.getElementById('sortOrder').value 
            })
        });

        const result = await response.json();
        tbody.innerHTML = '';

        if (result.success && Array.isArray(result.data)) {
            tbody.innerHTML = '';
            if (result.data.length > 0) {
                let rows = "";
                result.data.forEach(item => {
                    let giaValue = parseFloat(item.gia_nhap) || 0;
                    let giaDisplay = giaValue.toLocaleString('en-US', {
                        minimumFractionDigits: 0,
                        maximumFractionDigits: 0
                    });
                    let rowClass = "";
                    if (item.loai_hang === "Thực phẩm") rowClass = "row-ThucPham";
                    else if (item.loai_hang === "Điện máy") rowClass = "row-DienMay";
                    else if (item.loai_hang === "Gia dụng") rowClass = "row-GiaDung";
                    
                    rows += `<tr class="row-${item.loai_hang}"> <td>${item.ma_hang}</td>
                        <td>${item.ten_hang}</td>
                        <td>${giaDisplay}</td> 
                        <td>${item.so_luong}</td>
                    </tr>`;
                });
                tbody.innerHTML = rows;
            } else {
                tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Không tìm thấy kết quả.</td></tr>';
            }
        } else {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:red;">Dữ liệu lỗi!</td></tr>';
        }
    } catch (err) {
        console.error("Lỗi:", err);
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:red;">Lỗi!</td></tr>';
    }
}
// Vẽ biểu đồ khi trang đã tải xong
document.addEventListener("DOMContentLoaded", function() {
    const ctx = document.getElementById('myChart');
    
    if(ctx && window.chartDataFromFlask) {
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: window.chartDataFromFlask.labels,
                datasets: [
                    {
                        label: 'Số lượng Tồn Kho',
                        data: window.chartDataFromFlask.tonKho,
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Số lượng Đã Bán',
                        data: window.chartDataFromFlask.daBan,
                        backgroundColor: 'rgba(255, 99, 132, 0.7)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
});

// Hàm cập nhật bảng
function capNhatBang(danhSach) {
    const tbody = document.querySelector('#resultTable tbody');
    tbody.innerHTML = ''; 

    if (danhSach && danhSach.length > 0) {
        let rows = ""; 
        
        danhSach.forEach(item => {
            let giaValue = parseFloat(item.gia_nhap) || 0;
            let giaDisplay = giaValue.toLocaleString('en-US', {
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            });
            
            rows += `<tr>
                <td>${item.ma_hang}</td>
                <td>${item.ten_hang}</td>
                <td>${giaDisplay} VNĐ</td>
                <td>${item.so_luong}</td>
            </tr>`;
        });
        
        tbody.innerHTML = rows; 
    } else {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Không có dữ liệu.</td></tr>';
    }
}


// Hàm xử lý chức năng
async function xuLyChucNang(action) {
    const sortOrder = document.getElementById('sortOrder')?.value || 'gia_asc';

    const data = {
        action: action,
        keyword: document.getElementById('searchInput').value,
        criteria: document.getElementById('typeFilter').value,
        sort_type: sortOrder 
    };

    const response = await fetch('/api/sap-xep-tim-kiem', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    if (result.success) {
        capNhatBang(result.data); 
    }
}

// Tự động tô màu lại mỗi khi bảng danh sách thay đổi
const observer = new MutationObserver(() => {
    document.querySelectorAll('#resultTable tbody tr').forEach(row => {
        if (!row.cells[3]) return; 
        const txt = row.cells[3].innerText;
        if (txt.includes("Thực phẩm")) row.style.backgroundColor = "#d1fae5";
        else if (txt.includes("Điện máy")) row.style.backgroundColor = "#fee2e2";
        else if (txt.includes("Gia dụng")) row.style.backgroundColor = "#fef3c7";
    });
});
const target = document.getElementById('resultTable');
if (target) observer.observe(target, { childList: true, subtree: true });