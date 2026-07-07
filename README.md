# Bank Reconciliation API

**Problem:** Accountants spend 4–6 hours manually matching bank statements to internal ledgers every month.

**Solution:** Upload two CSV files. Get matched/unmatched transactions + balance difference in 2 seconds. Smart fuzzy matching with ±2 days date tolerance and amount rounding handling.

---

## 🚀 Live Demo
[https://your-app.onrender.com/docs](https://bank-reconciliation-kg87.onrender.com/docs)

---

## 📸 Screenshots

### Upload Endpoint
<img width="1108" height="600" alt="ss3" src="https://github.com/user-attachments/assets/e01c1193-78d4-4c42-86f2-23063b3c4c60" />


### Response
<img width="1086" height="600" alt="ss4" src="https://github.com/user-attachments/assets/4897883e-590c-47c8-8447-d8fc46bc9e75" />


---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI |
| Data Processing | Pandas, NumPy |
| Database | PostgreSQL + Alembic |
| Testing | pytest |
| Deployment | Render |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/reconcile` | Upload bank + ledger CSV |
| GET | `/api/v1/status/{job_id}` | Get reconciliation results |

---

## 📋 How to Use

### Method 1: Live API (Render)
**No setup needed.** Just visit the live URL and test.

1. Go to [Live Demo](https://your-app.onrender.com/docs)
2. Click `POST /api/v1/reconcile`
3. Upload `bank_statement.csv` and `internal_ledger.csv`
4. Copy `job_id` from response
5. Click `GET /api/v1/status/{job_id}`
6. Enter `job_id`, get full report

---

### Method 2: Run Locally

**Step 1: Download**
```bash
git clone https://github.com/yourusername/bank-reconciliation.git
cd bank-reconciliation

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

pip install -r requirements.txt

# Option A: PostgreSQL (Production)
# Create database "BankRecon" in PostgreSQL
# Update .env file

# Option B: SQLite (Quick Test)
# Edit app/config.py: DATABASE_URL = "sqlite:///./test.db"


# Create .env file
cp .env.example .env

# Edit .env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/BankRecon

# Activate (Mac/Linux)
source venv/bin/activate

pip install -r requirements.txt


alembic upgrade head
uvicorn app.main:app --reload
# Open browser
http://localhost:8000/docs

# Or run tests
pytest tests/ -v

Method 3: Docker (Coming Soon)
# Build and run with Docker Compose
docker-compose up --build


Example Request
Upload two CSV files:
curl -X POST "https://your-app.onrender.com/api/v1/reconcile" \
  -F "bank_statement=@bank.csv" \
  -F "internal_ledger=@ledger.csv"


Response:
{
  "job_id": 1,
  "status": "processing",
  "message": "Reconciliation started. Check status with job ID."
}


Check Status:
curl "https://your-app.onrender.com/api/v1/status/1"
Result:
JSON
{
  "job_id": 1,
  "status": "completed",
  "matched": [
    {
      "bank_date": "2024-01-15",
      "bank_amount": 100.00,
      "ledger_date": "2024-01-15",
      "ledger_amount": 100.00,
      "date_diff_days": 0
    }
  ],
  "unmatched_bank": [...],
  "unmatched_ledger": [...],
  "summary": {
    "bank_total": 425.50,
    "ledger_total": 650.50,
    "difference": -225.00,
    "matched_count": 2,
    "unmatched_bank_count": 1,
    "unmatched_ledger_count": 1
  }
}
🧪 Testing
pytest tests/ -v

4 tests passed:

| Test                           | Status |
| ------------------------------ | ------ |
| test\_health                   | ✅      |
| test\_reconcile\_basic         | ✅      |
| test\_reconcile\_invalid\_file | ✅      |
| test\_status\_not\_found       | ✅      |


Architecture
User Uploads 2 CSVs
    ↓
FastAPI receives + validates
    ↓
Background task starts
    ↓
Pandas fuzzy matching (±2 days, amount tolerance)
    ↓
Result saved to PostgreSQL
    ↓
User gets job ID → checks status → full report


CSV Format
bank_statement.csv:
csv
date,amount,description
2024-01-15,100.00,Client A
2024-01-16,250.50,Client B
2024-01-18,75.00,Client C

internal_ledger.csv:
csv
date,amount,description
2024-01-15,100.00,Client A
2024-01-17,250.50,Client B
2024-01-20,300.00,Client D


Configuration
| Variable       | Description                  | Default     |
| -------------- | ---------------------------- | ----------- |
| `DATABASE_URL` | PostgreSQL connection string | Required    |
| `UPLOAD_DIR`   | File upload directory        | `./uploads` |

Deploy Your Own
Render (Recommended - Free)
Fork this repo
Create account on Render
New Web Service → Connect GitHub repo
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port 10000
Add Environment Variable: DATABASE_URL
Deploy
Railway (Alternative)
Similar steps as Render.
AWS/GCP/Azure (Production)
Use RDS/Cloud SQL for PostgreSQL
Deploy on EC2/Cloud Run/App Service
Set environment variables


License
MIT
👤 Author
Muhammad Abdullah — Computer Engineering @ COMSATS University Islamabad
GitHub: https://github.com/abdullah-forge
LinkedIn: Muhammad Abdullah
Email: whello544@gmail.com
