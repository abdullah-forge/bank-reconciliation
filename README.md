# Bank Reconciliation API

**Problem:** Accountants spend 4–6 hours manually matching bank statements to internal ledgers every month.

**Solution:** Upload two CSV files. Get matched/unmatched transactions + balance difference in 2 seconds. Smart fuzzy matching with ±2 days date tolerance and amount rounding handling.

---

## 🚀 Live Demo
[https://your-app.onrender.com/docs](https://your-app.onrender.com/docs)

---

## 📸 Screenshots

### Upload Endpoint
![Upload](screenshot-upload.png)

### Response
![Response](screenshot-response.png)

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

# Activate (Mac/Linux)
source venv/bin/activate

pip install -r requirements.txt


