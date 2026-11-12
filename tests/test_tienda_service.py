import pytest

from Services import TiendaService


@pytest.fixture
def tienda():
    servicio = TiendaService()
    servicio.registrar_usuario("Laura", "laura@correo.com", "cliente", "Calle Real 10")
    servicio.crear_producto("electronico", "Auriculares", 59.99, 10, meses_garantia=24)
    servicio.crear_producto("ropa", "Camiseta", 15.0, 30, talla="M", color="Azul")
    return servicio


def test_email_repetido(tienda):
    with pytest.raises(ValueError):
        tienda.registrar_usuario("Otra", "LAURA@correo.com", "cliente", "Otra calle")


def test_pedido_calcula_total_y_reduce_stock(tienda):
    pedido = tienda.crear_pedido(1, [(1, 1), (2, 2)])
    assert pedido.calcular_total() == 89.99
    assert tienda.obtener_producto(1).stock == 9
    assert tienda.obtener_producto(2).stock == 28


def test_pedido_sin_stock_no_modifica_nada(tienda):
    with pytest.raises(ValueError):
        tienda.crear_pedido(1, [(2, 1), (1, 11)])
    assert tienda.obtener_producto(2).stock == 30


def test_pedido_de_cliente_inexistente(tienda):
    with pytest.raises(LookupError):
        tienda.crear_pedido(99, [(1, 1)])
