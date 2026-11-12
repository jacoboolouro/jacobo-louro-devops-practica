from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


# ------------------------------------------------------------------ Usuarios

class UsuarioCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str = Field(min_length=1)
    email: EmailStr
    tipo: Literal["cliente", "administrador"]
    direccion_postal: Optional[str] = None

    @model_validator(mode="after")
    def validar_direccion(self):
        if self.tipo == "cliente" and not self.direccion_postal:
            raise ValueError("Un cliente debe tener dirección postal")
        return self


class UsuarioRead(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    es_admin: bool


# ----------------------------------------------------------------- Productos

class ProductoCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "examples": [
                {"tipo": "electronico", "nombre": "Auriculares", "precio": 59.99, "stock": 10, "meses_garantia": 24}
            ]
        },
    )

    tipo: Literal["generico", "electronico", "ropa"]
    nombre: str = Field(min_length=1)
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    meses_garantia: Optional[int] = Field(default=None, ge=0)
    talla: Optional[str] = Field(default=None, min_length=1)
    color: Optional[str] = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validar_atributos_por_tipo(self):
        if self.tipo == "electronico":
            if self.meses_garantia is None:
                raise ValueError("Un producto electrónico debe indicar meses_garantia")
            if self.talla is not None or self.color is not None:
                raise ValueError("Un producto electrónico no tiene talla ni color")
        elif self.tipo == "ropa":
            if self.talla is None or self.color is None:
                raise ValueError("Un producto de ropa debe indicar talla y color")
            if self.meses_garantia is not None:
                raise ValueError("Un producto de ropa no tiene meses_garantia")
        else:  # generico
            if self.meses_garantia is not None or self.talla is not None or self.color is not None:
                raise ValueError("Un producto genérico no tiene meses_garantia, talla ni color")
        return self


class ProductoRead(BaseModel):
    id: int
    tipo: str
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None


# ------------------------------------------------------------------- Pedidos

class PedidoItemCreate(BaseModel):
    producto_id: int
    cantidad: int = Field(gt=0)


class PedidoCreate(BaseModel):
    cliente_id: int
    items: list[PedidoItemCreate] = Field(min_length=1)


class PedidoItemRead(BaseModel):
    producto_id: int
    nombre: str
    precio_unitario: float
    cantidad: int
    subtotal: float


class PedidoRead(BaseModel):
    id: int
    fecha: datetime
    cliente_id: int
    total: float
    items: list[PedidoItemRead]
