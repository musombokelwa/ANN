# Dockerfile pour Network Quality Prediction API
# Déploiement avec Docker

FROM python:3.10-slim

WORKDIR /app

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libhdf5-dev \
    libopenblas-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier les requirements
COPY requirements-api.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements-api.txt

# Copier le code de l'application
COPY run.py .
COPY config.py .
COPY app app/
COPY templates templates/
COPY static static/
COPY model model/

# Exposer le port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Lancer l'application avec Gunicorn
CMD ["gunicorn", \
    "--bind", "0.0.0.0:5000", \
    "--workers", "4", \
    "--worker-class", "sync", \
    "--timeout", "60", \
    "--access-logfile", "-", \
    "--error-logfile", "-", \
    "run:app"]
