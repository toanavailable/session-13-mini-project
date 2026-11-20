# Mini Project - Hệ thống Quản lý Bãi đỗ xe Thông minh (Smart Parking)

Chương trình dòng lệnh (CLI) quản lý bãi đỗ xe, xây dựng theo tài liệu đặc tả **SRS - Smart Parking System**. Dữ liệu được tổ chức bằng **List của Dictionary**, thực hiện đầy đủ các thao tác CRUD: Check-in, báo cáo, tìm kiếm, Check-out và tính phí.

## 1. Mục tiêu

- Vận dụng cấu trúc dữ liệu List của Dictionary để tổ chức dữ liệu dạng bản ghi.
- Thực hiện thành thạo các thao tác CRUD trong List.
- Áp dụng tư duy phân tích yêu cầu từ tài liệu đặc tả (SRS) vào lập trình thực tế.
- Quản lý dự án trên GitHub.

## 2. Mô tả bài toán

Lập trình viên tại công ty giải pháp đô thị xây dựng chương trình quản lý bãi xe theo các yêu cầu nghiệp vụ trong tài liệu SRS.

### Menu bắt buộc

```
======================================================
            QUẢN LÝ BÃI XE - SMART PARKING            
======================================================
    1. Check-in (Đăng ký xe vào)
    2. Báo cáo tồn kho (Hiển thị danh sách)
    3. Tìm kiếm xe (Theo biển số)
    4. Check-out (Xử lý xe ra & Tính phí)
    5. Thoát chương trình
======================================================
Nhập lựa chọn của bạn (1-5):
```

### Yêu cầu chức năng (theo SRS)

| Lựa chọn | Chức năng | Mô tả |
|---|---|---|
| 1 | Check-in | Nhập biển số, loại xe, giờ vào. Kiểm tra trống và trùng biển số; tự động cấp ID tăng dần |
| 2 | Báo cáo tồn kho | In bảng ID, Biển số, Loại xe, Giờ vào căn lề thẳng hàng; bãi trống thì in `[Thông báo: Bãi xe hiện đang trống!]` |
| 3 | Tìm kiếm xe | Nhập biển số, in thông tin chi tiết (Dictionary); không thấy thì báo ERR-04 |
| 4 | Check-out | Nhập biển số và giờ ra, tính phí = (giờ ra − giờ vào) × đơn giá, xóa xe khỏi List |
| 5 | Thoát | Lệnh duy nhất dừng chương trình |

### Danh mục mã lỗi (SRS mục 5)

| Mã lỗi | Thông báo | Vị trí | Xử lý |
|---|---|---|---|
| ERR-01 | `[Lỗi]: Xe với biển số này đã tồn tại trong bãi!` | Check-in | Nhập lại biển số |
| ERR-02 | `[Lỗi]: Loại xe không hợp lệ (1: Xe máy, 2: Ô tô)!` | Check-in | Lặp đến khi nhập 1 hoặc 2 |
| ERR-03 | `[Lỗi]: Giờ ra phải sau hoặc bằng giờ vào!` | Check-out | Nhập lại giờ ra |
| ERR-04 | `[Lỗi]: Không tìm thấy biển số [plate] trong hệ thống!` | Tìm kiếm / Check-out | Quay lại menu |
| ERR-05 | `[Lỗi]: Lựa chọn không hợp lệ. Vui lòng nhập từ 1-5!` | Menu chính | `continue`, hiện lại menu |

## 3. Phân tích và thiết kế

### 3.1. Thiết kế dữ liệu

```python
parking_lot = [
    {"id": 1, "plate": "29A-12345", "type": 1, "entry_time": 8},
    {"id": 2, "plate": "30B-99999", "type": 2, "entry_time": 9},
]
```

