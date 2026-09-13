import time
import threading
import uvicorn
import httpx
import json

def run_customer_service():
    uvicorn.run("customer_service:app", host="127.0.0.1", port=8081, log_level="warning")

def run_account_service():
    uvicorn.run("account_service:app", host="127.0.0.1", port=8082, log_level="warning")

def run_loan_service():
    uvicorn.run("loan_service:app", host="127.0.0.1", port=8083, log_level="warning")

def run_gateway_service():
    uvicorn.run("gateway:app", host="127.0.0.1", port=8222, log_level="info")

def run_test_cases():
    time.sleep(2)  # Đợi các server khởi động thành công
    print("\n" + "="*70)
    print("STARTING AUTOMATED INTEGRATION TESTS (API GATEWAY -> SERVICES)")
    print("="*70 + "\n")

    gateway_url = "http://127.0.0.1:8222"

    # Test Case 1: POST /api/loans/apply với customerId hợp lệ (CUST01)
    print("[TEST CASE 1]: Đăng ký khoản vay với customerId hợp lệ (CUST01)")
    payload_1 = {
        "customerId": "CUST01",
        "amount": 12000000.0,
        "termMonths": 12,
        "purpose": "Sắm sửa thiết bị học tập"
    }
    resp1 = httpx.post(f"{gateway_url}/api/loans/apply", json=payload_1)
    print(f"Status Code: {resp1.status_code}")
    print(f"Response Header 'X-Response-Time': {resp1.headers.get('X-Response-Time')}")
    print(f"Response Body:\n{json.dumps(resp1.json(), indent=2, ensure_ascii=False)}\n")

    # Test Case 2: POST /api/loans/apply với customerId không tồn tại (CUST99)
    print("[TEST CASE 2]: Đăng ký khoản vay với customerId không tồn tại (CUST99)")
    payload_2 = {
        "customerId": "CUST99",
        "amount": 5000000.0,
        "termMonths": 6,
        "purpose": "Vay tiêu dùng"
    }
    resp2 = httpx.post(f"{gateway_url}/api/loans/apply", json=payload_2)
    print(f"Status Code: {resp2.status_code}")
    print(f"Response Header 'X-Response-Time': {resp2.headers.get('X-Response-Time')}")
    print(f"Response Body: {resp2.json()}\n")

    # Test Case 3: POST /api/loans/apply với khách hàng chưa có tài khoản active (CUST02)
    print("[TEST CASE 3]: Đăng ký khoản vay với khách hàng không có tài khoản ACTIVE (CUST02)")
    payload_3 = {
        "customerId": "CUST02",
        "amount": 20000000.0,
        "termMonths": 24,
        "purpose": "Kinh doanh"
    }
    resp3 = httpx.post(f"{gateway_url}/api/loans/apply", json=payload_3)
    print(f"Status Code: {resp3.status_code}")
    print(f"Response Header 'X-Response-Time': {resp3.headers.get('X-Response-Time')}")
    print(f"Response Body: {resp3.json()}\n")

    print("="*70)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*70)

if __name__ == "__main__":
    t_customer = threading.Thread(target=run_customer_service, daemon=True)
    t_account = threading.Thread(target=run_account_service, daemon=True)
    t_loan = threading.Thread(target=run_loan_service, daemon=True)
    t_gateway = threading.Thread(target=run_gateway_service, daemon=True)

    t_customer.start()
    t_account.start()
    t_loan.start()
    t_gateway.start()

    run_test_cases()
