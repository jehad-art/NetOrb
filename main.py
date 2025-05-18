from fastapi import FastAPI
from routes.devices import router as device_router
from settings import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Network Security SaaS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(device_router, prefix="/devices", tags=["Devices"])

@app.get("/")
def root():
    return {"message": "Network Security Backend is running"}