import uuid
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Loan Service")

# Yêu cầu 2: FeignClient Interfaces (Mô phỏng bằng Client HTTP trong Python)
class CustomerServiceClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8081"):
        self.base_url = base_url

    def get_customer(self, customer_id: str):
        try:
            resp = httpx.get(f"{self.base_url}/api/customers/{customer_id}", timeout=5.0)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as err:
            raise HTTPException(status_code=500, detail=f"Customer Service communication error: {str(err)}")

class AccountServiceClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8082"):
        self.base_url = base_url

    def get_accounts_by_customer(self, customer_id: str):
        try:
            resp = httpx.get(f"{self.base_url}/api/accounts/customer/{customer_id}", timeout=5.0)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as err:
            raise HTTPException(status_code=500, detail=f"Account Service communication error: {str(err)}")

customer_client = CustomerServiceClient()
account_client = AccountServiceClient()

LOANS_DATABASE = []

class LoanApplicationRequest(BaseModel):
    customerId: str = Field(..., example="CUST01")
    amount: float = Field(..., gt=0, example=10000000.0)
    termMonths: int = Field(..., gt=0, example=12)
    purpose: str = Field(..., example="Mua xe")

# Yêu cầu 3: API Đăng ký khoản vay
@app.post("/api/loans/apply")
def apply_loan(req: LoanApplicationRequest):
    # Step 1: Gọi Customer Service lấy thông tin khách hàng
    customer = customer_client.get_customer(req.customerId)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer with ID '{req.customerId}' not found")

    # Step 2: Gọi Account Service lấy danh sách tài khoản
    accounts = account_client.get_accounts_by_customer(req.customerId)
    active_accounts = [acc for acc in accounts if acc.get("status") == "ACTIVE"]
    
    if not active_accounts:
        raise HTTPException(status_code=400, detail="Customer has no active account for disbursement")

    disbursement_account = active_accounts[0]

    # Step 3: Tính toán lãi suất (8%/năm) và khoản phải trả hàng tháng
    annual_rate = 0.08
    monthly_rate = annual_rate / 12.0
    n = req.termMonths

    # Công thức trả góp đều hàng tháng (Amortization formula)
    monthly_payment = req.amount * (monthly_rate * (1 + monthly_rate) ** n) / (((1 + monthly_rate) ** n) - 1)
    total_payable = monthly_payment * n

    # Step 4: Tạo bản ghi khoản vay với trạng thái PENDING
    loan_record = {
        "loanId": f"LOAN-{uuid.uuid4().hex[:8].upper()}",
        "customer": customer,
        "disbursementAccount": disbursement_account,
        "amount": req.amount,
        "termMonths": req.termMonths,
        "interestRateAnnual": "8.0%",
        "monthlyPayment": round(monthly_payment, 2),
        "totalPayable": round(total_payable, 2),
        "purpose": req.purpose,
        "status": "PENDING"
    }

    LOANS_DATABASE.append(loan_record)
    return loan_record
