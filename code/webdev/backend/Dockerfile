FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for OpenCV and networking
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for ultra-fast dependency resolution inside Docker
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project definition files
COPY pyproject.toml uv.lock* ./

# Install Python dependencies into system Python
RUN uv pip install --system --no-cache . || uv pip install --system --no-cache "fastapi[standard]>=0.115.0" "numpy>=1.26.0" "onnxruntime>=1.18.0" "opencv-python-headless>=4.9.0" "pillow>=10.0.0" "pydantic-settings>=2.0.0" "python-multipart>=0.0.9" "sqlalchemy>=2.0.0" "httpx>=0.27.0" "websockets>=12.0"

# Copy backend application source code
COPY . .

# Create persistent storage directories
RUN mkdir -p uploads models_weights

EXPOSE 8000

ENV ENABLE_MOCK_HARDWARE=true
ENV DATABASE_URL=sqlite:///./nusaqc.db

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]