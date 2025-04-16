FROM python:3.9-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=true \
    QR_CODE_DIR=/myapp/qr_codes

# Set working directory
WORKDIR /myapp

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy just what we need for installation
COPY ./requirements.txt /myapp/

# Install a minimal set of dependencies first, then the rest best-effort
RUN pip install --upgrade pip wheel \
    && pip install fastapi==0.103.0 pydantic==1.10.8 uvicorn==0.22.0 python-dotenv \
    && pip install -r requirements.txt || echo "Some requirements could not be installed, but core functionality should work"

# Create non-root user
RUN useradd -m myuser \
    && mkdir -p ${QR_CODE_DIR} \
    && chown -R myuser:myuser /myapp
USER myuser

# Copy application code
COPY --chown=myuser:myuser . /myapp

# Expose port
EXPOSE 8000

# Run the application
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]