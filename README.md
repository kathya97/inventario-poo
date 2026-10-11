# Inventario POO

Proyecto de la materia Programación Orientada a Objetos (CETEC). Modela un
inventario de bodega aplicando los cuatro pilares de la POO.

## Estructura

| Archivo | Contenido |
|---|---|
| `articulo.py` | Clase abstracta `Articulo` (abstracción y encapsulamiento) |
| `ubicacion.py` | Clase `Ubicacion` (usada por composición) |
| `producto.py` | `ProductoInventario` y su subclase `ProductoPerecedero` (herencia y polimorfismo) |
| `inventario.py` | Clase `Inventario`, que agrupa productos |
| `main.py` | Script de demostración |
| `test_producto.py` | Pruebas con pytest |

## Cómo ejecutarlo

```
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
python main.py
pytest
```

## Herramientas

- **black**: formateo del código
- **flake8**: revisión de estilo (linter)
- **pytest**: pruebas automáticas
