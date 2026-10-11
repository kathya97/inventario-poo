"""Clase abstracta base de todos los artículos de la bodega."""

from abc import ABC, abstractmethod


class Articulo(ABC):
    """Define lo que todo artículo de la bodega debe tener y saber hacer.

    PILAR - ABSTRACCIÓN: la clase expone solo lo esencial (código, nombre y
    descripción) y obliga a las clases hijas a implementar descripcion().
    No se puede instanciar directamente.
    """

    def __init__(self, codigo, nombre):
        # PILAR - ENCAPSULAMIENTO: el código es la identidad del artículo;
        # es privado y solo se puede leer mediante una propiedad.
        self.__codigo = codigo
        self.nombre = nombre

    @property
    def codigo(self):
        """Código único del artículo (solo lectura)."""
        return self.__codigo

    @abstractmethod
    def descripcion(self):
        """Devuelve un texto que describe el artículo. Cada hijo lo implementa."""

    def __eq__(self, otro):
        """Dos artículos son iguales si tienen el mismo código."""
        if not isinstance(otro, Articulo):
            return NotImplemented
        return self.codigo == otro.codigo

    def __hash__(self):
        """Coherente con __eq__: mismo código, mismo hash."""
        return hash(self.codigo)
