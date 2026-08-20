# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import create_db_and_tables

# IMPORTANTE: Importar TODOS los modelos antes de create_db_and_tables()
# para que SQLAlchemy registre todas las tablas y pueda resolver
# las claves foráneas (FK) correctamente al momento de insertar datos.
from app.models.user import User  # noqa: F401
from app.models.category import Category  # noqa: F401
from app.models.product import Product  # noqa: F401
from app.models.review import Review  # noqa: F401
from app.models.cart_item import CartItem  # noqa: F401
from app.models.task import Task  # noqa: F401

# Lifespan: Lo que se ejecuta exactamente al encender o apagar el servidor web
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando la Base de Datos Agóstica...")
    create_db_and_tables()
    yield
    print("Apagando API de forma segura...")

# Instancia central de la Aplicación
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Proyecto Base del Taller de la Taller de Actualización",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Configuración Anti-CORS (Muy pedido en la clase teórica del Día 4)
app.add_middleware(
    CORSMiddleware,
    # Durante desarrollo acepta de cualquier Frontend Angular local
    allow_origins=["http://localhost:4200", "http://localhost:8080", "https://cody-apps-internet-frontend-ng-rho.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint Salud inicial
@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Bienvenido al Taller 🎓. Añade /docs a la URL para ver la magia de FastAPI."
    }

# IMPORTANTE: Aquí conectamos el router global con todas nuestras carpetas /api
from app.api.main_router import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)
