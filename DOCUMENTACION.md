# Documentación: API Registro de Mascotas

API REST para el registro y gestión de perros y gatos con recomendaciones de cuidado personalizadas generadas por IA (Claude de Anthropic), desplegada en Railway.

---

## Tabla de contenidos

1. [Stack tecnológico](#1-stack-tecnológico)
2. [Arquitectura del sistema](#2-arquitectura-del-sistema)
3. [Estructura del proyecto](#3-estructura-del-proyecto)
4. [Desarrollo local](#4-desarrollo-local)
5. [Endpoints de la API](#5-endpoints-de-la-api)
6. [Integración con Anthropic Claude](#6-integración-con-anthropic-claude)
7. [Docker y contenedores](#7-docker-y-contenedores)
8. [Despliegue en Railway](#8-despliegue-en-railway)
9. [Variables de entorno](#9-variables-de-entorno)
10. [URLs de producción](#10-urls-de-producción)

---

## 1. Stack tecnológico

| Capa | Tecnología | Versión |
|---|---|---|
| API | FastAPI | 0.128.8 |
| Servidor ASGI | Uvicorn | 0.39.0 |
| ORM | SQLAlchemy | 2.0.50 |
| Base de datos | MySQL | 8.0 |
| Driver MySQL | PyMySQL | 1.2.0 |
| Validación | Pydantic | 2.13.4 |
| IA | Anthropic Claude | claude-sonnet-4-6 |
| SDK IA | anthropic | 0.105.0 |
| Frontend | Flask | 3.1.0 |
| Contenedores | Docker + Docker Compose | — |
| Plataforma | Railway | — |
| Lenguaje | Python | 3.9 |

---

## 2. Arquitectura del sistema

### Patrón por capas (Layered Architecture)

```
HTTP Request
     │
     ▼
┌─────────────┐
│   Routes    │  Recibe la petición HTTP, valida parámetros de ruta
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Services   │  Lógica de negocio, manejo de errores HTTP (404, etc.)
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│  Repositories    │  Acceso a datos, consultas SQLAlchemy
└──────┬───────────┘
       │
       ▼
┌─────────────┐
│   Models    │  Definición de tablas (SQLAlchemy ORM)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    MySQL    │  Base de datos relacional
└─────────────┘
```

### Arquitectura de servicios en Railway

```
Internet
    │
    ├──► frontapi (Flask)  ──► API interna ──► Puthoncito (FastAPI)
    │                                               │
    └──► Puthoncito (FastAPI) ─────────────────► MySQL
                                    │
                                    └──► Anthropic Claude API
```

### Flujo de recomendaciones IA

```
GET /dogs/{id}/recommendations
        │
        ▼
  DogService.get_by_id()        ← valida que el perro existe
        │
        ▼
  RecommendationService
  ._build_prompt(dog)           ← construye prompt compacto (~25 tokens)
        │
        ▼
  AnthropicService.complete()   ← llama a claude-sonnet-4-6
        │                          system prompt cacheado (~12 tokens)
        ▼
  { dog_id, dog_name, breed, recommendations }
```

---

## 3. Estructura del proyecto

```
Puthoncito/
├── main.py                          # Punto de entrada FastAPI
├── seed.py                          # Script de datos de ejemplo
├── requirements.txt                 # Dependencias Python
├── Dockerfile                       # Imagen de la app
├── Dockerfile.mysql                 # Imagen MySQL con schema
├── docker-compose.yml               # Orquestación local y Railway
├── railway.toml                     # Configuración Railway
├── .env                             # Variables locales (no commitear)
├── .gitignore                       # Excluye .env, venv, cache
├── .dockerignore                    # Excluye venv, .env, seed, etc.
│
├── docker/
│   └── init.sql                     # Schema: tablas dogs y cats
│
└── app/
    ├── database.py                  # Engine SQLAlchemy + get_db()
    ├── models/
    │   ├── dog.py                   # Modelo Dog (SQLAlchemy)
    │   └── cat.py                   # Modelo Cat (SQLAlchemy)
    ├── schemas/
    │   ├── dog.py                   # Schemas Pydantic Dog
    │   └── cat.py                   # Schemas Pydantic Cat
    ├── repositories/
    │   ├── dog_repository.py        # CRUD + conteo por raza (Dog)
    │   └── cat_repository.py        # CRUD + conteo por raza (Cat)
    ├── services/
    │   ├── dog_service.py           # Lógica de negocio Dog
    │   ├── cat_service.py           # Lógica de negocio Cat
    │   ├── anthropic_service.py     # Wrapper SDK Anthropic
    │   ├── recommendation_service.py        # Recomendaciones Dog
    │   └── cat_recommendation_service.py    # Recomendaciones Cat
    └── routes/
        ├── dog_routes.py            # Router /dogs
        └── cat_routes.py            # Router /cats
```

---

## 4. Desarrollo local

### Prerrequisitos

- Python 3.9+
- Docker Desktop
- Git

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/JoDamDiaz/Puthoncito.git
cd Puthoncito
```

### Paso 2 — Entorno virtual

```bash
python3 -m venv apivenv
source apivenv/bin/activate
```

### Paso 3 — Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4 — Variables de entorno

Crea el archivo `.env` en la raíz del proyecto:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=secret
DB_NAME=perritos

ANTHROPIC_API_KEY=sk-ant-...
```

### Paso 5 — Levantar base de datos con Docker

```bash
docker compose up db -d
```

Esto construye la imagen MySQL con el schema de `docker/init.sql` y levanta el contenedor con volumen persistente.

Verificar que la base de datos está lista:

```bash
docker compose ps
```

### Paso 6 — Ejecutar la API

```bash
uvicorn main:app --reload
```

La API queda disponible en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Paso 7 — Insertar datos de ejemplo

```bash
python seed.py
```

Inserta 12 perros y 12 gatos con datos de ejemplo para pruebas.

### Paso 8 — Levantar todo con Docker Compose

Para levantar la app y la base de datos juntas:

```bash
docker compose up --build
```

Servicios disponibles:
- API: `http://localhost:8000`
- MySQL: `localhost:3306`

### Paso 9 — Frontend local (opcional)

```bash
cd /ruta/a/frontapi
python3 -m venv frontvenv
source frontvenv/bin/activate
pip install -r requirements.txt
python app.py
```

Frontend en `http://localhost:5000`.

---

## 5. Endpoints de la API

### Perros — `/dogs`

| Método | Ruta | Descripción | Código |
|---|---|---|---|
| GET | `/dogs/` | Listar todos los perros | 200 |
| GET | `/dogs/{id}` | Obtener perro por ID | 200 / 404 |
| POST | `/dogs/` | Crear nuevo perro | 201 |
| PUT | `/dogs/{id}` | Actualizar perro | 200 / 404 |
| DELETE | `/dogs/{id}` | Eliminar perro | 204 / 404 |
| GET | `/dogs/breeds/count` | Conteo por raza (desc.) | 200 |
| GET | `/dogs/{id}/recommendations` | Recomendaciones IA | 200 / 404 |

### Gatos — `/cats`

| Método | Ruta | Descripción | Código |
|---|---|---|---|
| GET | `/cats/` | Listar todos los gatos | 200 |
| GET | `/cats/{id}` | Obtener gato por ID | 200 / 404 |
| POST | `/cats/` | Crear nuevo gato | 201 |
| PUT | `/cats/{id}` | Actualizar gato | 200 / 404 |
| DELETE | `/cats/{id}` | Eliminar gato | 204 / 404 |
| GET | `/cats/breeds/count` | Conteo por raza (desc.) | 200 |
| GET | `/cats/{id}/recommendations` | Recomendaciones IA | 200 / 404 |

### Esquema del modelo (Dog / Cat)

```json
{
  "id": 1,
  "name": "Max",
  "breed": "Labrador Retriever",
  "age": 3.0,
  "weight": 30.0,
  "sex": "macho",
  "owner": "Carlos Pérez"
}
```

Campos requeridos en POST: `name`, `breed`, `age` (>0), `weight` (>0), `sex` (`macho`|`hembra`), `owner`.  
En PUT todos los campos son opcionales (PATCH semántico).

---

## 6. Integración con Anthropic Claude

### Configuración del servicio

**`app/services/anthropic_service.py`**

- Modelo: `claude-sonnet-4-6`
- System prompt cacheado con `cache_control: ephemeral` (reduce costos en llamadas repetidas)
- `max_tokens`: 512 (optimizado para respuestas concisas)

### Optimización de tokens

| Elemento | Antes | Después | Ahorro |
|---|---|---|---|
| System prompt | ~55 tokens | ~12 tokens | 43 tokens |
| Prompt de usuario | ~110 tokens | ~25 tokens | 85 tokens |
| `max_tokens` output | 1024 | 512 | hasta 512 tokens |
| **Total por llamada** | ~1189 tokens | **~549 tokens** | **~640 tokens** |

### Prompt optimizado (perro)

```
Perro: {breed}, {age}a, {weight}kg, {sex}
Recomienda brevemente: 1.Alimentación 2.Ejercicio 3.Salud preventiva 4.Aseo 5.Raza
```

### Reglas del sistema

- No interactúa con el usuario ni hace preguntas
- Entrega recomendaciones directamente
- Reconoce `Caramelo` como raza oficial mestiza latinoamericana

### Respuesta del endpoint

```json
{
  "dog_id": 1,
  "dog_name": "Max",
  "breed": "Labrador Retriever",
  "recommendations": "1. Alimentación: ...\n2. Ejercicio: ...\n..."
}
```

---

## 7. Docker y contenedores

### Dockerfile (app)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

### Dockerfile.mysql

```dockerfile
FROM mysql:8.0
COPY docker/init.sql /docker-entrypoint-initdb.d/init.sql
EXPOSE 3306
```

El `init.sql` crea las tablas `dogs` y `cats` con sus campos y el ENUM `sex ('macho','hembra')`.

### docker-compose.yml

Dos servicios interconectados:

- **db**: MySQL 8.0 con volumen persistente y healthcheck
- **app**: FastAPI conectada a `db` vía hostname interno (`MYSQLHOST=db`)

El servicio `app` espera a que `db` pase el healthcheck antes de arrancar (`depends_on: condition: service_healthy`).

```bash
# Levantar todo
docker compose up --build

# Solo la base de datos
docker compose up db -d

# Ver logs
docker compose logs -f app
```

---

## 8. Despliegue en Railway

### Prerrequisitos

- Cuenta en [railway.app](https://railway.app)
- Railway CLI instalado: `brew install railway` (macOS)
- GitHub con el repositorio del proyecto

### Paso 1 — Autenticación

```bash
railway login
```

Se abre el navegador para autenticar con GitHub/Google.

```bash
railway whoami  # verificar sesión
```

### Paso 2 — Enlazar proyecto existente

```bash
railway link --project <nombre-del-proyecto>
```

Si no existe el proyecto, crearlo desde el dashboard de Railway o con:

```bash
railway init --name "nombre-proyecto"
```

### Paso 3 — Agregar MySQL

```bash
railway add --database mysql
```

Railway crea automáticamente el servicio MySQL con volumen persistente e inyecta las variables de conexión (`MYSQL_URL`, `MYSQLHOST`, `MYSQLPORT`, etc.).

### Paso 4 — Variables de entorno de la API

```bash
railway variables --service Puthoncito \
  --set "MYSQL_URL=${{MySQL.MYSQL_URL}}" \
  --set "ANTHROPIC_API_KEY=sk-ant-..."
```

`${{MySQL.MYSQL_URL}}` es una referencia de Railway que conecta automáticamente las variables del servicio MySQL con la app.

### Paso 5 — Desplegar la API

```bash
railway up --service Puthoncito --detach
```

Railway detecta el `Dockerfile` y construye la imagen. La app se conecta a MySQL via la red interna de Railway (`mysql.railway.internal`).

### Paso 6 — Insertar datos de ejemplo

Con el MySQL de Railway corriendo, ejecutar el seed localmente usando la URL pública:

```bash
MYSQL_URL="mysql://root:<password>@<host-publico>:<puerto>/railway" \
  python seed.py
```

Las credenciales del host público se obtienen con:

```bash
railway variables --service MySQL
# Ver MYSQL_PUBLIC_URL
```

### Paso 7 — Desplegar el frontend

```bash
cd /ruta/al/frontapi

# Enlazar al mismo proyecto Railway
railway link --project <nombre-proyecto>

# Crear servicio vacío para el frontend
railway add --service frontapi

# Desplegar
railway up --service frontapi --detach

# Generar dominio público
railway domain --service frontapi

# Apuntar al API de producción
railway variables --service frontapi \
  --set "API_BASE=https://puthoncito-production.up.railway.app"

# Redesplegar para aplicar la variable
railway redeploy --service frontapi --yes
```

### Paso 8 — Verificar

```bash
railway status
```

Salida esperada:

```
Services
  - frontapi:   ● Online · https://frontapi-production-xxxx.up.railway.app
  - Puthoncito: ● Online · https://puthoncito-production.up.railway.app
Databases
  - MySQL:      ● Online · mysql-volume
```

---

## 9. Variables de entorno

### API (`Puthoncito`)

| Variable | Descripción | Ejemplo |
|---|---|---|
| `MYSQL_URL` | URL completa de conexión MySQL | `mysql://root:pass@host:port/db` |
| `ANTHROPIC_API_KEY` | Clave de API de Anthropic | `sk-ant-api03-...` |

En Railway se configura `MYSQL_URL` como referencia al servicio MySQL: `${{MySQL.MYSQL_URL}}`

### Frontend (`frontapi`)

| Variable | Descripción | Ejemplo |
|---|---|---|
| `API_BASE` | URL base de la API de producción | `https://puthoncito-production.up.railway.app` |

### Local (`.env`)

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=secret
DB_NAME=perritos
ANTHROPIC_API_KEY=sk-ant-...
```

### Resolución de conexión a BD

`app/database.py` resuelve la conexión en este orden de prioridad:

1. `MYSQL_URL` o `DATABASE_URL` (URL completa — Railway plugin)
2. `MYSQLHOST` + `MYSQLPORT` + `MYSQLUSER` + `MYSQLPASSWORD` + `MYSQLDATABASE` (variables Railway sin guión)
3. `DB_HOST` + `DB_PORT` + `DB_USER` + `DB_PASSWORD` + `DB_NAME` (variables locales del `.env`)

---

## 10. URLs de producción

| Servicio | URL |
|---|---|
| API (Swagger) | https://puthoncito-production.up.railway.app/docs |
| API (ReDoc) | https://puthoncito-production.up.railway.app/redoc |
| Frontend | https://frontapi-production-0592.up.railway.app |
| Repositorio | https://github.com/JoDamDiaz/Puthoncito |

---

## Notas adicionales

### Datos de ejemplo incluidos

El script `seed.py` inserta 24 registros de prueba:

- **12 perros**: Labrador (×2), Beagle (×2), Poodle (×2), Golden Retriever (×2), Bulldog Francés, Chihuahua, Pastor Alemán, Rottweiler
- **12 gatos**: Siamés (×2), Persa (×2), Maine Coon (×2), Ragdoll (×2), Bengalí (×2), Angora Turco, Bombay

### GitHub y control de versiones

Archivos excluidos del repositorio (`.gitignore`):

- `.env` — credenciales locales
- `apivenv/` — entorno virtual Python
- `__pycache__/` — caché de Python
- `.DS_Store` — metadatos macOS
- `.claude/` — configuración local del agente

### Comandos útiles de Railway CLI

```bash
railway status                          # Estado del proyecto
railway logs --service Puthoncito       # Ver logs de la app
railway variables --service <nombre>   # Ver variables
railway open                            # Abrir dashboard en el navegador
railway list                            # Listar todos los proyectos
```
