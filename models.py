from pydantic import BaseModel, Field
from typing import Optional, List

class DeviceIn(BaseModel):
    ip: str
    open_ports: List[int]
    hostname: Optional[str] = None
    mac: Optional[str] = None

class DeviceOut(DeviceIn):
    device_type: Optional[str] = None
    status: Optional[str] = "discovered"
    last_seen: Optional[str] = None
    credentials: Optional[dict] = None