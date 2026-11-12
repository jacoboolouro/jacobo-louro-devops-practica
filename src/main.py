import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from models import Pedido, Producto, Usuario
from schemas import (
    PedidoCreate,
    PedidoItemRead,
    PedidoRead,
    ProductoCreate,
    ProductoRead,
    UsuarioCreate,
    UsuarioRead,
)
from Services import TiendaService

app = FastAPI(title="Tienda Online API")

# Permite que el frontend (abierto en el navegador) haga peticiones a la API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

service = TiendaService()


# ------------------------------------------------- Conversión modelo -> schema

def a_usuario_read(usuario: Usuario) -> UsuarioRead:
    return UsuarioRead(
        id=usuario.id,
        nombre=usuario.nombre,
        email=usuario.email,
        es_admin=usuario.es_admin(),
    )


def a_producto_read(producto: Producto) -> ProductoRead:
    return ProductoRead(
        id=producto.id,
        tipo=producto.tipo,
        nombre=producto.nombre,
        precio=producto.precio,
        stock=producto.stock,
        meses_garantia=getattr(producto, "meses_garantia", None),
        talla=getattr(producto, "talla", None),
        color=getattr(producto, "color", None),
    )


def a_pedido_read(pedido: Pedido) -> PedidoRead:
    return PedidoRead(
        id=pedido.id,
        fecha=pedido.fecha,
        cliente_id=pedido.cliente.id,
        total=pedido.calcular_total(),
        items=[
            PedidoItemRead(
                producto_id=producto.id,
                nombre=producto.nombre,
                precio_unitario=producto.precio,
                cantidad=cantidad,
                subtotal=round(producto.precio * cantidad, 2),
            )
            for producto, cantidad in pedido.lineas
        ],
    )


# ------------------------------------------------------------------ Usuarios

@app.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def crear_usuario(datos: UsuarioCreate):
    try:
        usuario = service.registrar_usuario(datos.nombre, datos.email, datos.tipo, datos.direccion_postal)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return a_usuario_read(usuario)


@app.get("/usuarios", response_model=list[UsuarioRead], tags=["Usuarios"])
def listar_usuarios():
    return [a_usuario_read(u) for u in service.listar_usuarios()]


@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead, tags=["Usuarios"])
def obtener_usuario(usuario_id: int):
    usuario = service.obtener_usuario(usuario_id)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe el usuario con id {usuario_id}")
    return a_usuario_read(usuario)


# ----------------------------------------------------------------- Productos

@app.post("/productos", response_model=ProductoRead, status_code=status.HTTP_201_CREATED, tags=["Productos"])
def crear_producto(datos: ProductoCreate):
    producto = service.crear_producto(
        datos.tipo,
        datos.nombre,
        datos.precio,
        datos.stock,
        meses_garantia=datos.meses_garantia,
        talla=datos.talla,
        color=datos.color,
    )
    return a_producto_read(producto)


@app.get("/productos", response_model=list[ProductoRead], tags=["Productos"])
def listar_productos():
    return [a_producto_read(p) for p in service.listar_productos()]


@app.get("/productos/{producto_id}", response_model=ProductoRead, tags=["Productos"])
def obtener_producto(producto_id: int):
    producto = service.obtener_producto(producto_id)
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe el producto con id {producto_id}")
    return a_producto_read(producto)


@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Productos"])
def eliminar_producto(producto_id: int):
    if not service.eliminar_producto(producto_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe el producto con id {producto_id}")


# ------------------------------------------------------------------- Pedidos

@app.post("/pedidos", response_model=PedidoRead, status_code=status.HTTP_201_CREATED, tags=["Pedidos"])
def crear_pedido(datos: PedidoCreate):
    items = [(item.producto_id, item.cantidad) for item in datos.items]
    try:
        pedido = service.crear_pedido(datos.cliente_id, items)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return a_pedido_read(pedido)


@app.get("/usuarios/{cliente_id}/pedidos", response_model=list[PedidoRead], tags=["Pedidos"])
def listar_pedidos_cliente(cliente_id: int):
    try:
        pedidos = service.obtener_pedidos_cliente(cliente_id)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return [a_pedido_read(p) for p in pedidos]


if __name__ == "__main__":
    # host="0.0.0.0" hace que la API acepte conexiones de otros equipos de la red.
    uvicorn.run(app, host="0.0.0.0", port=8000)
