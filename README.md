# Device Systems API

**Versión:** 3.0.0  
**Fecha de actualización:** 24/06/2026  
**Proyecto:** GA1-220501096-01-AA1-EV11 – FastAPI Seguridad (ADSO SENA)

---

## Descripción

**device_systems** es un microservicio backend desarrollado con **FastAPI** para la gestión centralizada de usuarios, inventario de hardware IT y control de préstamos de equipos. Esta versión incorpora una capa completa de **seguridad profesional**:

- Autenticación **OAuth2 con JWT**
- Hash de contraseñas con **bcrypt** (passlib)
- Protección de rutas por **roles** (admin, support, user)
- **Rate limiting** con slowapi
- **Middleware** personalizado con trazabilidad
- **CORS** configurado para entornos controlados
- **Validaciones avanzadas** con Pydantic v2

---

## Arquitectura del Proyecto

### Estructura Completa

```
device_systems/
│
├── .env                          # Variables de entorno (SECRET_KEY)
├── .env.example                  # Plantilla de variables de entorno
├── .gitignore
├── README.md
├── requirements.txt
├── alembic.ini
├── device_systems.db
│
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 59acfa326972_crear_tablas_iniciales.py
│       └── 256cc67dce0b_add_authentication_fields_to_users.py
│
├── app/
│   ├── main.py                   # Punto de entrada (CORS, middleware, routers)
│   │
│   ├── auth/                     # Módulo de autenticación
│   │   ├── __init__.py
│   │   ├── auth_routes.py        # Endpoints /auth
│   │   ├── auth_service.py       # Lógica de autenticación
│   │   └── security.py           # Hash, JWT, utilidades de seguridad
│   │
│   ├── database/
│   │   └── connection.py         # Configuración SQLAlchemy + SQLite
│   │
│   ├── dependencies/
│   │   ├── auth_dependency.py    # Dependencias: get_current_user, require_admin, etc.
│   │   └── database_dependency.py # Inyección de sesión BD
│   │
│   ├── middlewares/
│   │   ├── __init__.py
│   │   ├── rate_limiter.py       # Configuración de slowapi
│   │   └── request_middleware.py # Middleware: X-Process-Time, X-Request-ID
│   │
│   ├── models/
│   │   ├── user_model.py         # Modelo ORM: User (con hashed_password)
│   │   ├── device_model.py       # Modelo ORM: Device
│   │   └── loan_model.py         # Modelo ORM: Loan
│   │
│   ├── routes/
│   │   ├── user_routes.py        # Endpoints /users (protegidos)
│   │   ├── device_routes.py      # Endpoints /devices (protegidos por rol)
│   │   └── loan_routes.py        # Endpoints /loans (protegidos por rol)
│   │
│   ├── schemas/
│   │   ├── user_schema.py        # Schemas Pydantic: User (con password)
│   │   ├── device_schema.py      # Schemas Pydantic: Device
│   │   ├── loan_schema.py        # Schemas Pydantic: Loan
│   │   └── auth_schema.py        # Schemas: UserRegister, UserLogin, Token
│   │
│   └── services/
│       ├── user_service.py       # CRUD usuarios con SQLAlchemy
│       ├── device_service.py     # CRUD dispositivos con SQLAlchemy
│       └── loan_service.py       # Gestión de préstamos con SQLAlchemy
│
└── Evidencias/                   # Capturas de prueba funcional
    ├── 1_get_todos.png
    ...
    └── 9_error_404.png
```

---

## Seguridad Implementada

### 1. Hash de Contraseñas (bcrypt + passlib)

`app/auth/security.py`

| Función | Descripción |
|---|---|
| `get_password_hash(password)` | Genera hash bcrypt de la contraseña |
| `verify_password(plain, hashed)` | Verifica contraseña contra hash |
| `create_access_token(data)` | Genera token JWT con expiración (30 min) |
| `decode_access_token(token)` | Decodifica y valida token JWT |

### 2. Autenticación OAuth2 con JWT

Endpoints en `app/auth/auth_routes.py`:

| Método | Ruta | Protección | Descripción |
|---|---|---|---|
| **POST** | `/auth/register` | Pública | Registro de usuario con contraseña segura |
| **POST** | `/auth/login` | Pública | Login, retorna access_token JWT |
| **GET** | `/auth/me` | Token requerido | Datos del usuario autenticado |

### 3. Protección de Rutas por Roles

