# Proyecto: Device Systems API
*Fecha de reporte: 27/05/2026*

---

## Descripción de la Aplicación
<p><b>device_systems</b> es un microservicio backend desarrollado con FastAPI diseñado para la gestión centralizada, validación y administración del recurso de usuarios del sistema. La aplicación implementa una arquitectura REST funcional, garantizando el control estricto de tipos de datos en tiempo de ejecución, filtrado avanzado mediante parámetros de consulta, y políticas de seguridad para la prevención de registros duplicados.</p>

---

## Guía de Instalación y Ejecución

### Prerrequisitos
* Python 3.13 instalado globalmente.
* Git para la gestión del repositorio.

### Instrucciones de Despliegue Local
```bash
# 1. Clonar el repositorio desde GitHub
git clone [https://github.com/alycano/device_systems.git](https://github.com/alycano/device_systems.git)
cd device_systems

# 2. Crear y activar el entorno virtual aislado
python -m venv fastapi_env
# En Windows (Git Bash):
source fastapi_env/Scripts/activate

# 3. Instalar las dependencias oficiales requeridas
pip install -r requirements.txt

# 4. Iniciar el servidor de desarrollo en bucle de recarga automática
python -m uvicorn app.main:app --reload

## Fase 5 - Cabeceras y Respuestas Personalizadas
<p>En la quinta y última fase del proyecto, configuré la manipulación de metadatos en el protocolo HTTP mediante la inyección de cabeceras personalizadas en todas las respuestas del servidor. A través de la inclusión del parámetro 'Response' en las funciones de los endpoints, desarrollé una función auxiliar estandarizada que añade los encabezados 'X-App-Name' con el valor del proyecto y 'X-API-Version' fijado en la versión actual del sistema. Este procedimiento garantiza el cumplimiento de los estándares de auditoría y rastreabilidad solicitados en la rúbrica técnica, permitiendo que cualquier cliente que consuma la API pueda identificar de forma clara el origen y la versión del backend con el que interactúa. Con esta implementación, la arquitectura del microservicio queda totalmente integrada, validada y documentada de acuerdo a las buenas prácticas globales de desarrollo de software.</p>

---

## Fase 6 - Especificación de Servicios y Matriz de Endpoints
<p>En esta sección se detalla la matriz de operación de la API REST construida, mapeando los verbos HTTP correspondientes, los mecanismos de paso de parámetros requeridos y las respuestas devueltas por el servidor.</p>

### Matriz Técnica de Rutas
| Método | Ruta (Endpoint) | Parámetro | Ubicación | Código de Éxito | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GET** | `/users` | Ninguno / Filtros | Query (Opcional) | 200 OK | Retorna la lista de usuarios completa o filtrada por rol/estado. |
| **GET** | `/users/{user_id}` | `user_id` (int) | Path (Obligatorio) | 200 OK | Recupera los datos de un usuario por su ID único o devuelve 404. |
| **POST** | `/users` | Estructura JSON | Request Body | 201 Created | Registra un usuario en memoria validando duplicados de ID y correo. |

### Ejemplos de Estructuras de Datos (Payloads)

#### Petición POST /users (Input Body)
```json
{
  "id": 4,
  "name": "Estudiante Sena",
  "email": "estudiante@sena.edu.co",
  "role": "user",
  "is_active": true
}

{
  "id": 4,
  "name": "Estudiante Sena",
  "email": "estudiante@sena.edu.co",
  "role": "user",
  "is_active": true
}

