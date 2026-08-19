# pyrefly: ignore [missing-import]
"""
Script de Seed: Carga categorías y productos de ejemplo en la base de datos.

Elimina los datos existentes de categorías/productos (y sus dependencias)
y los recarga limpio. Uso:

    .venv/bin/python scripts/seed.py
"""
from sqlmodel import Session, select, delete
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import create_db_and_tables, engine
from app.models.category import Category
from app.models.product import Product
from app.models.cart_item import CartItem
from app.models.review import Review

CATEGORIES = [
    {"title": "Bebidas", "description": "Gaseosas, jugos y agua"},
    {"title": "Snacks", "description": "Papas, galletas y botanas"},
    {"title": "Lácteos", "description": "Leche, yogures y quesos"},
    {"title": "Panadería", "description": "Pan fresco y facturas"},
    {"title": "Limpieza", "description": "Productos de limpieza para el hogar"},
]

PRODUCTS = [
    # Bebidas (1)
    {"title": "Coca Cola 1.5L", "description": "Gaseosa cola 1.5 litros", "price": 3200, "stock": 45, "category_id": 1},
    {"title": "Agua Mineral 2L", "description": "Agua mineral sin gas", "price": 1800, "stock": 60, "category_id": 1},
    {"title": "Jugo de Naranja 1L", "description": "Jugo de naranja natural", "price": 2500, "stock": 30, "category_id": 1},
    {"title": "Cerveza Rubia 6pk", "description": "Pack de 6 cervezas rubias", "price": 9500, "stock": 25, "category_id": 1},
    # Snacks (2)
    {"title": "Papas Fritas Clásicas", "description": "Papas fritas saladas 120g", "price": 1500, "stock": 80, "category_id": 2},
    {"title": "Chocolates surtidos", "description": "Caja de bombones surtidos", "price": 4800, "stock": 20, "category_id": 2},
    {"title": "Galletas de Avena", "description": "Galletas integrales con avena", "price": 2200, "stock": 55, "category_id": 2},
    {"title": "Maní salado", "description": "Maní tostado y salado 250g", "price": 1900, "stock": 70, "category_id": 2},
    # Lácteos (3)
    {"title": "Leche Entera 1L", "description": "Leche entera pasteurizada", "price": 2100, "stock": 50, "category_id": 3},
    {"title": "Yogur Frutilla 1kg", "description": "Yogur sabor frutilla", "price": 2800, "stock": 35, "category_id": 3},
    {"title": "Queso Crema 250g", "description": "Queso crema untable", "price": 3400, "stock": 28, "category_id": 3},
    {"title": "Manteca 200g", "description": "Manteca común 200 gramos", "price": 2600, "stock": 40, "category_id": 3},
    # Panadería (4)
    {"title": "Pan de Molde", "description": "Pan de molde blanco 700g", "price": 2900, "stock": 32, "category_id": 4},
    {"title": "Facturas docena", "description": "Docena de facturas surtidas", "price": 5200, "stock": 15, "category_id": 4},
    {"title": "Pan Negro Integral", "description": "Pan integral de centeno", "price": 3300, "stock": 22, "category_id": 4},
    {"title": "Bizcochos de grasa", "description": "Bizcochos salados x200g", "price": 1700, "stock": 48, "category_id": 4},
    # Limpieza (5)
    {"title": "Detergente 750ml", "description": "Detergente lavavajillas", "price": 3100, "stock": 38, "category_id": 5},
    {"title": "Lavandina 1L", "description": "Lavandina concentrada", "price": 1400, "stock": 65, "category_id": 5},
    {"title": "Esponja de cocina", "description": "Pack de 3 esponjas", "price": 900, "stock": 90, "category_id": 5},
    {"title": "Jabón en polvo 800g", "description": "Jabón en polvo para ropa", "price": 5600, "stock": 26, "category_id": 5},
]


def seed():
    create_db_and_tables()
    with Session(engine) as session:
        # Limpiar en orden por dependencias (reviews -> cart -> products -> categories)
        session.exec(delete(Review))
        session.exec(delete(CartItem))
        session.exec(delete(Product))
        session.exec(delete(Category))
        session.commit()

        for cat in CATEGORIES:
            session.add(Category(**cat))
        session.commit()

        for prod in PRODUCTS:
            session.add(Product(**prod))
        session.commit()

    with Session(engine) as session:
        cats = list(session.exec(select(Category)).all())
        prods = list(session.exec(select(Product)).all())
        total_stock = sum(p.stock for p in prods)
        print("\nSeed completado:")
        print(f"  Categorías: {len(cats)}")
        print(f"  Productos: {len(prods)}")
        print(f"  Stock total: {total_stock} unidades")
        print("\nProductos:")
        for p in prods:
            print(f"   [{p.id}] {p.title} - ${p.price} - stock {p.stock} (cat {p.category_id})")


if __name__ == "__main__":
    seed()