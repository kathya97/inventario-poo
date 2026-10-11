"""Agrupación de productos: la clase Inventario."""

import logging

logger = logging.getLogger(__name__)


class Inventario:
    """Mantiene una colección de productos y opera sobre ella.

    AGRUPACIÓN DE CLASES: un Inventario contiene muchos productos (por
    ejemplo, una Biblioteca que contiene varios Libro).
    """

    def __init__(self, nombre):
        self.nombre = nombre
        self._productos = []

    def agregar(self, *productos):
        """Agrega uno o varios productos (sobrecarga simulada con *args)."""
        for producto in productos:
            if producto in self._productos:  # usa __eq__: compara por código
                raise ValueError(f"El producto {producto.codigo} ya existe")
            self._productos.append(producto)
        logger.info("%s: se agregaron %s productos", self.nombre, len(productos))

    def buscar(self, codigo):
        """Devuelve el producto con ese código, o None si no existe."""
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None

    def valor_total(self):
        """Valor de todo el inventario."""
        return sum(producto.valor_total() for producto in self._productos)

    def a_reabastecer(self, minimo=10):
        """Lista los productos cuyo stock está por debajo del mínimo."""
        return [p for p in self._productos if p.necesita_reabastecer(minimo)]

    def __len__(self):
        return len(self._productos)

    def __iter__(self):
        return iter(self._productos)
