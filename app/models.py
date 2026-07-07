from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from app.database import Base
from datetime import datetime

class ReconciliationJob(Base):
    __tablename__ = "reconciliation_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="processing")
    bank_total = Column(Float, nullable=True)
    ledger_total = Column(Float, nullable=True)
    difference = Column(Float, nullable=True)
    matched_count = Column(Integer, nullable=True)
    unmatched_bank_count = Column(Integer, nullable=True)
    unmatched_ledger_count = Column(Integer, nullable=True)
    result_data = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)
