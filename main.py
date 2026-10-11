"""Demostración del proyecto de inventario."""

import logging
from datetime import date, timedelta

from inventario import Inventario
from producto import ProductoInventario, ProductoPerecedero

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main():
    hoy = date.today()
    teclado = ProductoInventario(
        "P-001", "Teclado mecánico", 45.50, 30, "Periféricos", pasillo="B", estante=2
    )
    leche = ProductoPerecedero(
        "P-100", "Leche entera 1L", 1.25, 60, "Lácteos", hoy + timedelta(days=5)
    )
    yogur = ProductoPerecedero(
        "P-101", "Yogur natural", 0.90, 8, "Lácteos", hoy - timedelta(days=2)
    )

    inventario = Inventario("Bodega Central")
    inventario.agregar(teclado, leche, yogur)  # *args: varios productos a la vez

    print("\n--- Polimorfismo: misma llamada, distinto resultado ---")
    for producto in inventario:
        print(producto.descripcion())

    print("\n--- Venta de 2 unidades de cada producto ---")
    for producto in inventario:
        try:
            producto.vender(2)
            print(f"Venta correcta: {producto.nombre} (stock: {producto.stock})")
        except ValueError as error:
            print(f"No se pudo vender: {error}")

    print("\n--- Sobrecarga simulada (argumentos por defecto y *args) ---")
    teclado.ingresar_stock(5)
    teclado.ingresar_stock(5, 10, 3)
    teclado.aplicar_descuento()
    print("Precio con descuento por defecto (10 %):", teclado.precio_unitario)
    teclado.aplicar_descuento(20)
    print("Precio tras un descuento adicional de 20 %:", teclado.precio_unitario)

    print("\n--- Agrupación y composición ---")
    print("Productos en el inventario:", len(inventario))
    print("Valor total: $", round(inventario.valor_total(), 2))
    print("A reabastecer:", [p.nombre for p in inventario.a_reabastecer()])
    print("Ubicación del teclado:", teclado.ubicacion)
    print("Precio del teclado con IVA:", ProductoInventario.precio_con_iva(45.50))


if __name__ == "__main__":
    main()
