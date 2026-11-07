"""Shared pytest fixtures: isolated SQLite database, fake inference engine and HTTP client.

Environment variables must be set before any ``app`` module is imported, because
``app.config.settings`` and ``app.core.database.engine`` are built at import time.
"""

import io
import os
import tempfile

_TMP = tempfile.mkdtemp()
os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(_TMP, "test.db").replace("\\", "/")
os.environ["UPLOAD_DIR"] = os.path.join(_TMP, "uploads")
os.makedirs(os.environ["UPLOAD_DIR"], exist_ok=True)
os.environ["CAPTURE_MIN_FREE_BYTES"] = "0"
os.environ["QC_AGENT_TOKEN"] = AGENT_TOKEN = "test-agent-token"
os.environ["QC_GATE_TOKEN"] = GATE_TOKEN = "test-gate-token"

import pytest
from fastapi.testclient import TestClient
from PIL import Image

import app.models  # noqa: F401  (registers every table on Base.metadata)
from app.core.database import Base, SessionLocal, engine
from app.main import app as fastapi_app
from app.schemas.delivery_trace import DeliveryCreate
from app.services import material_lineage_service, two_view_inspection_service


class FakeEngine:
    """Stands in for AIInferenceEngine. Grades and defects are consumed one entry per call."""

    def __init__(self):
        self.freshness_session = None
        self.defect_session = None
        self.grades: list[str] = []
        self.defects: list[list[dict]] = []
        self.freshness_calls = 0
        self.defect_calls = 0

    def predict_freshness(self, pil):
        self.freshness_calls += 1
        grade = self.grades.pop(0) if self.grades else "A"
        return {"grade": grade, "confidence": 0.9}

    def predict_defects(self, pil):
        self.defect_calls += 1
        return self.defects.pop(0) if self.defects else []


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def fake_engine(monkeypatch):
    fake = FakeEngine()
    monkeypatch.setattr(two_view_inspection_service, "get_ai_engine", lambda: fake)
    return fake


@pytest.fixture
def jpeg_bytes() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (64, 48), (120, 200, 90)).save(buf, format="JPEG")
    return buf.getvalue()


@pytest.fixture
def png_bytes() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (32, 24), (10, 20, 200)).save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def client():
    """HTTP client that signs as qc-gate, so the existing write-route tests keep exercising the service."""
    with TestClient(fastapi_app, headers={"X-Api-Token": GATE_TOKEN}) as c:
        yield c


@pytest.fixture
def anon_client():
    with TestClient(fastapi_app) as c:
        yield c


@pytest.fixture
def make_delivery():
    """Factory: make_delivery(db, now=None, **overrides) -> ReceivingDelivery in active_receiving."""

    def _make(db, now=None, **overrides):
        fields = {
            "supplier_name": "Supplier A",
            "species": "Oreochromis niloticus",
            "fish_family": "Cichlidae",
            "stated_quantity": 500.0,
            "quantity_unit": "kg",
            "truck_identifier": "B 1234 XY",
            "created_by": "qc.tester",
        }
        fields.update(overrides)
        return material_lineage_service.create_delivery(db, DeliveryCreate(**fields), now=now)

    return _make
