from datetime import datetime

from models.Producto import Producto
from models.Usuario import Cliente


class Pedido:
    """Pedido realizado por un cliente. Cada línea es una tupla (producto, cantidad)."""

    def __init__(self, id: int, cliente: Cliente, lineas: list[tuple[Producto, int]]):
        self.id = id
        self.cliente = cliente
        self.lineas = lineas
        self.fecha = datetime.now()

    def calcular_total(self) -> float:
        return round(sum(producto.precio * cantidad for producto, cantidad in self.lineas), 2)

    def __str__(self) -> str:
        return (
            f"Pedido {self.id} - {self.cliente.nombre} - "
            f"{self.fecha:%d/%m/%Y %H:%M} - Total: {self.calcular_total():.2f} €"
        )
