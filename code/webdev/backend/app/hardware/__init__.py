from app.config import settings
from app.hardware.controller import BaseHardwareController
from app.hardware.mock_controller import MockHardwareController
from app.hardware.gpio_controller import GPIOController

_hardware_instance: BaseHardwareController = None

def get_hardware_controller() -> BaseHardwareController:
    """
    Singleton factory: Returns GPIOController if running on real hardware,
    otherwise returns MockHardwareController.
    """
    global _hardware_instance
    if _hardware_instance is None:
        if settings.ENABLE_MOCK_HARDWARE:
            _hardware_instance = MockHardwareController()
        else:
            try:
                _hardware_instance = GPIOController()
                if not getattr(_hardware_instance, "available", False):
                    print("⚠️ Falling back to MockHardwareController.")
                    _hardware_instance = MockHardwareController()
            except Exception:
                _hardware_instance = MockHardwareController()
                
    return _hardware_instance