"""Pruebas del proyecto de inventario (se ejecutan con: pytest)."""

from datetime import date, timedelta

import pytest

from articulo import Articulo
from inventario import Inventario
from producto import ProductoInventario, ProductoPerecedero


def crear_producto(codigo="P-001", stock=10):
    return ProductoInventario(codigo, "Teclado", 45.50, stock, "Periféricos")


def test_articulo_abstracto_no_se_instancia():
    with pytest.raises(TypeError):
        Articulo("X-1", "Algo")


def test_igualdad_por_codigo():
    assert crear_producto("P-001") == crear_producto("P-001")
    assert crear_producto("P-001") != crear_producto("P-002")


def test_vender_descuenta_stock():
    producto = crear_producto(stock=10)
    producto.vender(4)
    assert producto.stock == 6


def test_vender_mas_del_stock_falla():
    with pytest.raises(ValueError):
        crear_producto(stock=3).vender(5)


def test_perecedero_vencido_no_se_vende():
    vencido = ProductoPerecedero(
        "P-101", "Yogur", 0.90, 8, "Lácteos", date.today() - timedelta(days=1)
    )
    with pytest.raises(ValueError):
        vencido.vender(1)


def test_inventario_rechaza_duplicados():
    inventario = Inventario("Prueba")
    inventario.agregar(crear_producto("P-001"))
    with pytest.raises(ValueError):
        inventario.agregar(crear_producto("P-001"))
