"""Clases de producto: ProductoInventario y su subclase ProductoPerecedero."""

import logging
from datetime import date

from articulo import Articulo
from ubicacion import Ubicacion

logger = logging.getLogger(__name__)


class ProductoInventario(Articulo):
    """Producto almacenado en la bodega de una empresa.

    PILAR - HERENCIA: hereda de Articulo (clase abstracta) y agrega precio,
    stock, categoría y ubicación física dentro de la bodega.
    """

    TASA_IVA = 0.13  # constante de clase: evita repetir el "número mágico" 0.13

    def __init__(
        self,
        codigo,
        nombre,
        precio_unitario,
        stock,
        categoria,
        bodega="Central",
        pasillo="A",
        estante=1,
    ):
        """Crea un producto.

        Args:
            codigo (str): código único, por ejemplo "P-001".
            nombre (str): nombre comercial.
            precio_unitario (float): precio por unidad, sin IVA.
            stock (int): unidades disponibles (no negativo).
            categoria (str): familia a la que pertenece el producto.
            bodega, pasillo, estante: ubicación en la bodega. Tienen valores
                por defecto, lo que simula la sobrecarga del constructor.

        Raises:
            ValueError: si el precio o el stock son negativos.
        """
        super().__init__(codigo, nombre)
        if precio_unitario < 0 or stock < 0:
            raise ValueError("El precio y el stock no pueden ser negativos")
        self.categoria = categoria  # variable primitiva (str)
        self._precio_unitario = precio_unitario  # primitiva (float), protegida
        self.__stock = stock  # primitiva (int), privada
        # Variable de tipo clase y COMPOSICIÓN: el producto crea y posee su
        # Ubicacion; si el producto desaparece, su ubicación también.
        self.ubicacion = Ubicacion(bodega, pasillo, estante)
        logger.info("Producto %s creado", codigo)

    @property
    def stock(self):
        """Unidades disponibles (solo lectura; cambia con vender/ingresar)."""
        return self.__stock

    @property
    def precio_unitario(self):
        """Precio por unidad sin IVA (solo lectura)."""
        return self._precio_unitario

    # PILAR - ABSTRACCIÓN: implementa el método abstracto de Articulo.
    def descripcion(self):
        return (
            f"{self.codigo} - {self.nombre} ({self.categoria}) | "
            f"stock: {self.__stock} | ubicación: {self.ubicacion}"
        )

    def ingresar_stock(self, *cantidades):
        """Suma una o varias entradas de mercadería.

        SOBRECARGA SIMULADA con *args: se puede llamar con una cantidad,
        ingresar_stock(5), o con varias, ingresar_stock(5, 10, 3). Python no
        permite dos métodos con el mismo nombre; *args recibe todas las
        cantidades en una tupla y el método decide qué hacer.
        """
        if not cantidades:
            raise ValueError("Indique al menos una cantidad")
        if any(cantidad <= 0 for cantidad in cantidades):
            raise ValueError("Las cantidades deben ser positivas")
        self.__stock += sum(cantidades)
        logger.info("%s: ingresaron %s unidades", self.codigo, sum(cantidades))

    def vender(self, cantidad):
        """Descuenta unidades vendidas; falla si no hay suficiente stock."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        if cantidad > self.__stock:
            raise ValueError(f"Stock insuficiente de {self.nombre}")
        self.__stock -= cantidad

    def valor_total(self):
        """Valor del inventario de este producto (stock por precio)."""
        return self.__stock * self._precio_unitario

    def necesita_reabastecer(self, minimo=10):
        """Indica si el stock cayó por debajo del mínimo (por defecto, 10)."""
        return self.__stock < minimo

    def aplicar_descuento(self, porcentaje=10):
        """Reduce el precio unitario en un porcentaje (por defecto, 10 %).

        SOBRECARGA SIMULADA con argumento por defecto: aplicar_descuento()
        y aplicar_descuento(20) son dos formas de llamar al mismo método.
        """
        if not 0 <= porcentaje <= 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        self._precio_unitario = round(self._precio_unitario * (1 - porcentaje / 100), 2)

    @classmethod
    def desde_cadena(cls, texto):
        """Crea un producto desde 'codigo;nombre;precio;stock;categoria'."""
        codigo, nombre, precio, stock, categoria = [
            campo.strip() for campo in texto.split(";")
        ]
        return cls(codigo, nombre, float(precio), int(stock), categoria)

    @staticmethod
    def precio_con_iva(precio, tasa=TASA_IVA):
        """Calcula el precio con IVA. No depende de ningún producto en particular."""
        return round(precio * (1 + tasa), 2)


class ProductoPerecedero(ProductoInventario):
    """Producto con fecha de vencimiento (leche, yogur, medicinas...).

    PILAR - HERENCIA: reutiliza todo lo de ProductoInventario y agrega la
    fecha de vencimiento. PILAR - POLIMORFISMO: sobrescribe vender() y
    descripcion(), así que la misma llamada se comporta distinto que en la
    clase padre.
    """

    def __init__(
        self,
        codigo,
        nombre,
        precio_unitario,
        stock,
        categoria,
        fecha_vencimiento,
        **opciones,
    ):
        """Crea un producto perecedero.

        Args:
            fecha_vencimiento (date): fecha límite para vender el producto.
            **opciones: datos de ubicación opcionales (bodega, pasillo,
                estante) que se pasan tal cual al constructor del padre.
        """
        super().__init__(codigo, nombre, precio_unitario, stock, categoria, **opciones)
        self.fecha_vencimiento = fecha_vencimiento

    def dias_para_vencer(self, hoy=None):
        """Días que faltan para el vencimiento (negativo si ya venció)."""
        hoy = hoy or date.today()
        return (self.fecha_vencimiento - hoy).days

    def vender(self, cantidad):
        """Sobrescribe vender(): no permite vender mercadería vencida."""
        if self.dias_para_vencer() < 0:
            raise ValueError(f"{self.nombre} está vencido y no se puede vender")
        super().vender(cantidad)

    def descripcion(self):
        """Sobrescribe descripcion(): agrega la fecha de vencimiento."""
        return f"{super().descripcion()} | vence: {self.fecha_vencimiento.isoformat()}"
