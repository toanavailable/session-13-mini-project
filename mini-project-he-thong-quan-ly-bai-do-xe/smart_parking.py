"""Smart Parking System - Hệ thống quản lý bãi đỗ xe thông minh (theo tài liệu SRS)."""

# =====================================================================
# KHỞI TẠO DỮ LIỆU
# parking_lot: List các Dictionary (VehicleRecord)
#   {"id": int, "plate": str, "type": int (1: Xe máy, 2: Ô tô), "entry_time": int (0-24)}
# =====================================================================
parking_lot = []
next_id = 1                      # ID tự tăng, không dùng lại ID của xe đã ra
MOTORBIKE_PRICE = 5000           # Đơn giá xe máy (VNĐ/giờ)
CAR_PRICE = 10000                # Đơn giá ô tô (VNĐ/giờ)
line_width = 54

while True:
    print("\n" + "=" * line_width)
    print(f"{'QUẢN LÝ BÃI XE - SMART PARKING':^{line_width}}")
    print("=" * line_width)
    print("    1. Check-in (Đăng ký xe vào)")
    print("    2. Báo cáo tồn kho (Hiển thị danh sách)")
    print("    3. Tìm kiếm xe (Theo biển số)")
    print("    4. Check-out (Xử lý xe ra & Tính phí)")
    print("    5. Thoát chương trình")
    print("=" * line_width)
    choice = input("Nhập lựa chọn của bạn (1-5): ").strip()

    # =================================================================
    # Lựa chọn 1: CHECK-IN
    # =================================================================
    if choice == "1":
        # Nhập biển số: không trống, không trùng (ERR-01) -> nhập lại
        while True:
            plate = input("Nhập biển số xe: ").strip().upper()
            if plate == "":
                print("[Lỗi]: Biển số không được để trống!")
                continue
            is_duplicate = False
            for vehicle in parking_lot:
                if vehicle["plate"] == plate:
                    is_duplicate = True
                    break
            if is_duplicate:
                print("[Lỗi]: Xe với biển số này đã tồn tại trong bãi!")          # ERR-01
                continue
            break

        # Nhập loại xe: chỉ chấp nhận 1 hoặc 2 (ERR-02) -> nhập lại
        while True:
            type_text = input("Nhập loại xe (1: Xe máy, 2: Ô tô): ").strip()
            if type_text == "1" or type_text == "2":
                vehicle_type = int(type_text)
                break
            print("[Lỗi]: Loại xe không hợp lệ (1: Xe máy, 2: Ô tô)!")            # ERR-02

        # Nhập giờ vào: số nguyên 0-24 -> nhập lại nếu sai
        while True:
            entry_text = input("Nhập giờ vào (0-24): ").strip()
            if entry_text.isdigit() and int(entry_text) <= 24:
                entry_time = int(entry_text)
                break
            print("[Lỗi]: Giờ phải là số nguyên từ 0 đến 24!")

        # Tạo bản ghi và thêm vào parking_lot
        new_vehicle = {
            "id": next_id,
            "plate": plate,
            "type": vehicle_type,
            "entry_time": entry_time
        }
        parking_lot.append(new_vehicle)
        next_id += 1
        print(f"[Thành công]: Xe {plate} đã được đăng ký vào bãi (ID {new_vehicle['id']}).")

    # =================================================================
    # Lựa chọn 2: BÁO CÁO TỒN KHO
    # =================================================================
    elif choice == "2":
        if len(parking_lot) == 0:
            print("[Thông báo: Bãi xe hiện đang trống!]")
            continue
        print(f"\n{'ID':<5}| {'Biển số xe':<14}| {'Loại xe':<8}| Giờ vào")
        print("-" * 42)
        for vehicle in parking_lot:
            if vehicle["type"] == 1:
                type_name = "Xe máy"
            else:
                type_name = "Ô tô"
            print(f"{vehicle['id']:<5}| {vehicle['plate']:<14}| {type_name:<8}| {vehicle['entry_time']}")
        print("-" * 42)
        print(f"Tổng số xe đang đỗ: {len(parking_lot)}")

    # =================================================================
    # Lựa chọn 3 và 4: đều cần tìm xe theo biển số
    # =================================================================
    elif choice == "3" or choice == "4":
        # Bãi trống thì không cần tìm kiếm / xóa
        if len(parking_lot) == 0:
            print("[Thông báo: Bãi xe hiện đang trống!]")
            continue

        if choice == "3":
            prompt = "Nhập biển số xe cần tìm: "
        else:
            prompt = "Nhập biển số xe cần ra: "
        while True:
            plate = input(prompt).strip().upper()
            if plate != "":
                break
            print("[Lỗi]: Biển số không được để trống!")

        found_vehicle = None
        for vehicle in parking_lot:
            if vehicle["plate"] == plate:
                found_vehicle = vehicle
                break

        if found_vehicle is None:
            print(f"[Lỗi]: Không tìm thấy biển số {plate} trong hệ thống!")      # ERR-04
            continue

        # ---------- Lựa chọn 3: Tìm kiếm ----------
        if choice == "3":
            print(f"Thông tin chi tiết: {found_vehicle}")
            continue

        # ---------- Lựa chọn 4: Check-out ----------
        while True:
            exit_text = input("Nhập giờ ra: ").strip()
            if not exit_text.isdigit() or int(exit_text) > 24:
                print("[Lỗi]: Giờ phải là số nguyên từ 0 đến 24!")
                continue
            exit_time = int(exit_text)
            if exit_time < found_vehicle["entry_time"]:
                print("[Lỗi]: Giờ ra phải sau hoặc bằng giờ vào!")               # ERR-03
                continue
            break

        if found_vehicle["type"] == 1:
            unit_price = MOTORBIKE_PRICE
        else:
            unit_price = CAR_PRICE
        fee = (exit_time - found_vehicle["entry_time"]) * unit_price
        print(f"Tổng phí phải trả: {fee} VNĐ")
        parking_lot.remove(found_vehicle)
        print(f"[Thành công]: Đã xóa xe ID {found_vehicle['id']} thành công!")

    # =================================================================
    # Lựa chọn 5: THOÁT
    # =================================================================
    elif choice == "5":
        print("Đã thoát chương trình. Hẹn gặp lại!")
        break

    # Nhập chữ, ký tự hoặc ngoài dải 1-5
    else:
        print("[Lỗi]: Lựa chọn không hợp lệ. Vui lòng nhập từ 1-5!")               # ERR-05
