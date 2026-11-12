# Práctica 3.2 - Imagen de la API de la Tienda Online (Práctica 2)
FROM python:3.12-slim

# Vincula la imagen publicada con este repositorio de GitHub
LABEL org.opencontainers.image.source="https://github.com/jacoboolouro/jacobo-devops-practica" \
      org.opencontainers.image.description="API de la Tienda Online (Práctica 2)"

# Evita ficheros .pyc y muestra los logs sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

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

# El código importa sus módulos (models, Services, schemas) desde src/
WORKDIR /app/src

EXPOSE 8000

# 4) Comando de inicio
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
