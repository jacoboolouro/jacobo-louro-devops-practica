class Usuario:
    """Usuario base de la tienda."""

    def __init__(self, id: int, nombre: str, email: str):
        self.id = id
        self.nombre = nombre
        self.email = email

    def es_admin(self) -> bool:
        return False

    def __str__(self) -> str:
        return f"{self.nombre} <{self.email}>"


class Cliente(Usuario):
    """Cliente que puede realizar pedidos."""

    def __init__(self, id: int, nombre: str, email: str, direccion_postal: str):
        super().__init__(id, nombre, email)
        self.direccion_postal = direccion_postal

    def __str__(self) -> str:
        return f"Cliente: {super().__str__()} - {self.direccion_postal}"


class Administrador(Usuario):
    """Administrador de la tienda."""

    def es_admin(self) -> bool:
        return True

    def __str__(self) -> str:
        return f"Administrador: {super().__str__()}"
