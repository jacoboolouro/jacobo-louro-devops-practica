# jacobo-devops-practica

**Autor:** Jacobo (@jacoboolouro)

## Descripción

Aplicación Python desarrollada en la Práctica 2: una **calculadora expuesta como API REST**
(Flask). Recibe dos números y una operación (suma, resta, multiplicación, división o
potencia) y devuelve el resultado en JSON. Este repositorio se usa para practicar control
de versiones con Git/GitHub (ramas `feature/*`, commits y Pull Requests) y la
contenerización con Docker.

## Estructura del proyecto

```
.
├── src/
│   ├── app.py          # API Flask (endpoints /, /health, /calcular)
│   └── calculos.py     # Lógica de la calculadora
├── tests/              # Pruebas unitarias (pytest)
├── requirements.txt    # Dependencias con versiones fijadas
├── Dockerfile
├── .dockerignore
└── README.md
```

## Ejecución sin Docker (opcional)

```bash
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.app                # Arranca en http://localhost:5000
```

## Docker

### 1. Construir la imagen

Desde la raíz del repositorio:

```bash
docker build -t calculadora-devops:1.0.0 .
docker tag calculadora-devops:1.0.0 calculadora-devops:latest
```

La imagen se basa en `python:3.12-slim`, instala las dependencias de
`requirements.txt` sin caché de pip, copia el código de `src/` y se ejecuta con un
usuario sin privilegios (`appuser`). El fichero `.dockerignore` evita copiar `.git`,
entornos virtuales, cachés, tests y secretos (`.env`).

### 2. Ejecutar el contenedor

```bash
# Ejecución básica: publica el puerto 5000 del contenedor en el 8080 del host
docker run -d --name calculadora -p 8080:5000 calculadora-devops:1.0.0

# Cambiando variables de entorno
docker run -d --name calculadora -p 8080:8000 \
  -e PORT=8000 -e APP_NAME=mi-calculadora \
  calculadora-devops:1.0.0

# Ver logs y parar
docker logs calculadora
docker stop calculadora && docker rm calculadora
```

### 3. Variables de entorno soportadas

| Variable   | Valor por defecto     | Descripción                                  |
|------------|-----------------------|----------------------------------------------|
| `PORT`     | `5000`                | Puerto en el que escucha la API en el contenedor |
| `APP_NAME` | `calculadora-devops`  | Nombre que devuelve el endpoint `/`          |

No se necesita ningún secreto. Si en el futuro hiciera falta, se pasaría con `-e` o
`--env-file .env` (el `.env` está excluido de Git y de la imagen).

### 4. Pruebas y salida esperada

Con el contenedor arrancado en el puerto 8080:

```bash
curl http://localhost:8080/health
# {"status":"ok"}

curl "http://localhost:8080/calcular?op=suma&a=2&b=3"
# {"a":2.0,"b":3.0,"operacion":"suma","resultado":5.0}

curl "http://localhost:8080/calcular?op=division&a=1&b=0"
# {"error":"No se puede dividir entre cero"}   (HTTP 400)

curl http://localhost:8080/
# {"app":"calculadora-devops","mensaje":"API de la calculadora. ...","operaciones":[...]}
```

Operaciones disponibles: `suma`, `resta`, `multiplicacion`, `division`, `potencia`.
También se puede abrir en el navegador: http://localhost:8080/calcular?op=potencia&a=2&b=10

En los logs del contenedor (`docker logs calculadora`) debe verse el arranque de
gunicorn: `Listening at: http://0.0.0.0:5000`.

### 5. Publicar y descargar la imagen (Docker Hub)

```bash
docker login
docker tag calculadora-devops:1.0.0 <usuario-dockerhub>/calculadora-devops:1.0.0
docker tag calculadora-devops:1.0.0 <usuario-dockerhub>/calculadora-devops:latest
docker push <usuario-dockerhub>/calculadora-devops:1.0.0
docker push <usuario-dockerhub>/calculadora-devops:latest

# En cualquier otra máquina
docker pull <usuario-dockerhub>/calculadora-devops:1.0.0
docker run -d -p 8080:5000 <usuario-dockerhub>/calculadora-devops:1.0.0
```

## Flujo de trabajo Git

- `main`: rama principal y estable (protegida, solo se modifica mediante Pull Request).
- `feature/docker`: contenerización de la aplicación (Práctica 3.2), fusionada en
  `main` mediante Pull Request.
