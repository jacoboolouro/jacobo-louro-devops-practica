"""Cliente de la API REST de la tienda online.

No importa nada del servidor: toda la comunicación se hace por HTTP con requests.
Para usar la API de otro equipo, cambiar BASE_URL por su IP, p. ej. "http://192.168.1.34:8000".
"""

import sys
import time

import requests

BASE_URL = "http://localhost:8000"


def comprobar(respuesta: requests.Response, codigo_esperado: int):
    """Comprueba el código HTTP y devuelve el JSON de la respuesta."""
    print(f"  -> {respuesta.request.method} {respuesta.url} : {respuesta.status_code}")
    datos = respuesta.json()
    if respuesta.status_code != codigo_esperado:
        print(f"  Error (se esperaba {codigo_esperado}): {datos.get('detail', datos)}")
        sys.exit(1)
    return datos


def crear_usuario(nombre: str, email: str, tipo: str, direccion_postal: str | None = None) -> dict:
    datos = {"nombre": nombre, "email": email, "tipo": tipo, "direccion_postal": direccion_postal}
    return comprobar(requests.post(f"{BASE_URL}/usuarios", json=datos), 201)


def listar_usuarios() -> list:
    return comprobar(requests.get(f"{BASE_URL}/usuarios"), 200)


def crear_producto(datos: dict) -> dict:
    return comprobar(requests.post(f"{BASE_URL}/productos", json=datos), 201)


def listar_productos() -> list:
    return comprobar(requests.get(f"{BASE_URL}/productos"), 200)


def crear_pedido(cliente_id: int, items: list[dict]) -> dict:
    datos = {"cliente_id": cliente_id, "items": items}
    return comprobar(requests.post(f"{BASE_URL}/pedidos", json=datos), 201)


def listar_pedidos_usuario(cliente_id: int) -> list:
    return comprobar(requests.get(f"{BASE_URL}/usuarios/{cliente_id}/pedidos"), 200)


def main():
    print(f"API: {BASE_URL}\n")

    print("1. Crear un usuario")
    # Email distinto en cada ejecución para que no choque con uno ya registrado.
    email = f"laura.{int(time.time())}@correo.com"
    usuario = crear_usuario("Laura Gómez", email, "cliente", "Calle Real 10, A Coruña")
    print(f"  Usuario creado: id={usuario['id']} {usuario['nombre']} <{usuario['email']}>\n")

    print("2. Consultar la lista de usuarios")
    for u in listar_usuarios():
        rol = "admin" if u["es_admin"] else "cliente"
        print(f"  [{u['id']}] {u['nombre']} <{u['email']}> ({rol})")
    print()

    print("3. Crear varios productos")
    nuevos = [
        {"tipo": "generico", "nombre": "Taza", "precio": 7.5, "stock": 50},
        {"tipo": "electronico", "nombre": "Auriculares", "precio": 59.99, "stock": 10, "meses_garantia": 24},
        {"tipo": "ropa", "nombre": "Camiseta", "precio": 15.0, "stock": 30, "talla": "M", "color": "Azul"},
    ]
    productos_creados = [crear_producto(p) for p in nuevos]
    for p in productos_creados:
        print(f"  Producto creado: id={p['id']} {p['nombre']} ({p['tipo']})")
    print()

    print("4. Consultar la lista de productos")
    for p in listar_productos():
        print(f"  [{p['id']}] {p['nombre']} - {p['precio']:.2f} € - stock {p['stock']} ({p['tipo']})")
    print()

    print("5. Crear un pedido para el usuario")
    items = [
        {"producto_id": productos_creados[1]["id"], "cantidad": 1},
        {"producto_id": productos_creados[2]["id"], "cantidad": 2},
    ]
    pedido = crear_pedido(usuario["id"], items)
    print(f"  Pedido creado: id={pedido['id']} total={pedido['total']:.2f} €\n")

    print("6. Consultar los pedidos del usuario")
    for p in listar_pedidos_usuario(usuario["id"]):
        print(f"  Pedido {p['id']} ({p['fecha']}) - Total: {p['total']:.2f} €")
        for item in p["items"]:
            print(f"    {item['cantidad']} x {item['nombre']} = {item['subtotal']:.2f} €")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print(f"No se pudo conectar con la API en {BASE_URL}")
        sys.exit(1)
