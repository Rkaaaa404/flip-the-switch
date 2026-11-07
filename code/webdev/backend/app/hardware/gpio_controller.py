from typing import Dict, Any
from app.hardware.controller import BaseHardwareController

# PIN CONFIGURATION (Raspberry Pi 5 BCM standard)
PIN_CONVEYOR_RELAY = 17  # Active LOW Relay for conveyor AC motor
PIN_LIGHT_GREEN = 27     # Green Tower LED
PIN_LIGHT_YELLOW = 22    # Yellow Tower LED
PIN_LIGHT_RED = 23       # Red Tower LED
PIN_BUZZER = 24          # 5V Buzzer

# TODO: Check if this GPIO controller have the functions correctly configured or not

class GPIOController(BaseHardwareController):
    """
    Production Hardware Driver interfacing with physical Raspberry Pi GPIO pins.
    """

    def __init__(self):
        try:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            self.GPIO.setmode(self.GPIO.BCM)
            self.GPIO.setwarnings(False)

            # Setup Output Pins
            pins = [PIN_CONVEYOR_RELAY, PIN_LIGHT_GREEN, PIN_LIGHT_YELLOW, PIN_LIGHT_RED, PIN_BUZZER]
            for pin in pins:
                self.GPIO.setup(pin, self.GPIO.OUT)

            # Initial State: Conveyor Normal, Green Light ON
            self.trigger_signal("GREEN")
            self.available = True
            print("⚡ [GPIO HARDWARE] Physical Raspberry Pi GPIO initialized successfully.")
        except Exception as e:
            self.available = False
            print(f"⚠️ [GPIO HARDWARE] Physical GPIO unavailable ({str(e)}). Fallback required.")

    def trigger_signal(self, signal: str) -> Dict[str, Any]:
        if not self.available:
            return {"error": "GPIO not available"}

        signal = signal.upper()

        if signal == "GREEN":
            self.GPIO.output(PIN_CONVEYOR_RELAY, self.GPIO.HIGH) # Relay engaged (motor on)
            self.GPIO.output(PIN_LIGHT_GREEN, self.GPIO.HIGH)
            self.GPIO.output(PIN_LIGHT_YELLOW, self.GPIO.LOW)
            self.GPIO.output(PIN_LIGHT_RED, self.GPIO.LOW)
            self.GPIO.output(PIN_BUZZER, self.GPIO.LOW)
            current_tower = "GREEN"
            conveyor = "ACTIVE"
            buzzer = "OFF"

        elif signal == "YELLOW":
            self.GPIO.output(PIN_CONVEYOR_RELAY, self.GPIO.HIGH)
            self.GPIO.output(PIN_LIGHT_GREEN, self.GPIO.LOW)
            self.GPIO.output(PIN_LIGHT_YELLOW, self.GPIO.HIGH)
            self.GPIO.output(PIN_LIGHT_RED, self.GPIO.LOW)
            self.GPIO.output(PIN_BUZZER, self.GPIO.HIGH)
            current_tower = "YELLOW"
            conveyor = "ACTIVE"
            buzzer = "ACTIVE"

        elif signal == "RED":
            self.GPIO.output(PIN_CONVEYOR_RELAY, self.GPIO.LOW) # Relay open (motor STOP)
            self.GPIO.output(PIN_LIGHT_GREEN, self.GPIO.LOW)
            self.GPIO.output(PIN_LIGHT_YELLOW, self.GPIO.LOW)
            self.GPIO.output(PIN_LIGHT_RED, self.GPIO.HIGH)
            self.GPIO.output(PIN_BUZZER, self.GPIO.HIGH)
            current_tower = "RED"
            conveyor = "STOPPED"
            buzzer = "ACTIVE"

        return {
            "camera": "ONLINE",
            "conveyor_relay": conveyor,
            "tower_light": current_tower,
            "buzzer": buzzer,
            "mock_mode": False
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            "camera": "ONLINE",
            "conveyor_relay": "ACTIVE" if self.available else "UNKNOWN",
            "tower_light": "GREEN",
            "buzzer": "OFF",
            "mock_mode": False
        }

    def test_connection(self, ip_address: str) -> Dict[str, Any]:
        import subprocess
        try:
            res = subprocess.run(["ping", "-c", "1", "-W", "1", ip_address], stdout=subprocess.PIPE)
            return {"success": res.returncode == 0, "message": f"Ping exit code: {res.returncode}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def cleanup(self) -> None:
        if self.available:
            self.GPIO.cleanup()