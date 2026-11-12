from models import (
    Administrador,
    Cliente,
    Pedido,
    Producto,
    ProductoElectronico,
    ProductoRopa,
    Usuario,
)


class TiendaService:
    """Lógica de negocio de la tienda. Los datos se guardan en memoria.

    Errores que lanza:
      - LookupError: el usuario o el producto indicado no existe.
      - ValueError: los datos no cumplen una regla de negocio (email repetido,
        stock insuficiente, el usuario no es un cliente...).
    """

    def __init__(self):
        self.usuarios: dict[int, Usuario] = {}
        self.productos: dict[int, Producto] = {}
        self.pedidos: dict[int, Pedido] = {}
        self._siguiente_id_usuario = 1
        self._siguiente_id_producto = 1
        self._siguiente_id_pedido = 1

    # ---------------------------------------------------------------- Usuarios

    def registrar_usuario(self, nombre: str, email: str, tipo: str, direccion_postal: str | None = None) -> Usuario:
        if any(u.email.lower() == email.lower() for u in self.usuarios.values()):
            raise ValueError(f"Ya existe un usuario con el email {email}")

        id = self._siguiente_id_usuario
        if tipo == "cliente":
            usuario = Cliente(id, nombre, email, direccion_postal)
        elif tipo == "administrador":
            usuario = Administrador(id, nombre, email)
        else:
            raise ValueError(f"Tipo de usuario no válido: {tipo}")

        self.usuarios[id] = usuario
        self._siguiente_id_usuario += 1
        return usuario

    def obtener_usuario(self, usuario_id: int) -> Usuario | None:
        return self.usuarios.get(usuario_id)

    def listar_usuarios(self) -> list[Usuario]:
        return list(self.usuarios.values())

    # --------------------------------------------------------------- Productos

    def crear_producto(
        self,
        tipo: str,
        nombre: str,
        precio: float,
        stock: int,
        meses_garantia: int | None = None,
        talla: str | None = None,
        color: str | None = None,
    ) -> Producto:
        id = self._siguiente_id_producto
        if tipo == "generico":
            producto = Producto(id, nombre, precio, stock)
        elif tipo == "electronico":
            producto = ProductoElectronico(id, nombre, precio, stock, meses_garantia)
        elif tipo == "ropa":
            producto = ProductoRopa(id, nombre, precio, stock, talla, color)
        else:
            raise ValueError(f"Tipo de producto no válido: {tipo}")

        self.productos[id] = producto
        self._siguiente_id_producto += 1
        return producto

    def listar_productos(self) -> list[Producto]:
        return list(self.productos.values())

    def obtener_producto(self, producto_id: int) -> Producto | None:
        return self.productos.get(producto_id)

    def eliminar_producto(self, producto_id: int) -> bool:
        return self.productos.pop(producto_id, None) is not None

    # ----------------------------------------------------------------- Pedidos

    def crear_pedido(self, cliente_id: int, items: list[tuple[int, int]]) -> Pedido:
        """Crea un pedido. `items` es una lista de tuplas (producto_id, cantidad)."""
        cliente = self.obtener_usuario(cliente_id)
        if cliente is None:
            raise LookupError(f"No existe el cliente con id {cliente_id}")
        if not isinstance(cliente, Cliente):
            raise ValueError(f"El usuario con id {cliente_id} no es un cliente")

        # Se comprueba todo antes de tocar el stock, para no dejar pedidos a medias.
        lineas: list[tuple[Producto, int]] = []
        cantidad_total: dict[int, int] = {}
        for producto_id, cantidad in items:
            producto = self.obtener_producto(producto_id)
            if producto is None:
                raise LookupError(f"No existe el producto con id {producto_id}")
            cantidad_total[producto_id] = cantidad_total.get(producto_id, 0) + cantidad
            if not producto.hay_stock(cantidad_total[producto_id]):
                raise ValueError(
                    f"Stock insuficiente para '{producto.nombre}' "
                    f"(disponible: {producto.stock}, solicitado: {cantidad_total[producto_id]})"
                )
            lineas.append((producto, cantidad))

        for producto, cantidad in lineas:
            producto.reducir_stock(cantidad)

        pedido = Pedido(self._siguiente_id_pedido, cliente, lineas)
        self.pedidos[pedido.id] = pedido
        self._siguiente_id_pedido += 1
        return pedido

    def obtener_pedidos_cliente(self, cliente_id: int) -> list[Pedido]:
        cliente = self.obtener_usuario(cliente_id)
        if cliente is None:
            raise LookupError(f"No existe el cliente con id {cliente_id}")
        if not isinstance(cliente, Cliente):
            raise ValueError(f"El usuario con id {cliente_id} no es un cliente")
        return [p for p in self.pedidos.values() if p.cliente.id == cliente_id]
