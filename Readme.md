# README

## Tổng quan
Đây là repo **ecommerce microservices** cho cửa hàng bán **laptop** và **mobile**.  
Hệ thống được tách thành **4 service nghiệp vụ** và **1 API Gateway**:

- `staff_service`
- `customer_service`
- `laptop_service`
- `mobile_service`
- `api_gateway_service`

PDF yêu cầu xác nhận rõ mapping database:
- `staff_service` → **MySQL**
- `customer_service` → **MySQL**
- `laptop_service` → **PostgreSQL**
- `mobile_service` → **PostgreSQL** :contentReference[oaicite:0]{index=0} :contentReference[oaicite:1]{index=1}

---

## Công nghệ dùng để code
Repo này được code chủ yếu bằng:

- **Python**
- **Django** để tạo từng service (`django-admin startproject`)
- **Django app structure**:
  - `portal` cho `staff_service`, `customer_service`
  - `catalog` cho `laptop_service`, `mobile_service`
- **Django REST-style API** cho `laptop_service` và `mobile_service`  
  (thấy có `serializers.py`, `views.py`, `urls.py`)
- **Docker / Docker Compose** để chạy toàn bộ hệ thống
- **Nginx** cho `api_gateway_service`
- **MySQL** cho `staff_service`, `customer_service`
- **PostgreSQL** cho `laptop_service`, `mobile_service` :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}

---

## Kiến trúc
Luồng tổng quát:

`Client -> API Gateway -> Staff/Customer Service -> Laptop/Mobile Service -> Database`

Trong đó:
- `api_gateway_service` là điểm vào chung
- `customer_service` xử lý logic phía khách hàng
- `staff_service` xử lý logic quản trị
- `laptop_service` quản lý catalog laptop
- `mobile_service` quản lý catalog mobile :contentReference[oaicite:4]{index=4}

---

## Vai trò từng service

### 1. `customer_service`
Chức năng:
- đăng ký
- đăng nhập
- tìm kiếm sản phẩm
- xem laptop / mobile
- thêm vào giỏ hàng
- xem giỏ hàng

DB:
- **MySQL** :contentReference[oaicite:5]{index=5} :contentReference[oaicite:6]{index=6}

### 2. `staff_service`
Chức năng:
- đăng nhập staff
- xem danh sách sản phẩm
- thêm sản phẩm
- cập nhật sản phẩm
- xóa sản phẩm

DB:
- **MySQL** :contentReference[oaicite:7]{index=7}

### 3. `laptop_service`
Chức năng:
- quản lý dữ liệu laptop
- expose API cho laptop
- phục vụ search / create / update laptop

DB:
- **PostgreSQL** :contentReference[oaicite:8]{index=8}

### 4. `mobile_service`
Chức năng:
- quản lý dữ liệu mobile
- expose API cho mobile
- phục vụ search / create / update mobile

DB:
- **PostgreSQL** :contentReference[oaicite:9]{index=9}

---

## API Gateway
Gateway dùng để:
- nhận request từ client
- route tới `staff_service` hoặc `customer_service`
- làm public entrypoint cho toàn bộ hệ thống

Theo PDF, gateway được dựng riêng và dùng **Nginx** trong Docker Compose. :contentReference[oaicite:10]{index=10} :contentReference[oaicite:11]{index=11}

---

## Hai flow chính

### Flow 1: Customer Search & Add to Cart
- Client gọi vào gateway
- Gateway chuyển request cho `customer_service`
- `customer_service` gọi `laptop_service` và `mobile_service` để search
- kết quả được gộp lại
- khách hàng chọn sản phẩm và thêm vào cart
- cart được lưu trong MySQL của `customer_service` :contentReference[oaicite:12]{index=12} :contentReference[oaicite:13]{index=13}

### Flow 2: Staff Create Product
- Staff thao tác qua giao diện admin
- request đi qua gateway
- `staff_service` xác định loại sản phẩm
- nếu là laptop thì gọi `laptop_service`
- nếu là mobile thì gọi `mobile_service`
- dữ liệu sản phẩm được lưu vào PostgreSQL tương ứng :contentReference[oaicite:14]{index=14}

---

## Cấu trúc repo
Cấu trúc chính theo PDF:

```text
.
├── api_gateway_service/
├── customer_service/
├── laptop_service/
├── mobile_service/
├── staff_service/
├── docker-compose.yml
└── venv/