## Evidencias de Pruebas Funcionales (Swagger UI)
<p>Las capturas de pantalla integradas en el repositorio demuestran de forma secuencial la ejecución satisfactoria y el comportamiento del microservicio ante diferentes escenarios de petición. En el ámbito de las operaciones de consulta, adjunté las evidencias correspondientes al listado general inicial de usuarios (evidencias/1_get_todos.png), el comportamiento de los filtros de búsqueda por rol administrativo (evidencias/2_get_todos2.png), la segmentación por estado activo o inactivo (evidencias/3_get_todos3.png), y la verificación de la persistencia de datos en memoria tras realizar consultas masivas (evidencias/6_get_todos4.png). Adicionalmente, documenté la búsqueda exitosa de registros específicos mediante identificadores numéricos en la ruta de acceso (evidencias/7_buscar_por_id.png), la validación avanzada de parámetros secundarios en peticiones GET (evidencias/8_buscar_por_id2.png), y el correcto disparo de la excepción HTTP 404 cuando el identificador consultado no coincide con ningún registro del sistema (evidencias/9_error_404.png).</p>

<p>En lo que respecta al endpoint de escritura y el manejo de lógica de negocio, incluí las capturas detalladas que certifican la creación exitosa de un nuevo usuario con el código de respuesta 201 Created (evidencias/4_post_usuario.png), reflejando la inmediata actualización de la colección temporal. Por último, registré el funcionamiento del sistema de excepciones ante peticiones erróneas o maliciosas (evidencias/5_post_usuario2.png), donde el backend interrumpe el flujo y retorna un código 400 Bad Request al detectar intentos de registro con identificadores numéricos duplicados o correos electrónicos que ya se encuentran en uso por otros usuarios, demostrando la robustez de las validaciones de Pydantic v2 y el control de concurrencia diseñado para salvaguardar la integridad de la aplicación.</p>

---

## Reflexión sobre el uso de FastAPI en la Arquitectura REST
<p>El desarrollo de este reto integrador evidencia que FastAPI representa una evolución disruptiva en la construcción de servicios backend bajo el lenguaje Python. Su integración nativa con Pydantic v2 resuelve de forma elegante la validación de tipos de datos en tiempo de ejecución, transformando una tarea que tradicionalmente requería múltiples líneas de código de control en un proceso declarativo y automatizado. Asimismo, la generación automática de la documentación bajo el estándar OpenAPI (Swagger UI) optimiza los tiempos de desarrollo y facilita la comunicación con equipos de desarrollo externos o de aseguramiento de calidad. En conclusión, FastAPI no solo incrementa la velocidad de ejecución del software gracias a su soporte asíncrono, sino que eleva la productividad del desarrollador al garantizar la robustez, la tipificación estricta y el manejo nativo de errores HTTP con un esfuerzo de infraestructura mínimo.</p>

---

# Proyecto: Device Systems API (Evolución CRUD y Arquitectura Modular)
*Fecha de reporte: 04/06/2026*

---

## Descripción de la Aplicación
<p><b>device_systems</b> es un microservicio backend desarrollado con FastAPI diseñado para la gestión centralizada, validación y administración del recurso de usuarios del sistema. En esta segunda versión, la aplicación evoluciona de manera estructural hacia una solución profesional y robusta de nivel empresarial. Se implementa un ciclo CRUD completo para el recurso de usuarios, integrando inyección de dependencias para la reutilización de lógica de validación, un sistema avanzado y tipificado de control de excepciones HTTP, y metadatos extendidos para la autogeneración de la documentación OpenAPI.</p>

---

## Guía de Instalación y Ejecución

### Prerrequisitos
* Python 3.11 o superior instalado globalmente.
* Git para la gestión del repositorio.

### Instrucciones de Despliegue Local
```bash
# 1. Clonar el repositorio y acceder a la rama de la evolución técnica
git clone [https://github.com/alycano/device_systems.git](https://github.com/alycano/device_systems.git)
cd device_systems
git checkout feature-evolucion-api

# 2. Crear y activar el entorno virtual aislado
python -m venv fastapi_env
# En Windows (Git Bash):
source fastapi_env/Scripts/activate

# 3. Instalar las dependencias oficiales requeridas (FastAPI, Pydantic, Uvicorn)
pip install -r requirements.txt

# 4. Iniciar el servidor de desarrollo en bucle de recarga automática
uvicorn app.main:app --reload