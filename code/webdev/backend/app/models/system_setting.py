# app/models/system_setting.py
from sqlalchemy import Column, String, Integer, Float, Boolean
from app.core.database import Base

class SystemSetting(Base):
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String(64), unique=True, index=True, nullable=False)
    confidence_threshold = Column(Float, default=0.75, nullable=False)
    auto_export_csv = Column(Boolean, default=False, nullable=False)
    log_retention_days = Column(Integer, default=30, nullable=False)
    active_species = Column(String(255), default="Scombridae,Cichlidae,Salmonidae", nullable=False)
    mock_mode_enabled = Column(Boolean, default=True, nullable=False)