`app/dependencies/auth_dependency.py`

| Dependencia | Descripción |
|---|---|
| `get_current_user` | Valida token JWT, retorna usuario |
| `get_current_active_user` | Valida token + usuario activo |
| `require_admin` | Usuario activo con rol admin o support |
| `require_admin_only` | Solo administradores |

### 4. Matriz de Protección de Rutas

| Ruta | Método | Protección |
|---|---|---|
| `GET /users` | Autenticado + 30 req/min | `get_current_active_user` |
| `GET /users/{id}` | Autenticado | `get_current_active_user` |
| `POST /devices` | Admin o Support | `require_admin` |
| `PUT /devices/{id}` | Admin o Support | `require_admin` |
| `DELETE /devices/{id}` | Solo Admin | `require_admin_only` |
| `POST /loans` | Autenticado + 10 req/min | `get_current_active_user` |
| `POST /loans/{id}/return` | Admin o Support | `require_admin` |
| `GET /loans/details` | Admin o Support | `require_admin` |

### 5. Rate Limiting (slowapi)

| Endpoint | Límite |
|---|---|
| `POST /auth/login` | 5 solicitudes/minuto |
| `POST /auth/register` | 3 solicitudes/minuto |
| `GET /users` | 30 solicitudes/minuto |
| `POST /loans` | 10 solicitudes/minuto |

### 6. CORS

```python
allow_origins = [
    "http://localhost:5173",  # Vite/React
    "http://localhost:3000"   # React/Node
]
```

> **Nota:** En producción no se recomienda usar `"*"` cuando hay credenciales (`allow_credentials=True`), porque el estándar CORS exige que `allow_origins` sea explícito (no comodín) para solicitudes con credenciales.

### 7. Middleware Personalizado

`app/middlewares/request_middleware.py`

- `X-Process-Time`: Tiempo de respuesta en segundos
- `X-App-Name`: `device_systems`
- `X-Request-ID`: UUID único por petición (traza)

---

## Endpoints de la API

### Autenticación (`/auth`)

| Método | Ruta | Descripción | Códigos |
|---|---|---|---|
| POST | `/auth/register` | Registrar usuario | 201, 400 |
| POST | `/auth/login` | Iniciar sesión (retorna JWT) | 200, 401 |
| GET | `/auth/me` | Perfil del usuario autenticado | 200, 401 |

### Usuarios (`/users`)

| Método | Ruta | Parámetros | Protección | Códigos |
|---|---|---|---|---|
| GET | `/users` | role, is_active (query) | Auth | 200 |
| GET | `/users/{id}` | — | Auth | 200, 404 |
| POST | `/users` | Body: UserCreate | Pública | 201, 400 |
| PUT | `/users/{id}` | Body: UserUpdate | Pública | 200, 400, 404 |
| PATCH | `/users/{id}` | Body: UserPatch | Pública | 200, 400, 404 |
| DELETE | `/users/{id}` | — | Pública | 204, 404 |

### Dispositivos (`/devices`)

| Método | Ruta | Parámetros | Protección | Códigos |
|---|---|---|---|---|
| GET | `/devices` | device_type, is_available, search (query) | Pública | 200 |
| POST | `/devices` | Body: DeviceCreate | Admin/Support | 201, 400 |
| GET | `/devices/{id}` | — | Pública | 200, 404 |
| PUT | `/devices/{id}` | Body: DeviceUpdate | Admin/Support | 200, 404 |
| DELETE | `/devices/{id}` | — | Solo Admin | 204, 404 |

### Préstamos (`/loans`)

| Método | Ruta | Protección | Códigos |
|---|---|---|---|
| POST | `/loans` | Auth + 10 req/min | 201, 400, 404 |
| POST | `/loans/{id}/return` | Admin/Support | 200, 400, 404 |
| GET | `/loans/details` | Admin/Support | 200 |

---

## Validaciones de Contraseña (Pydantic v2)

`UserRegister` en `app/schemas/auth_schema.py`:

| Regla | Validación |
|---|---|
| Longitud mínima | 8 caracteres |
| Mayúscula | Al menos una |
| Minúscula | Al menos una |
| Número | Al menos un dígito |
| Espacios | No permitidos |

---

## Manejo de Errores

