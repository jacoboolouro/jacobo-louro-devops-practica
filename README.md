# jacobo-devops-practica

**Autor:** Jacobo Louro Rodríguez-Volta

## Descripción

**Tienda Online**: aplicación Python desarrollada en la Práctica 2. Es una **API REST
con FastAPI** que gestiona los usuarios (clientes y administradores), los productos
(genéricos, electrónicos y de ropa) y los pedidos de una tienda, con los datos en memoria.
Incluye un cliente HTTP de ejemplo (`cliente/cliente.py`) y un frontend web sencillo
(`frontend/index.html`).

Este repositorio se usa para practicar control de versiones con Git/GitHub (ramas
`feature/*`, commits y Pull Requests) y la contenerización con Docker.

## Estructura del proyecto

```
.
├── src/
│   ├── main.py             # API FastAPI (endpoints de usuarios, productos y pedidos)
│   ├── schemas.py          # Esquemas Pydantic de entrada y salida
│   ├── models/             # Clases Usuario, Producto y Pedido
│   └── Services/           # Lógica de negocio (TiendaService)
├── cliente/cliente.py      # Cliente HTTP que prueba la API con requests
├── frontend/index.html     # Frontend web que consume la API
├── tests/                  # Pruebas unitarias (pytest)
├── requirements.txt        # Dependencias con versiones fijadas
├── .github/workflows/      # Publicación automática de la imagen
├── Dockerfile
├── .dockerignore
└── README.md
```

## Endpoints de la API

| Método | Ruta                       | Descripción                      |
|--------|----------------------------|----------------------------------|
| POST   | `/usuarios`                | Registra un usuario              |
| GET    | `/usuarios`                | Lista los usuarios               |
| GET    | `/usuarios/{id}`           | Consulta un usuario              |
| POST   | `/productos`               | Crea un producto                 |
| GET    | `/productos`               | Lista los productos              |
| GET    | `/productos/{id}`          | Consulta un producto             |
| DELETE | `/productos/{id}`          | Elimina un producto              |
| POST   | `/pedidos`                 | Crea un pedido                   |
| GET    | `/usuarios/{id}/pedidos`   | Lista los pedidos de un cliente  |

La documentación interactiva (Swagger) está en `/docs`.

## Ejecución sin Docker (opcional)

```bash
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd src
python main.py                   # Arranca en http://localhost:8000
```

Con la API arrancada, en otra terminal: `python cliente/cliente.py`, o abrir
`frontend/index.html` en el navegador.

## Docker

### 1. Construir la imagen

Desde la raíz del repositorio:

```bash
docker build -t tienda-online:1.0.0 .
docker tag tienda-online:1.0.0 tienda-online:latest
```

La imagen se basa en `python:3.12-slim`, instala las dependencias de
`requirements.txt` sin caché de pip, copia el código de `src/` y se ejecuta con un
usuario sin privilegios (`appuser`). El fichero `.dockerignore` evita copiar `.git`,
entornos virtuales, cachés, tests y secretos (`.env`).

### 2. Ejecutar el contenedor

```bash
# Ejecución básica: la API queda en http://localhost:8000
docker run -d --name tienda -p 8000:8000 tienda-online:1.0.0

# Cambiando el puerto interno con una variable de entorno
docker run -d --name tienda -p 8000:9000 -e PORT=9000 tienda-online:1.0.0

# Ver logs y parar
docker logs tienda
docker stop tienda && docker rm tienda
```

Se publica en el puerto 8000 del host porque el cliente (`cliente/cliente.py`) y el
frontend (`frontend/index.html`) llaman a `http://localhost:8000`.

### 3. Variables de entorno soportadas

| Variable | Valor por defecto | Descripción                                       |
|----------|-------------------|---------------------------------------------------|
| `PORT`   | `8000`            | Puerto en el que escucha la API dentro del contenedor |

No se necesita ningún secreto. Si en el futuro hiciera falta, se pasaría con `-e` o
`--env-file .env` (el `.env` está excluido de Git y de la imagen).

### 4. Pruebas y salida esperada

Con el contenedor arrancado en el puerto 8000:

```bash
# Crear un cliente
curl -X POST http://localhost:8000/usuarios -H "Content-Type: application/json" \
  -d '{"nombre":"Laura","email":"laura@correo.com","tipo":"cliente","direccion_postal":"Calle Real 10"}'
# {"id":1,"nombre":"Laura","email":"laura@correo.com","es_admin":false}

# Crear un producto
curl -X POST http://localhost:8000/productos -H "Content-Type: application/json" \
  -d '{"tipo":"electronico","nombre":"Auriculares","precio":59.99,"stock":10,"meses_garantia":24}'
# {"id":1,"tipo":"electronico","nombre":"Auriculares","precio":59.99,"stock":10,"meses_garantia":24,"talla":null,"color":null}

# Crear un pedido de 2 unidades
curl -X POST http://localhost:8000/pedidos -H "Content-Type: application/json" \
  -d '{"cliente_id":1,"items":[{"producto_id":1,"cantidad":2}]}'
# {"id":1,"fecha":"...","cliente_id":1,"total":119.98,"items":[...]}

# Listar productos (el stock baja a 8)
curl http://localhost:8000/productos
```

Otras formas de probarlo:

- Abrir http://localhost:8000/docs y usar la documentación interactiva (Swagger).
- Ejecutar el cliente de ejemplo: `python cliente/cliente.py` (necesita `requests`).
- Abrir `frontend/index.html` en el navegador.

En los logs del contenedor (`docker logs tienda`) debe verse
`Uvicorn running on http://0.0.0.0:8000`.

Los datos se guardan en memoria: al parar el contenedor se pierden.

### 5. Publicar y descargar la imagen (GitHub Container Registry)

La imagen se publica en el registry de GitHub (ghcr.io) de forma automática: el
workflow `.github/workflows/docker-publish.yml` se ejecuta en cada push a `main` y sigue
el flujo **build → run → test → push**.

Descargar y ejecutar la imagen publicada en cualquier máquina:

```bash
docker pull ghcr.io/jacoboolouro/jacobo-devops-practica:1.0.0
docker run -d --name tienda -p 8000:8000 ghcr.io/jacoboolouro/jacobo-devops-practica:1.0.0
```

Publicarla a mano (alternativa al workflow), con un token de GitHub con permiso
`write:packages` guardado en la variable de entorno `GHCR_TOKEN`:

```bash
echo "$GHCR_TOKEN" | docker login ghcr.io -u jacoboolouro --password-stdin
docker tag tienda-online:1.0.0 ghcr.io/jacoboolouro/jacobo-devops-practica:1.0.0
docker push ghcr.io/jacoboolouro/jacobo-devops-practica:1.0.0
```

## Flujo de trabajo Git

- `main`: rama principal y estable (protegida, solo se modifica mediante Pull Request).
- `feature/docker`: contenerización de la aplicación (Práctica 3.2), fusionada en
  `main` mediante Pull Request.
- `feature/tienda-online`: código de la Práctica 2, fusionada mediante Pull Request.
