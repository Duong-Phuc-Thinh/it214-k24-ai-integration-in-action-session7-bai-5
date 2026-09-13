# FinBank Microservices - Loan Application System with API Gateway Filter & FeignClient

Hệ thống mô phỏng kiến trúc Microservices xử lý đăng ký khoản vay (Loan Application) tại ngân hàng FinBank.

## Kiến trúc hệ thống
1. **API Gateway (Port 8222)**: Định tuyến request và chứa **Global Filter** để ghi log (Method, URL, Execution Time) và thêm HTTP Header `X-Response-Time` vào response.
2. **Customer Service (Port 8081)**: Quản lý thông tin khách hàng (`GET /api/customers/{id}`).
3. **Account Service (Port 8082)**: Quản lý thông tin tài khoản ngân hàng (`GET /api/accounts/customer/{customerId}`).
4. **Loan Service (Port 8083)**: Xử lý nghiệp vụ đăng ký khoản vay. Sử dụng `FeignClient` (HTTP Inter-service communication) để phối hợp gọi dữ liệu từ **Customer Service** và **Account Service**.

---

## Chi tiết các Test Case
- **Test Case 1**: Đăng ký khoản vay thành công cho khách hàng hợp lệ và có tài khoản ACTIVE (`CUST01`).
- **Test Case 2**: Đăng ký khoản vay thất bại khi khách hàng không tồn tại (`CUST99` -> Trả về lỗi `404 Not Found`).
- **Test Case 3**: Đăng ký khoản vay thất bại khi khách hàng không có tài khoản ACTIVE (`CUST02` - tài khoản INACTIVE hoặc `CUST03` - chưa mở tài khoản -> Trả về lỗi `400 Bad Request`).
- **Header Check**: Kiểm tra response từ Gateway luôn chứa header `X-Response-Time`.

---

## Yêu cầu cài đặt & Chạy ứng dụng

### 1. Cài đặt thư viện phụ thuộc
```bash
pip install fastapi uvicorn httpx pydantic
```

### 2. Chạy ứng dụng và Test tự động
```bash
python main.py
```
