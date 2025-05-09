# ---- Base stage: builds dependencies into virtualenv ----
    FROM python:3.12-bookworm as base

    ENV PYTHONUNBUFFERED=1 \
        PYTHONFAULTHANDLER=1 \
        PIP_NO_CACHE_DIR=true \
        PIP_DEFAULT_TIMEOUT=100 \
        PIP_DISABLE_PIP_VERSION_CHECK=on \
        QR_CODE_DIR=/myapp/qr_codes
    
    WORKDIR /myapp
    
    # Install build dependencies
    RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        libc-bin \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*
    
    # Install Python dependencies in a virtual environment
    COPY requirements.txt .
    RUN python -m venv /.venv \
        && . /.venv/bin/activate \
        && pip install --upgrade pip \
        && pip install -r requirements.txt
    
    # ---- Final runtime stage ----
    FROM python:3.12-slim-bookworm as final
    
    # Install runtime dependencies (minimal)
    RUN apt-get update && apt-get install -y \
        libc-bin \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*
    
    # Copy virtualenv from build stage
    COPY --from=base /.venv /.venv
    
    # Set environment and path for virtualenv
    ENV PATH="/.venv/bin:$PATH" \
        PYTHONUNBUFFERED=1 \
        PYTHONFAULTHANDLER=1 \
        QR_CODE_DIR=/myapp/qr_codes
    
    WORKDIR /myapp
    
    # Create and switch to non-root user
    RUN useradd -m myuser
    USER myuser
    
    # Copy app code with correct ownership
    COPY --chown=myuser:myuser . .
    
    EXPOSE 8000
    
    # Run the app
    ENTRYPOINT ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
    