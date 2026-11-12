# Práctica 3.2 - Imagen de la calculadora (Práctica 2)
FROM python:3.12-slim

# Evita ficheros .pyc y muestra los logs sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    APP_NAME=calculadora-devops

WORKDIR /app

# 1) Dependencias primero para aprovechar la caché de capas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Código fuente
COPY src/ ./src/

# 3) Usuario sin privilegios y permisos para ejecutar el código
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app \
    && chmod -R u+rx /app/src
USER appuser

EXPOSE 5000

# 4) Comando de inicio
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 2 src.app:app"]
