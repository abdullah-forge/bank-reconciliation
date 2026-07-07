from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_reconcile_basic():
    bank_csv = "date,amount,description\n2024-01-15,100.00,Client A\n2024-01-16,250.50,Client B"
    ledger_csv = "date,amount,description\n2024-01-15,100.00,Client A\n2024-01-17,250.50,Client B"
    
    response = client.post(
        "/api/v1/reconcile",
        files={
            "bank_statement": ("bank.csv", io.BytesIO(bank_csv.encode()), "text/csv"),
            "internal_ledger": ("ledger.csv", io.BytesIO(ledger_csv.encode()), "text/csv")
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "processing"
    assert "job_id" in data

def test_reconcile_invalid_file():
    response = client.post(
        "/api/v1/reconcile",
        files={
            "bank_statement": ("test.txt", io.BytesIO(b"not csv"), "text/plain"),
            "internal_ledger": ("test.txt", io.BytesIO(b"not csv"), "text/plain")
        }
    )
    assert response.status_code == 400

def test_status_not_found():
    response = client.get("/api/v1/status/99999")
    assert response.status_code == 404
