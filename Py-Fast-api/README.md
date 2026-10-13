# Py-Fast-api

Proyecto de clase con modelos Pydantic de aprendices, conexión MongoDB y serialización de documentos.
`src/main.py` y las rutas HTTP están pendientes de desarrollo.

## Preparación en Windows

Requisitos: Python 3.14 e internet para instalar las dependencias.

1. Ejecutar `Preparar_entorno.cmd` con doble clic.
2. Copiar `.env.example` como `.env` y establecer `MONGO_URI` con la conexión del entorno de clase.
3. Para trabajar desde PowerShell, usar `.\.venv\Scripts\python.exe`.

El script crea `.venv` dentro del proyecto. `.env` y `.venv` están excluidos de Git.
Las variables de entorno existentes tienen prioridad sobre `.env`.

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
| `src/views` | Serialización y controladores en desarrollo |
| `src/templates` | Plantillas pendientes |
| `test` | Pruebas automáticas aisladas |
| `examples` | Demostraciones manuales |
| `data` | Carpeta de datos del proyecto |
