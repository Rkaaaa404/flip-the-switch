"""Domain errors raised by delivery traceability services; the API layer maps them to HTTP codes."""


class DeliveryServiceError(Exception):
    """Base class for delivery traceability domain errors."""


class NotFoundError(DeliveryServiceError):
    """Referenced delivery, disposition or lot does not exist (404)."""


class DeliveryStateError(DeliveryServiceError):
    """Operation not allowed in the delivery's current status (409)."""


class QuantityValidationError(DeliveryServiceError):
    """Quantity, unit or lineage reference violates an accounting invariant (422)."""


class InvalidImageError(DeliveryServiceError):
    """Uploaded capture could not be decoded as an image (422)."""


class CaptureBackpressureError(DeliveryServiceError):
    """Too many captures are queued for inference (503)."""


class InsufficientStorageError(DeliveryServiceError):
    """Not enough free disk space to start a capture session (507)."""
