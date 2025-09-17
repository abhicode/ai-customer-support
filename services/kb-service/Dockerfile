# syntax=docker/dockerfile:1

FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# System deps for FAISS + transformers
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    wget \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Install torch with CUDA first
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir torch==2.4.0+cu121 torchvision==0.19.0+cu121 torchaudio==2.4.0+cu121 \
       --index-url https://download.pytorch.org/whl/cu121 \
    && pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
