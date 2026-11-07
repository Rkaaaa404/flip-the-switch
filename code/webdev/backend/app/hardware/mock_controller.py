import time
from typing import Dict, Any
from app.hardware.controller import BaseHardwareController

# TODO: Check if this mock controller have the functions align with the made schemas in hardware.py


class MockHardwareController(BaseHardwareController):
    """
    Simulated Hardware Controller for local laptop development, Docker containers,
    and COMPFEST judge evaluation without physical Raspberry Pi GPIO pins.
    """

    def __init__(self):
        self.conveyor_status = "ACTIVE"
        self.tower_light = "GREEN"
        self.buzzer = "OFF"
        self.camera_status = "ONLINE"
        print("🛠️ [MOCK HARDWARE] Controller initialized in SIMULATION mode.")

    def trigger_signal(self, signal: str) -> Dict[str, Any]:
        signal = signal.upper()
        
        if signal == "GREEN":
            self.conveyor_status = "ACTIVE"
            self.tower_light = "GREEN"
            self.buzzer = "OFF"
            log_badge = "\033[92m[SIGNAL: GREEN]\033[0m"
            action_desc = "Conveyor Running (Normal Speed) | Buzzer OFF"

        elif signal == "YELLOW":
            self.conveyor_status = "ACTIVE"
            self.tower_light = "YELLOW"
            self.buzzer = "ACTIVE"
            log_badge = "\033[93m[SIGNAL: YELLOW]\033[0m"
            action_desc = "Conveyor Running | Yellow Indicator ON | Short Beep (Secondary Check)"

        elif signal == "RED":
            self.conveyor_status = "STOPPED"
            self.tower_light = "RED"
            self.buzzer = "ACTIVE"
            log_badge = "\033[91m[SIGNAL: RED]\033[0m"
            action_desc = "RELAY TRIGGERED -> Conveyor Motor STOPPED | Continuous Alarm ON"

        else:
            log_badge = "[SIGNAL: UNKNOWN]"
            action_desc = "No state change."

        # Structured terminal log for demonstration / proof-of-work video
        print(f"🏭 [MOCK HARDWARE] {log_badge} {action_desc}")
        
        return self.get_status()

    def get_status(self) -> Dict[str, Any]:
        return {
            "camera": self.camera_status,
            "conveyor_relay": self.conveyor_status,
            "tower_light": self.tower_light,
            "buzzer": self.buzzer,
            "mock_mode": True
        }

    def test_connection(self, ip_address: str) -> Dict[str, Any]:
        # Simulated ping for network hardware test
        time.sleep(0.05)
        return {
            "success": True,
            "message": f"Successfully pinged edge device at {ip_address}",
            "latency_ms": 14
        }

    def cleanup(self) -> None:
        print("🛑 [MOCK HARDWARE] Cleanup completed. Signals reset.")