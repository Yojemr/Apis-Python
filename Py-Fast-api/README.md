# Py-Fast-api

Proyecto de clase con FastAPI, modelos Pydantic y MongoDB para gestionar
aprendices. Los endpoints HTTP se definen en `src/main.py`;
`src/views/controllers.py` contiene el acceso a datos y `src/templates/templates.py`
reserva un router para futuras rutas, sin duplicar las existentes.

## Preparación en Windows

Requisitos: Python 3.14 e internet para instalar las dependencias.

1. Ejecutar `Preparar_entorno.cmd` con doble clic.
2. Copiar `.env.example` como `.env` y establecer `MONGO_URI` con la conexión del entorno de clase.
3. Para trabajar desde PowerShell, usar `.\.venv\Scripts\python.exe`.

El script crea `.venv` dentro del proyecto. `.env` y `.venv` están excluidos de Git.
Las variables de entorno existentes tienen prioridad sobre `.env`.

4. Iniciar la API desde la carpeta `Py-Fast-api`:

```powershell
.\.venv\Scripts\python.exe -m uvicorn src.main:app --reload
```

Abrir http://127.0.0.1:8000/docs para consultar la documentación de FastAPI.
La ruta `POST /trainee` funciona, pero no aparece en Swagger porque
`main.py` la define con `include_in_schema=False`.

## Rutas implementadas

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/` | Mensaje de bienvenida |
| POST | `/trainee` | Crear un aprendiz (HTTP 201) |
| GET | `/trainees` | Listar aprendices |
| GET | `/trainee/{id}` | Consultar por ID |
| PUT | `/trainee/{id}` | Actualizar parcialmente por ID |
| DELETE | `/trainee/{id}` | Eliminar por ID y devolver un mensaje |

Para consultar, actualizar o eliminar se utiliza el identificador `_id`
de MongoDB convertido a texto (24 caracteres hexadecimales), no el campo
`document`. Los identificadores inexistentes o inválidos devuelven HTTP 404.


## Comprobaciones locales

Desde la carpeta `Py-Fast-api`:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m unittest discover -s test -p "test_*.py" -v
.\.venv\Scripts\python.exe -m pip check
```

Las pruebas no necesitan credenciales ni acceso a MongoDB.

## MongoDB

Comprobar únicamente la conexión configurada:

```powershell
.\.venv\Scripts\python.exe src/models/database.py
```

La demostración `examples/mongodb_insert.py` inserta un documento cada vez que se ejecuta. Se ejecuta manualmente sobre una base de clase preparada para esa operación.

## Estructura

| Ruta | Contenido |
| --- | --- |
| `src/models` | Modelos y conexión MongoDB |
| `src/views` | Controladores de las operaciones CRUD y serialización |
| `src/templates` | Router reservado para futuras rutas, sin endpoints duplicados |
| `test` | Pruebas automáticas aisladas |
| `examples` | Demostraciones manuales |
| `data` | Carpeta de datos del proyecto |
