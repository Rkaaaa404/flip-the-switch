from typing import Generator
from app.core.database import get_db

# Re-export get_db for convenient dependency injection in routes
__all__ = ["get_db"]