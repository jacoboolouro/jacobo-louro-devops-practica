import pytest

from src.calculos import calcular


def test_operaciones():
    assert calcular("suma", 2, 3) == 5
    assert calcular("resta", 2, 3) == -1
    assert calcular("multiplicacion", 2, 3) == 6
    assert calcular("division", 6, 3) == 2
    assert calcular("potencia", 2, 3) == 8


def test_division_entre_cero():
    with pytest.raises(ZeroDivisionError):
        calcular("division", 1, 0)


def test_operacion_no_valida():
    with pytest.raises(ValueError):
        calcular("raiz", 1, 1)
