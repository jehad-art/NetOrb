from fastapi import FastAPI
from routes.devices import router as device_router
from settings import settings

app = FastAPI(title="Network Security SaaS")

app.include_router(device_router, prefix="/devices", tags=["Devices"])

@app.get("/")
def root():
    return {"message": "Network Security Backend is running"}