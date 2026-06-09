def tim_theo_ma(danh_sach, ma_hang):
    for item in danh_sach:
        if item["ma_hang"] == ma_hang:
            return item

    return None