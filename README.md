# Proyecto: Device Systems API
*Fecha de reporte: 27/05/2026*

---

## Fase 1 - Evidencia de Configuración
<p>En esta primera fase del proyecto 'device_systems', configuré con éxito la estructura base del entorno backend utilizando Python 3.13. Inicialicé un repositorio Git local y organicé las carpetas de manera modular, separando los esquemas de validación y los enrutadores lógicos dentro del directorio principal 'app' para garantizar la escalabilidad de la arquitectura. Asimismo, creé y activé un entorno virtual aislado denominado 'fastapi_env' para prevenir conflictos de dependencias en el sistema global, y mediante el archivo 'requirements.txt' instalé de forma estricta las versiones oficiales requeridas para este reto: FastAPI v0.115.0 y Uvicorn v0.31.0 con soporte estándar. Finalmente, implementé un archivo '.gitignore' personalizado para asegurar que los archivos temporales de Python y los binarios del entorno virtual no se suban al repositorio remoto de GitHub, cumpliendo así con las buenas prácticas de desarrollo profesional desde el despliegue inicial.</p>

---

## Fase 2 - Modelo de Usuario con Pydantic
<p>En la segunda fase del proyecto, implementé la capa de validación de datos para el recurso de usuarios mediante el uso de 'Pydantic v2' dentro del módulo 'user_schema.py'. Siguiendo las buenas prácticas de arquitectura de software, definí una estructura de datos segmentada que consta de un modelo base ('UserBase'), un modelo de entrada para la creación de registros ('UserCreate') y un modelo de salida estandarizado ('UserResponse'), actuando este último como el 'Response Model' solicitado en la guía. Para administrar de forma estricta los privilegios de acceso en el sistema, incorporé la clase 'Enum' de Python, limitando el campo 'role' exclusivamente a los valores fijos de 'admin', 'support' y 'user'. Asimismo, utilicé la clase 'Field' para añadir restricciones numéricas y de longitud en tiempo de ejecución, obligando a que el campo 'name' posea un mínimo de 3 caracteres y el 'id' sea un entero estrictamente mayor a cero, mientras que el campo 'email' quedó respaldado por el tipo especializado 'EmailStr' para garantizar la estructura sintáctica correcta de cada dirección de correo electrónico recibida.</p>

---

## Fase 3 - Endpoints GET con Parámetros
<p>En la tercera fase del proyecto, desarrollé los endpoints de lectura para el recurso de usuarios dentro del enrutador modular 'user_routes.py', utilizando el decorador '@router.get' para exponer las rutas de consulta HTTP. Con el objetivo de simular un entorno de producción persistente, estructuré una base de datos en memoria denominada 'db_users' poblada con registros iniciales tipados. Implementé un endpoint general para listar la colección completa de usuarios, el cual integra 'Query Parameters' opcionales que permiten al cliente filtrar las respuestas de forma dinámica según el rol administrativo asignado o el estado de actividad del usuario en el sistema. Asimismo, diseñé un endpoint específico que emplea 'Path Parameters' dinámicos para recuperar la información de un único usuario a través de su identificador numérico; este endpoint incluye una estructura de control de flujo que valida la existencia del recurso en la lista local y, en caso de que el identificador consultado no coincida con ningún registro, dispara de forma automática una excepción 'HTTPException' con un código de estado 404 de recurso no encontrado, garantizando una respuesta estandarizada y segura.</p>

---