| Trường | Kiểu | Ý nghĩa | Ràng buộc |
|---|---|---|---|
| `id` | int | Mã xe tự tăng | Lấy từ `next_id`, không dùng lại sau khi xe ra |
| `plate` | str | Biển số (mã định danh) | Không trống, không trùng, chuẩn hóa `strip().upper()` |
| `type` | int | 1: Xe máy, 2: Ô tô | Chỉ nhận "1" hoặc "2" |
| `entry_time` | int | Giờ vào | Số nguyên 0-24 |

Đơn giá đặt thành hằng số ở đầu chương trình: `MOTORBIKE_PRICE = 5000`, `CAR_PRICE = 10000` (VNĐ/giờ).

### 3.2. Phân tích Input / Output

| Input | Biến | Kiểm tra | Output |
|---|---|---|---|
| Lựa chọn menu | `choice` | So sánh chuỗi "1"…"5" | Chức năng tương ứng hoặc ERR-05 |
| Biển số | `plate` | Không trống; Check-in: không trùng | ERR-01 / ERR-04 nếu sai |
| Loại xe | `type_text → vehicle_type` | Chỉ "1" hoặc "2" | ERR-02 nếu sai |
| Giờ vào / giờ ra | `entry_text`, `exit_text` | `isdigit()` và ≤ 24; giờ ra ≥ giờ vào | ERR-03 nếu giờ ra < giờ vào |
| — | `fee` | — | `Tổng phí phải trả: ... VNĐ` |

### 3.3. Luồng chương trình (Pseudocode)

```
parking_lot ← []; next_id ← 1
LẶP MÃI:
    IN menu; NHẬP choice
    "1": LẶP nhập biển số đến khi không trống và không trùng (ERR-01)
         LẶP nhập loại xe đến khi là 1 hoặc 2 (ERR-02)
         LẶP nhập giờ vào đến khi là số nguyên 0-24
         append({id: next_id, plate, type, entry_time}); next_id += 1; IN [Thành công]
    "2": rỗng → [Thông báo: Bãi xe hiện đang trống!]
         ngược lại IN bảng căn lề (đổi type 1/2 → Xe máy / Ô tô)
    "3" hoặc "4":
         rỗng → thông báo bãi trống, quay lại menu
         NHẬP biển số (không trống); found ← xe có plate trùng
         không thấy → ERR-04, quay lại menu
         "3": IN found (Dictionary)
         "4": LẶP nhập giờ ra đến khi là số 0-24 và ≥ entry_time (ERR-03)
              đơn_giá ← 5000 nếu xe máy, 10000 nếu ô tô
              phí ← (giờ_ra − giờ_vào) × đơn_giá; IN phí
              parking_lot.remove(found); IN [Thành công]
    "5": THOÁT
    khác: ERR-05
```

### 3.4. Các điểm kỹ thuật chính

- **Không crash khi nhập sai kiểu:** mọi giá trị số đều kiểm tra bằng `isdigit()` trước khi `int()`; lựa chọn menu và loại xe so sánh dạng chuỗi, nên nhập chữ, số âm hay để trống đều chỉ ra thông báo lỗi.
- **Bắt nhập lại ngay lập tức:** biển số, loại xe, giờ vào, giờ ra dùng vòng `while True` riêng, chỉ `break` khi dữ liệu hợp lệ (đúng yêu cầu Phần III).
- **Toàn vẹn dữ liệu:** thêm bằng `append`, xóa bằng `remove` trực tiếp trên `parking_lot`; ID tăng theo biến `next_id` nên không bị trùng kể cả sau khi xe ra.
- **Kiểm soát ranh giới:** chức năng 2, 3, 4 kiểm tra bãi trống trước khi duyệt / tìm / xóa.
- **Căn lề bảng:** f-string `{:<5}`, `{:<14}`, `{:<8}` cho tiêu đề và nội dung cùng độ rộng.

## 4. Mã nguồn

File: [`smart_parking.py`](smart_parking.py)

```python
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
```

## 5. Kết quả chạy thử

Kịch bản chạy toàn bộ chức năng và mọi mã lỗi *(ẩn khung menu lặp lại cho gọn)*:

```
Nhập lựa chọn của bạn (1-5): abc
[Lỗi]: Lựa chọn không hợp lệ. Vui lòng nhập từ 1-5!

Nhập lựa chọn của bạn (1-5): 9
[Lỗi]: Lựa chọn không hợp lệ. Vui lòng nhập từ 1-5!

Nhập lựa chọn của bạn (1-5): 2
[Thông báo: Bãi xe hiện đang trống!]

Nhập lựa chọn của bạn (1-5): 3
[Thông báo: Bãi xe hiện đang trống!]

Nhập lựa chọn của bạn (1-5): 4
[Thông báo: Bãi xe hiện đang trống!]

Nhập lựa chọn của bạn (1-5): 1
Nhập biển số xe: 29a-12345
Nhập loại xe (1: Xe máy, 2: Ô tô): 1
Nhập giờ vào (0-24): 8
[Thành công]: Xe 29A-12345 đã được đăng ký vào bãi (ID 1).

Nhập lựa chọn của bạn (1-5): 1
Nhập biển số xe:  
[Lỗi]: Biển số không được để trống!
Nhập biển số xe: 29A-12345
[Lỗi]: Xe với biển số này đã tồn tại trong bãi!
Nhập biển số xe: 30b-99999
Nhập loại xe (1: Xe máy, 2: Ô tô): 3
[Lỗi]: Loại xe không hợp lệ (1: Xe máy, 2: Ô tô)!
Nhập loại xe (1: Xe máy, 2: Ô tô): x
[Lỗi]: Loại xe không hợp lệ (1: Xe máy, 2: Ô tô)!
Nhập loại xe (1: Xe máy, 2: Ô tô): 2
Nhập giờ vào (0-24): abc
[Lỗi]: Giờ phải là số nguyên từ 0 đến 24!
Nhập giờ vào (0-24): 30
[Lỗi]: Giờ phải là số nguyên từ 0 đến 24!
Nhập giờ vào (0-24): 9
[Thành công]: Xe 30B-99999 đã được đăng ký vào bãi (ID 2).

Nhập lựa chọn của bạn (1-5): 2

ID   | Biển số xe    | Loại xe | Giờ vào
------------------------------------------
1    | 29A-12345     | Xe máy  | 8
2    | 30B-99999     | Ô tô    | 9
------------------------------------------
Tổng số xe đang đỗ: 2

Nhập lựa chọn của bạn (1-5): 3
Nhập biển số xe cần tìm: 29A-12345
Thông tin chi tiết: {'id': 1, 'plate': '29A-12345', 'type': 1, 'entry_time': 8}

Nhập lựa chọn của bạn (1-5): 3
Nhập biển số xe cần tìm: 88A-00000
[Lỗi]: Không tìm thấy biển số 88A-00000 trong hệ thống!

Nhập lựa chọn của bạn (1-5): 4
Nhập biển số xe cần ra: 44C-11111
[Lỗi]: Không tìm thấy biển số 44C-11111 trong hệ thống!

Nhập lựa chọn của bạn (1-5): 4
Nhập biển số xe cần ra: 29A-12345
Nhập giờ ra: 11
Tổng phí phải trả: 15000 VNĐ
[Thành công]: Đã xóa xe ID 1 thành công!

Nhập lựa chọn của bạn (1-5): 4
Nhập biển số xe cần ra: 30B-99999
Nhập giờ ra: 7
[Lỗi]: Giờ ra phải sau hoặc bằng giờ vào!
Nhập giờ ra: -1
[Lỗi]: Giờ phải là số nguyên từ 0 đến 24!
Nhập giờ ra: x
[Lỗi]: Giờ phải là số nguyên từ 0 đến 24!
Nhập giờ ra: 
[Lỗi]: Giờ phải là số nguyên từ 0 đến 24!
Nhập giờ ra: 12
Tổng phí phải trả: 30000 VNĐ
[Thành công]: Đã xóa xe ID 2 thành công!

Nhập lựa chọn của bạn (1-5): 2
[Thông báo: Bãi xe hiện đang trống!]

Nhập lựa chọn của bạn (1-5): 1
Nhập biển số xe: 51F-55555
Nhập loại xe (1: Xe máy, 2: Ô tô): 2
Nhập giờ vào (0-24): 10
[Thành công]: Xe 51F-55555 đã được đăng ký vào bãi (ID 3).

Nhập lựa chọn của bạn (1-5): 2

ID   | Biển số xe    | Loại xe | Giờ vào
------------------------------------------
3    | 51F-55555     | Ô tô    | 10
------------------------------------------
Tổng số xe đang đỗ: 1

Nhập lựa chọn của bạn (1-5): 5
Đã thoát chương trình. Hẹn gặp lại!
```

