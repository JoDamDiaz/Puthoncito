from fastapi import FastAPI
from app.database import Base, engine
from app.routes.dog_routes import router as dog_router
from app.routes.cat_routes import router as cat_router
import app.models.dog  # noqa: F401
import app.models.cat  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Registro de Mascotas",
    description="CRUD de perros y gatos con FastAPI + MySQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(dog_router)
app.include_router(cat_router)
