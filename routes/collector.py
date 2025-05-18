from fastapi import APIRouter, Body
from db import configs_collection  # if you have a new collection

router = APIRouter()

@router.post("/submit_config")
def submit_config(data: dict = Body(...)):
    from datetime import datetime
    data["received_at"] = datetime.utcnow().isoformat()
    configs_collection.insert_one(data)
    return {"message": "Configuration received"}