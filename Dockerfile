# Dockerfile
# Image de base officielle — slim = allégée (~50 Mo)
FROM python:3.11-slim

# Éviter les fichiers .pyc et forcer les logs en temps réel
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Répertoire de travail dans le conteneur
WORKDIR /app

# IMPORTANT : copier requirements AVANT le code
# → Docker réutilise ce layer en cache si requirements.txt ne change pas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY src/ ./src/
# Copier les tests
COPY tests/ ./tests/

# Sécurité : ne PAS tourner en root
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Healthcheck : Docker vérifie que l'app répond
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]