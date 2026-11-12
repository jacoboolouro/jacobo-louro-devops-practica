"""Lógica de cálculo de la calculadora."""

OPERACIONES = ("suma", "resta", "multiplicacion", "division", "potencia")


def calcular(operacion: str, a: float, b: float) -> float:
    """Aplica la operación indicada a los operandos a y b."""
    if operacion == "suma":
        return a + b
    if operacion == "resta":
        return a - b
    if operacion == "multiplicacion":
        return a * b
    if operacion == "division":
        if b == 0:
            raise ZeroDivisionError("No se puede dividir entre cero")
        return a / b
    if operacion == "potencia":
        return a ** b
    raise ValueError(
        f"Operación '{operacion}' no soportada. Usa una de: {', '.join(OPERACIONES)}"
    )
