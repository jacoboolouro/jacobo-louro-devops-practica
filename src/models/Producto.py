class Producto:
    """Producto genérico de la tienda."""

    tipo = "generico"

    def __init__(self, id: int, nombre: str, precio: float, stock: int):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def hay_stock(self, cantidad: int) -> bool:
        return self.stock >= cantidad

    def reducir_stock(self, cantidad: int) -> None:
        if not self.hay_stock(cantidad):
            raise ValueError(f"Stock insuficiente para '{self.nombre}'")
        self.stock -= cantidad

    def __str__(self) -> str:
        return f"{self.nombre} - {self.precio:.2f} € (stock: {self.stock})"


class ProductoElectronico(Producto):
    """Producto electrónico con meses de garantía."""

    tipo = "electronico"

    def __init__(self, id: int, nombre: str, precio: float, stock: int, meses_garantia: int):
        super().__init__(id, nombre, precio, stock)
        self.meses_garantia = meses_garantia

    def __str__(self) -> str:
        return f"{super().__str__()} - Garantía: {self.meses_garantia} meses"


class ProductoRopa(Producto):
    """Prenda de ropa con talla y color."""

    tipo = "ropa"

    def __init__(self, id: int, nombre: str, precio: float, stock: int, talla: str, color: str):
        super().__init__(id, nombre, precio, stock)
        self.talla = talla
        self.color = color

    def __str__(self) -> str:
        return f"{super().__str__()} - Talla: {self.talla}, Color: {self.color}"
