"""Ubicación física de un producto dentro de la bodega."""


class Ubicacion:
    """Indica dónde está guardado un producto: bodega, pasillo y estante."""

    def __init__(self, bodega, pasillo, estante):
        self.bodega = bodega
        self.pasillo = pasillo
        self.estante = estante

    def __str__(self):
        return f"{self.bodega}-{self.pasillo}{self.estante}"
