from pydantic import BaseModel
from typing import Literal, Optional

DeviceStatus = Literal["ONLINE", "OFFLINE", "WARNING", "ACTIVE", "STOPPED"]

class HardwareStatusSchema(BaseModel):
    camera: DeviceStatus
    conveyor_relay: DeviceStatus
    tower_light: Literal["GREEN", "YELLOW", "RED", "OFF"]
    buzzer: Literal["ACTIVE", "OFF"]
    mock_mode: bool

class ConnectionTestRequest(BaseModel):
    ip_address: str

class ConnectionTestResponse(BaseModel):
    success: bool
    message: str
    latency_ms: Optional[int] = None


#   camera: "ONLINE" | "OFFLINE";
#   conveyor_relay: "ACTIVE" | "INACTIVE";
#   tower_light: "GREEN" | "YELLOW" | "RED";
#   mock_mode_enabled: boolean;