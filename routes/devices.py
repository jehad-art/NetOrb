from fastapi import APIRouter, Body, Header, HTTPException
from db import devices_collection, configs_collection
from models import DeviceIn, DeviceOut
from datetime import datetime
from cryptography.fernet import Fernet
from settings import settings
from analyzer.analyzer import analyze_config
from analyzer.interconnection_rules import analyze_interconnections
from db import configs_collection
import json

router = APIRouter()

fernet = Fernet(settings.fernet_key.encode())

def encrypt_credentials(data: dict) -> str:
    return fernet.encrypt(json.dumps(data).encode()).decode()

def decrypt_credentials(token: str) -> dict:
    return json.loads(fernet.decrypt(token.encode()).decode())

@router.post("/discovered")
def register_device(device: DeviceIn):
    doc = device.dict()
    doc["status"] = "discovered"
    doc["last_seen"] = datetime.utcnow().isoformat()
    devices_collection.update_one({"ip": device.ip}, {"$set": doc}, upsert=True)
    return {"message": "Device recorded"}

@router.get("/")
def list_devices():
    return list(devices_collection.find({}, {"_id": 0, "credentials": 0}))

@router.put("/{ip}")
def update_device(ip: str, device: dict = Body(...)):
    if "credentials" in device and isinstance(device["credentials"], dict):
        device["credentials"] = encrypt_credentials(device["credentials"])

    device["last_seen"] = datetime.utcnow().isoformat()
    result = devices_collection.update_one({"ip": ip}, {"$set": device})

    if result.matched_count == 0:
        return {"message": "Device not found"}
    return {"message": "Device updated"}

@router.get("/secrets/{ip}")
def get_credentials(ip: str, authorization: str = Header(...)):
    expected_token = f"Bearer {settings.agent_token}"
    if authorization != expected_token:
        raise HTTPException(status_code=403, detail="Unauthorized")

    device = devices_collection.find_one({"ip": ip}, {"_id": 0, "credentials": 1})
    if not device or "credentials" not in device:
        raise HTTPException(status_code=404, detail="Not found")

    decrypted = decrypt_credentials(device["credentials"])
    return decrypted

@router.get("/interconnection_issues")
def get_interconnection_issues():
    all_configs = list(configs_collection.find({}, {"_id": 0}))
    return analyze_interconnections(all_configs)

@router.post("/submit_config")
def submit_config(data: dict = Body(...)):
    device_type = data.get("sections", {}).get("device_type", "router")
    analysis = analyze_config(data.get("sections", {}), device_type)

    try:
        analysis = analyze_config(data.get("sections", {}), device_type)
    except Exception as e:
        print(f"Analyzer crash: {e}")
        raise HTTPException(status_code=500, detail="Analyzer failure")
    
    # Load all configs from DB
    all_configs = list(configs_collection.find({}, {"_id": 0}))

    # Temporarily include the current config (not yet inserted)
    all_configs.append(data)

    # Analyze interconnection-level issues
    try:
        interconnection_results = analyze_interconnections(all_configs)
        analysis["interconnection_issues"] = interconnection_results.get("interconnection_issues", [])
    except Exception as e:
        print(f"[!] Interconnection analysis failed: {e}")
        analysis["interconnection_issues"] = []

    data["analysis"] = analysis
    data["received_at"] = datetime.utcnow().isoformat()
    print(f"Analysis result: {json.dumps(analysis, indent=2)}")

    result = configs_collection.update_one(
        {"device_ip": data.get("device_ip")},
        {"$set": data},
        upsert=True
    )

    return {
        "message": "Configuration and analysis received",
        "score": analysis.get("score", 0),
        "issues": (
            len(analysis.get("misconfigurations", [])) +
            len(analysis.get("missing_recommendations", [])) +
            len(analysis.get("interconnection_issues", []))
        ),
        "analysis": analysis,
        "debug": {
            "device_type": device_type,
            "section_keys": list(data.get("sections", {}).keys()),
            "parsed_keys": list(data.get("sections", {}).get("parsed_config", {}).keys()),
            "rules_loaded": analysis.get("rules_loaded", []),
            "upserted": result.upserted_id is not None,
            "updated_existing": result.matched_count
        }
    }

@router.get("/configs")
def get_configs():
    return list(configs_collection.find({}, {"_id": 0}))