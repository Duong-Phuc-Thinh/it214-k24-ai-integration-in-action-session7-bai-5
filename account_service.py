from fastapi import FastAPI

app = FastAPI(title="Account Service")

# Mock database tài khoản ngân hàng
ACCOUNTS = [
    {
        "id": "ACC01",
        "customer_id": "CUST01",
        "account_number": "1000111222",
        "status": "ACTIVE",
        "balance": 5000000.0
    },
    {
        "id": "ACC02",
        "customer_id": "CUST01",
        "account_number": "1000111333",
        "status": "ACTIVE",
        "balance": 15000000.0
    },
    {
        "id": "ACC03",
        "customer_id": "CUST02",
        "account_number": "2000222333",
        "status": "INACTIVE",
        "balance": 0.0
    }
]

@app.get("/api/accounts/customer/{customer_id}")
def get_accounts_by_customer(customer_id: str):
    """Yêu cầu 1: Lấy danh sách tất cả tài khoản của 1 khách hàng theo customerId"""
    customer_accounts = [acc for acc in ACCOUNTS if acc["customer_id"] == customer_id]
    return customer_accounts
