from fastapi import APIRouter
from db import devices_collection
from models import DeviceIn, DeviceOut
from datetime import datetime

router = APIRouter()

@router.post("/discovered")
def register_device(device: DeviceIn):
    doc = device.dict()
    doc["status"] = "discovered"
    doc["last_seen"] = datetime.utcnow().isoformat()
    devices_collection.update_one({"ip": device.ip}, {"$set": doc}, upsert=True)
    return {"message": "Device recorded"}

@router.get("/")
def list_devices():
    return list(devices_collection.find({}, {"_id": 0}))