### Bảng kiểm thử

| Kịch bản | Dữ liệu | Kết quả mong đợi | Kết quả |
|---|---|---|---|
| Menu nhập chữ / ngoài dải | `abc`, `9`, `44C-11111` | ERR-05, hiện lại menu | Đạt |
| Báo cáo / tìm / check-out khi bãi trống | Chọn 2, 3, 4 | `[Thông báo: Bãi xe hiện đang trống!]` | Đạt |
| Check-in hợp lệ (chữ thường) | `29a-12345`, 1, 8 | Lưu `29A-12345`, ID 1 | Đạt |
| Biển số trống | khoảng trắng | Báo lỗi, nhập lại | Đạt |
| Biển số trùng | `29A-12345` | ERR-01, nhập lại | Đạt |
| Loại xe sai | `3`, `x` | ERR-02, nhập lại | Đạt |
| Giờ vào sai | `abc`, `30` | Báo lỗi, nhập lại | Đạt |
| Báo cáo có dữ liệu | Chọn 2 | Bảng 2 xe căn lề thẳng hàng | Đạt |
| Tìm thấy | `29A-12345` | `{'id': 1, 'plate': '29A-12345', 'type': 1, 'entry_time': 8}` | Đạt |
| Tìm không thấy | `88A-00000` | ERR-04 | Đạt |
| Check-out không thấy | `44C-11111` | ERR-04 | Đạt |
| Check-out xe máy | `29A-12345`, giờ ra 11 | Phí 15000 VNĐ, xóa ID 1 | Đạt |
| Giờ ra < giờ vào | `30B-99999`, giờ ra 7 | ERR-03, nhập lại | Đạt |
| Giờ ra sai kiểu | `-1`, `x`, trống | Báo lỗi, nhập lại | Đạt |
| Check-out ô tô | giờ ra 12 (vào 9) | Phí 30000 VNĐ, xóa ID 2 | Đạt |
| ID không dùng lại | Check-in `51F-55555` sau khi bãi trống | ID 3 | Đạt |
| Thoát | `5` | Kết thúc chương trình | Đạt |

## 6. Ghi chú về giả định

- SRS chỉ ghi công thức "(exit_time − entry_time) × Đơn giá" mà không nêu đơn giá. Ví dụ mẫu (xe máy vào 8 giờ, ra 11 giờ, phí 15000) cho thấy xe máy 5000 VNĐ/giờ. Đơn giá ô tô không có trong đề nên chọn 10000 VNĐ/giờ, khai báo thành hằng `CAR_PRICE` để dễ sửa.
- Giờ vào được nhập tay (số nguyên 0-24) theo mô hình dữ liệu của SRS, để kiểm thử được ví dụ giờ vào 8, 9 như đề.
- SRS nhắc trạng thái `parked`; vì bản ghi mẫu ở chức năng tìm kiếm chỉ có 4 trường `id, plate, type, entry_time`, chương trình coi mọi xe đang nằm trong `parking_lot` là đang đỗ, xe ra thì bị xóa khỏi List.

## 7. Cách chạy

Yêu cầu Python 3.x:

```bash
python smart_parking.py
```

## Báo cáo

- [Báo cáo dạng Word (DOCX)](bao-cao-mini-project-quan-ly-bai-do-xe.docx)
