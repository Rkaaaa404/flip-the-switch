# backend/app/api/v1/hardware.py
from fastapi import APIRouter, Request, status
from app.hardware import get_hardware_controller

router = APIRouter()

@router.get(
    "/status",
    status_code=status.HTTP_200_OK,
    summary="Get Hardware Peripheral & Actuator Status",
    description="Powers HardwareStatus.tsx on dashboard and settings pages."
)
def get_hardware_status():
    hw = get_hardware_controller()
    raw_status = hw.get_status()

    camera_status = raw_status.get("camera", "ONLINE")
    conveyor_status = raw_status.get("conveyor_relay", "ACTIVE")
    tower_light = raw_status.get("tower_light", "GREEN")
    buzzer_status = raw_status.get("buzzer", "OFF")
    mock_mode = raw_status.get("mock_mode", True)

    # Return dual-compatible payload (snake_case + camelCase)
    return {
        # Standard snake_case
        "camera": camera_status,
        "conveyor_relay": conveyor_status,
        "tower_light": tower_light,
        "buzzer": buzzer_status,
        "mock_mode": mock_mode,

        # Frontend camelCase aliases
        "conveyor": conveyor_status,
        "towerLight": tower_light,
        "mockMode": mock_mode,
        "mockModeEnabled": mock_mode
    }

@router.post(
    "/test-connection",
    status_code=status.HTTP_200_OK,
    summary="Test Connection to Edge Hardware / IP Camera",
    description="Tests network connectivity to the target IP address configured in Hardware.tsx."
)
async def test_hardware_connection(request: Request):
    payload = await request.json()
    
    # Accepts both 'ip_address' and 'ipAddress'
    ip_addr = payload.get("ip_address") or payload.get("ipAddress") or "127.0.0.1"
    
    hw = get_hardware_controller()
    result = hw.test_connection(ip_addr)
    
    latency = result.get("latency_ms", 15)
    success = result.get("success", True)
    msg = result.get("message", f"Successfully connected to {ip_addr}")

    # Return dual-compatible payload
    return {
        "success": success,
        "message": msg,
        "latency_ms": latency,
        "latencyMs": latency
    }