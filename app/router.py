from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends,status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import process_reconciliation
from app.models import ReconciliationJob
import json

router = APIRouter(
    prefix = "/reconcile"
)

@router.post("/")
async def reconcile(background_tasks: BackgroundTasks,
    bank_statement: UploadFile = File(...),
    internal_ledger: UploadFile = File(...),
    db: Session = Depends(get_db)):
    #validation
    if not bank_statement.filename.endswith("csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Bank statemnet must be csv file ")
    if not internal_ledger.filename.endswith("csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Internal ledger file should be csv")
    
    
    job = ReconciliationJob(status="processing")
    db.add(job)
    db.commit()
    db.refresh(job)

    #read
    bank_bytes = await bank_statement.read()
    ledger_bytes = await internal_ledger.read()

    background_tasks.add_task(process_and_save, job.id, bank_bytes, ledger_bytes, db)

    return {
        "job_id": job.id,
        "status": "processing",
        "message": "Reconciliation started. Check status with job ID."
    }

