from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.database import Base, engine
from app.routes.dog_routes import router as dog_router
from app.routes.cat_routes import router as cat_router
from app.routes.auth_routes import router as auth_router
import app.models.dog   # noqa: F401
import app.models.cat   # noqa: F401
import app.models.user  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Registro de Mascotas",
    description="""
## Descripción
API REST para el registro y gestión de mascotas (perros y gatos) con recomendaciones de cuidado personalizadas generadas por IA.

## Tecnologías
- **FastAPI** — framework web
- **MySQL + SQLAlchemy** — persistencia de datos
- **Claude (Anthropic)** — recomendaciones veterinarias con IA

## Recursos

### 🐶 Perros `/dogs`
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/dogs/` | Listar todos los perros |
| GET | `/dogs/{id}` | Obtener un perro por ID |
| POST | `/dogs/` | Registrar un nuevo perro |
| PUT | `/dogs/{id}` | Actualizar datos de un perro |
| DELETE | `/dogs/{id}` | Eliminar un perro |
| GET | `/dogs/breeds/count` | Conteo de perros por raza |
| GET | `/dogs/{id}/recommendations` | Recomendaciones de cuidado por IA |

### 🐱 Gatos `/cats`
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/cats/` | Listar todos los gatos |
| GET | `/cats/{id}` | Obtener un gato por ID |
| POST | `/cats/` | Registrar un nuevo gato |
| PUT | `/cats/{id}` | Actualizar datos de un gato |
| DELETE | `/cats/{id}` | Eliminar un gato |
| GET | `/cats/breeds/count` | Conteo de gatos por raza |
| GET | `/cats/{id}/recommendations` | Recomendaciones de cuidado por IA |
""",
    version="1.2.0",
    contact={
        "name": "Daniel Miranda",
        "email": "daniel.miranda.diaz@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(auth_router)
app.include_router(dog_router)
app.include_router(cat_router)
