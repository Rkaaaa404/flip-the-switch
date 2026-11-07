from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from app.config import settings
from app.core.database import init_db
import app.models
from app.core.websocket import ws_manager
from app.api.v1.router import api_v1_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.MODEL_DIR, exist_ok=True)
    init_db()
    print(f"🚀 {settings.APP_NAME} initialized successfully!")
    print(f"📁 SQLite Database: {settings.DATABASE_URL}")
    print(f"⚙️ Mock Hardware Mode: {settings.ENABLE_MOCK_HARDWARE}")
    yield
    print("🛑 Shutting down backend...")

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving for inspection images
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# REST API routes
app.include_router(api_v1_router, prefix="/api/v1")

# WebSocket Endpoint for live events
@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep-alive loop
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "mock_hardware": settings.ENABLE_MOCK_HARDWARE,
        "database": "connected"
    }