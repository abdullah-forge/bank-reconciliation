from fastapi import FastAPI
from app.database import engine, Base
from app.router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bank Reconciliation API")

# Health check OUTSIDE router
@app.get("/health")
def health():
    return {"status": "ok"}

# Router with prefix
app.include_router(router, prefix="/api/v1")