| Código | Significado |
|---|---|
| 200 | OK |
| 201 | Creado exitosamente |
| 204 | Eliminado (sin contenido) |
| 400 | Bad Request (datos inválidos, email duplicado, etc.) |
| 401 | Unauthorized (token inválido/faltante) |
| 403 | Forbidden (rol sin permisos) |
| 404 | Not Found (recurso no existe) |
| 429 | Too Many Requests (rate limit excedido) |
| 500 | Internal Server Error |

---

## Migraciones (Alembic)

### Migraciones Disponibles

| ID | Descripción |
|---|---|
| `59acfa326972` | Crear tablas iniciales (users, devices, loans) |
| `256cc67dce0b` | Agregar campo hashed_password a users |

### Comandos

```bash
# Ejecutar todas las migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1

# Generar nueva migración automática
alembic revision --autogenerate -m "descripcion"
```

---

## Guía de Instalación y Ejecución

### Prerrequisitos

- Python 3.11 o superior
- Git

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/alycano/device_systems.git
cd device_systems

# 2. Crear y activar entorno virtual
python -m venv fastapi_env
source fastapi_env/Scripts/activate     # Windows (Git Bash)
# source fastapi_env/bin/activate       # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar SECRET_KEY en .env para producción

# 5. Ejecutar migraciones
alembic upgrade head

# 6. Iniciar servidor
uvicorn app.main:app --reload
```

### Acceso

- **API:** `http://localhost:8000`
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## Flujo de Autenticación

```
1. POST /auth/register
   { "name": "...", "email": "...", "password": "MiPass123" }
   → 201 Created

2. POST /auth/login
   { "email": "...", "password": "MiPass123" }
   → { "access_token": "eyJ...", "token_type": "bearer" }

3. GET /auth/me
   Authorization: Bearer eyJ...
   → { "id": 1, "name": "...", "email": "...", "role": "user", "is_active": true }

4. GET /users (protegido)
   Authorization: Bearer eyJ...
   → [ { "id": 1, ... }, ... ]
```

---

## Dependencias Principales

| Paquete | Versión | Propósito |
|---|---|---|
| fastapi | 0.136.3 | Framework web ASGI |
| uvicorn | 0.48.0 | Servidor ASGI |
| pydantic | 2.13.4 | Validación de datos |
| SQLAlchemy | 2.0.50 | ORM para base de datos |
| alembic | — | Migraciones de BD |
| python-jose | 3.5.0 | JWT (JSON Web Tokens) |
| passlib | 1.7.4 | Hash de contraseñas |
| bcrypt | 4.0.1 | Algoritmo de hash |
| slowapi | 0.1.10 | Rate limiting |
| python-multipart | — | Soporte para formularios OAuth2 |
| email-validator | 2.3.0 | Validación de correos |

---

## Historial de Versiones

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 27/05/2026 | Versión inicial con datos en memoria |
| 1.1.0 | 04/06/2026 | CRUD, inyección de dependencias, cabeceras HTTP |
| 2.0.0 | 22/06/2026 | Persistencia SQLAlchemy + SQLite, Alembic, modelos Device/Loan |
| **3.0.0** | **24/06/2026** | **Seguridad: OAuth2+JWT, bcrypt, rate limiting, middleware, CORS, roles** |

---

## Evidencias de Pruebas (Requeridas EV11)

Las siguientes pruebas deben documentarse con capturas:

1. Registro de usuario
2. Registro con contraseña débil
3. Registro con email duplicado
4. Login correcto
5. Login con contraseña incorrecta
6. Consulta de /auth/me
7. Acceso a ruta protegida sin token
8. Acceso con token inválido
9. Acceso con usuario sin permisos (403)
10. Creación de dispositivo con rol permitido
11. Eliminación de dispositivo con rol no permitido
12. Configuración CORS
13. Cabeceras generadas por middleware
14. Activación de rate limiting (429)
15. Verificación de Swagger/OpenAPI con OAuth2

---

## Reflexión sobre Seguridad en APIs REST

La implementación de seguridad en APIs REST es crucial para proteger datos sensibles y garantizar la integridad del sistema. El uso de **JWT** permite autenticación stateless sin almacenar sesiones en servidor, mientras que **bcrypt** garantiza que las contraseñas se almacenen de forma segura mediante hash con sal. El **rate limiting** protege contra ataques de fuerza bruta y abuso de endpoints, y **CORS** controla qué dominios pueden consumir la API. Los **roles y permisos** aseguran que cada usuario tenga acceso solo a las operaciones que le corresponden, siguiendo el principio de mínimo privilegio.
