from fastapi import FastAPI, HTTPException

app = FastAPI(title="Customer Service")

# Mock database khách hàng
CUSTOMERS = {
    "CUST01": {"id": "CUST01", "name": "Nguyen Van A", "phone": "0901234567"},
    "CUST02": {"id": "CUST02", "name": "Tran Thi B", "phone": "0987654321"},
    "CUST03": {"id": "CUST03", "name": "Le Van C", "phone": "0911223344"}
}

@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    if customer_id not in CUSTOMERS:
        raise HTTPException(status_code=404, detail=f"Customer with ID '{customer_id}' not found")
    return CUSTOMERS[customer_id]
