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

def process_and_save(job_id : int, bank_bytes: bytes, ledger_bytes : bytes, db:Session):
    try:
        result = process_reconciliation(bank_bytes, ledger_bytes)
        #job = db.query(ReconciliationJob.id).filter(ReconciliationJob.id==job.id).first()
        job = db.query(ReconciliationJob).filter(ReconciliationJob.id == job_id).first()
        job.status = "completed"
        job.bank_total = result["summary"]["bank_total"]
        job.ledger_total = result["summary"]["ledger_total"]
        job.difference = result["summary"]["difference"]
        job.matched_count = result["summary"]["matched_count"]
        job.unmatched_bank_count = result["summary"]["unmatched_bank_count"]
        job.unmatched_ledger_count = result["summary"]["unmatched_ledger_count"]
        job.result_data = result
        db.commit()
    except Exception as e:
        job = db.query(ReconciliationJob).filter(ReconciliationJob.id==job_id).first()
        job.status = "failed"
        job.error_message = str(e)
        db.commit()

    
@router.get("/status/{job_id}")
async def get_status(job_id: int, db : Session = Depends(get_db)):
    job = db.query(ReconciliationJob).filter(ReconciliationJob.id == job.id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Job not found")
    if job.status == "processing":
        return {
            "job_id": job.id,
            "status": "processing",
            "created_at": job.created_at,
            "message": "Still processing. Check again in a few seconds."
        }
    if job.status == "failed":
        raise HTTPException(status_code=500, detail=job.error_message)
    
    # Completed
    return {
        "job_id": job.id,
        "status": "completed",
        "created_at": job.created_at,
        "completed_at": job.created_at,  # Ideally update this field too
        "data": {
            "matched": job.result_data.get("matched", []),
            "unmatched_bank": job.result_data.get("unmatched_bank", []),
            "unmatched_ledger": job.result_data.get("unmatched_ledger", []),
            "summary": {
                "bank_total": job.bank_total,
                "ledger_total": job.ledger_total,
                "difference": job.difference,
                "matched_count": job.matched_count,
                "unmatched_bank_count": job.unmatched_bank_count,
                "unmatched_ledger_count": job.unmatched_ledger_count
            }
        }
    }
