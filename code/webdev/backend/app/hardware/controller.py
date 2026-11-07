from abc import ABC, abstractmethod
from typing import Dict, Any

# TODO: Check if this abstract class is still needed or if it can be removed

class BaseHardwareController(ABC):
    """
    Abstract Base Class for hardware actuators.
    Guarantees identical interface whether running on physical Raspberry Pi or Mock mode.
    """

    @abstractmethod
    def trigger_signal(self, signal: str) -> Dict[str, Any]:
        """
        Actuates hardware based on inspection signal: 'GREEN', 'YELLOW', or 'RED'.
        Returns current state summary.
        """
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """
        Returns real-time status of connected peripheral components.
        """
        pass

    @abstractmethod
    def test_connection(self, ip_address: str) -> Dict[str, Any]:
        """
        Pings or verifies connectivity to edge camera / industrial workstation.
        """
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """
        Safely shuts down pins and relays on application shutdown.
        """
        pass