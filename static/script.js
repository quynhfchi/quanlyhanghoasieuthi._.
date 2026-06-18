document.addEventListener('DOMContentLoaded', function() {
    const loaiHang = document.getElementById('loai_hang');
    const dateRow = document.getElementById('date-row');
    if (loaiHang) {
        loaiHang.addEventListener('change', function() {
            dateRow.style.display = (this.value === 'ThucPham') ? 'flex' : 'none';
        });
    }

    const addForm = document.getElementById('addForm');
    if (addForm) {
        addForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const productData = {
                ma_hang: document.getElementById('ma_hang').value,
                ten_hang: document.getElementById('ten_hang').value,
                loai_hang: loaiHang.value,
                so_luong: parseInt(document.getElementById('so_luong').value),
                gia_nhap: parseFloat(document.getElementById('gia_nhap').value),
                ngay_san_xuat: document.getElementById('ngay_san_xuat').value || null,
                han_su_dung: document.getElementById('han_su_dung').value || null
            };
            fetch('/api/hang-hoa', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(productData)
            }).then(() => window.location.reload());
        });
    }

    initSupermarketChart();
    executeSearch();
});

function executeSearch() {
    const keyword = document.getElementById('searchKeyword').value;
    fetch('/api/sap-xep-tim-kiem', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({action: 'search', keyword: keyword})
    })
    .then(res => res.json())
    .then(res => renderFilteredTable(res.data));
}

function executeSort() {
    const criteria = document.getElementById('sortCriteria').value;
    let tieu_chi = 'gia_nhap';
    let kieu = 'asc';

    if (criteria === 'gia-giam') { tieu_chi = 'gia_nhap'; kieu = 'desc'; }
    else if (criteria === 'sl-tang') { tieu_chi = 'so_luong'; kieu = 'asc'; }
    else if (criteria === 'sl-giam') { tieu_chi = 'so_luong'; kieu = 'desc'; }
    else if (criteria === 'ten-tang') { tieu_chi = 'ten_hang'; kieu = 'asc'; }

    fetch('/api/sap-xep-tim-kiem', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({action: 'sort', tieu_chi: tieu_chi, kieu: kieu})
    })
    .then(res => res.json())
    .then(res => {
        renderFilteredTable(res.data);
        updateMainTable(res.data); 
    });
}

function renderFilteredTable(data) {
    const tbody = document.getElementById('filterTableBody');
    tbody.innerHTML = '';
    data.forEach(item => {
        tbody.innerHTML += `
            <tr>
                <td><strong>${item.ma_hang}</strong></td>
                <td>${item.ten_hang}</td>
                <td>${item.gia_nhap.toLocaleString()}đ</td>
                <td><span class="badge">${item.so_luong}</span></td>
                <td>${item.han_su_dung ? item.han_su_dung : 'Không áp dụng'}</td>
            </tr>
        `;
    });
}

function updateMainTable(data) {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';
    data.forEach(item => {
        tbody.innerHTML += `
            <tr class="${item.loai_hang === 'ThucPham' ? 'row-thucpham' : (item.loai_hang === 'DienMay' ? 'row-dienmay' : 'row-giadung')}">
                <td><strong>${item.ma_hang}</strong></td>
                <td>${item.ten_hang}</td>
                <td>${item.gia_nhap.toLocaleString()}đ</td>
                <td><span class="badge">${item.so_luong}</span></td>
                <td>${item.ngay_nhap}</td>
                <td>${item.han_su_dung ? item.han_su_dung : 'Không áp dụng'}</td>
            </tr>
        `;
    });
}

function initSupermarketChart() {
    const ctx = document.getElementById('supmarketChart').getContext('2d');
    const totalStock = thongKeRawData.ton_kho.reduce((a, b) => a + b, 0);
    document.getElementById('kpi-total').innerText = totalStock;
    document.getElementById('kpi-new').innerText = thongKeRawData.labels.length;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: thongKeRawData.labels,
            datasets: [
                {
                    label: 'Số lượng tồn kho',
                    data: thongKeRawData.ton_kho,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Sản phẩm đã bán',
                    data: thongKeRawData.da_ban,
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function switchTab(tabName) {
    document.querySelectorAll('.tab-section').forEach(sec => sec.classList.remove('active'));
    document.querySelectorAll('.sidebar-menu li').forEach(item => item.classList.remove('active'));
    document.getElementById('tab-' + tabName).classList.add('active');
    event.currentTarget.parentElement.classList.add('active');
}
addForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const productData = {
        ma_hang: document.getElementById('ma_hang').value,
        ten_hang: document.getElementById('ten_hang').value,
        loai_hang: document.getElementById('loai_hang').value,
        so_luong: document.getElementById('so_luong').value,
        gia_nhap: document.getElementById('gia_nhap').value,
        han_su_dung: document.getElementById('han_su_dung')?.value || null
    };

    fetch('/api/hang-hoa', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(productData)
    })
    .then(res => res.json())
    .then(res => {
        if (res.success) {
            window.location.reload();
        } else {
            alert("⚠️ KHÔNG THỂ THÊM HÀNG: " + res.message);
        }
    });
});