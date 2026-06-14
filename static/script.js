// Đợi HTML tải xong mới chạy Script
document.addEventListener("DOMContentLoaded", function() {
    
    // Tìm tất cả các nút Xóa trên giao diện
    const deleteButtons = document.querySelectorAll(".btn-delete");

    // Thêm sự kiện click cho từng nút
    deleteButtons.forEach(function(button) {
        button.addEventListener("click", function(event) {
            // Hiển thị hộp thoại xác nhận
            const confirmDelete = confirm("Bạn có chắc chắn muốn xóa mặt hàng này khỏi kho không?");
            
            // Nếu người dùng bấm Cancel, chặn hành động xóa
            if (!confirmDelete) {
                event.preventDefault();
            }
        });
    });

});