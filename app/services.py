import pandas as pd
import numpy as np
from io import BytesIO
from typing import Dict, List

def process_reconciliation(bank_bytes : bytes , ledger_bytes : bytes):
    bank = pd.read_csv(BytesIO(bank_bytes))
    ledger = pd.read_csv(BytesIO(ledger_bytes))
    bank.columns = [c.lower().strip() for c in bank.columns]
    ledger.columns = [c.lower().strip() for c in ledger.columns]
    for df, name in[(bank, "bank"),(ledger, "ledger")]:
        if "date" not in df.columns or "amount" not in df.columns:
            raise ValueError(f"{name} csv must have date and amount column")
        
    bank["date"] = pd.to_datetime(bank["date"], errors="coerce")
    ledger["date"] = pd.to_datetime(ledger["date"], errors="coerce")

    bank["amount"] = pd.to_numeric(bank["amount"], errors="coerce")
    ledger["amount"] = pd.to_numeric(ledger["amount"], errors="coerce")

    bank = bank.dropna(subset=["date","amount"]).copy()
    ledger = ledger.copy()
    
    bank["description"] = bank.get("description", "").astype(str)
    ledger["description"] = ledger.get("description", "").astype(str)

    ledger_used = set()
    matched = []

    for b_idx , b_row in bank.iterrows():
        b_amt = b_row["amount"]
        b_date = b_row["date"]
        
        candidates = []
        for l_idx, l_row in ledger.iterrows():
            if l_idx in ledger_used:
                continue
            if np.isclose(l_row["amount"],b_amt, rtol = 1e-5):
                date_diff = abs((l_row["date"] - b_date).days)
                if date_diff <=2:
                    candidates.append((l_idx, l_row, date_diff))
        if candidates:
            candidates.sort(key = lambda x:x[2])
            best_idx , best_row, best_diff = candidates[0]
            ledger_used.add(best_idx)
            matched.append({
                "bank_date" : b_date.strftime("%Y-%m-%d"),
                "bank_amount": round(float(b_amt), 2),
                "bank_description": b_row["description"],
                "ledger_date": best_row["date"].strftime("%Y-%m-%d"),
                "ledger_amount": round(float(best_row["amount"]), 2),
                "ledger_description": best_row["description"],
                "date_diff_days": int(best_diff)
            }
            )
