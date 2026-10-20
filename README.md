# Apis-Python

Repositorio de ejercicios y proyectos de API en Python desarrollados durante las clases. El proyecto implementado actualmente es **Py-Fast-api**, una API REST para la gestión de aprendices, respaldada por MongoDB y acompañada de una interfaz de consola.

## Características

- API REST construida con FastAPI y documentada con OpenAPI/Swagger.
- Operaciones CRUD de aprendices: crear, listar, consultar por ID, actualizar y eliminar.
- Validación de datos con Pydantic, incluida la validación del correo electrónico.
- Persistencia en MongoDB mediante PyMongo.
- CLI interactiva que consume la API por HTTP con HTTPX; puede conectarse al despliegue de Render o a una instancia local.
- Pruebas aisladas con conexiones y colecciones simuladas; no requieren escribir datos en MongoDB.
- Configuración de secretos mediante variables de entorno y archivos `.env` locales excluidos de Git.

## Despliegue

- **Swagger / documentación interactiva:** [https://apis-python.onrender.com/docs](https://apis-python.onrender.com/docs)
- **API en Render:** [https://apis-python.onrender.com](https://apis-python.onrender.com)

Render puede tardar en responder la primera vez después de un periodo de inactividad en el plan gratuito.

## Estructura del repositorio

```text
Apis-Python/
├── .github/workflows/       # Integración continua
├── Py-Fast-api/             # Aplicación FastAPI y CLI
│   ├── src/
│   │   ├── main.py          # Aplicación y rutas HTTP
│   │   ├── models/          # Modelos Pydantic y conexión MongoDB
│   │   ├── templates/       # Router reservado para nuevas rutas
│   │   └── views/
│   │       ├── controllers.py # Operaciones CRUD contra MongoDB
│   │       └── view.py        # Menú CLI que consume la API
│   ├── test/                # Pruebas aisladas
│   ├── examples/            # Ejemplos manuales de acceso a MongoDB
│   ├── data/                # Carpeta para datos del proyecto
│   ├── requirements.txt     # Dependencias de ejecución
│   ├── requirements-dev.txt # Dependencias de desarrollo
│   ├── .env.example         # Plantilla sin secretos
│   └── README.md            # Guía detallada del proyecto FastAPI
├── CONTRIBUTING.md          # Flujo y convenciones de contribución
└── README.md
```

## Requisitos

- Python 3.14, según la configuración actual del proyecto.
- MongoDB accesible para ejecutar las operaciones CRUD de la API.
- Git para clonar y actualizar el repositorio.

## Instalación y configuración

En PowerShell, desde la carpeta raíz del repositorio:

```powershell
cd Py-Fast-api
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Edita `.env` y configura `MONGO_URI` con la URI privada de tu base de datos. No publiques ese archivo ni pegues la URI en el README, el código o los commits. El archivo `.env` está excluido de Git.

También puedes ejecutar `Preparar_entorno.cmd` para instalar las dependencias de ejecución y `INICIAR_API.cmd` para iniciar la API en Windows.

## Iniciar la API local

Desde `Py-Fast-api`:

```powershell
.\.venv\Scripts\python.exe -m uvicorn src.main:app --reload
```

La API local queda disponible en `http://127.0.0.1:8000`. Abre `http://127.0.0.1:8000/docs` para usar Swagger.

## Usar la interfaz de consola

La CLI realiza solicitudes HTTP a la API; no accede directamente a MongoDB. Inicia la API local o usa el despliegue configurado por defecto y ejecuta, desde `Py-Fast-api`:

```powershell
.\.venv\Scripts\python.exe -m src.views.view
```

El menú ofrece listar, consultar, crear, actualizar y eliminar aprendices. Para eliminar un registro solicita confirmación. La actualización permite dejar en blanco los campos que se desean conservar sin cambios. La validación final del correo y de los datos la realiza la API.

**Importante:** si usas la URL de Render, crear, actualizar y eliminar modifica los datos reales del servicio desplegado. Para practicar sin afectar esos datos, configura `API_BASE_URL` para apuntar a una instancia local.

Por defecto, la CLI usa `https://apis-python.onrender.com`. Para apuntarla a una API local, configura la variable en la misma terminal antes de ejecutarla:

```powershell
$env:API_BASE_URL = "http://127.0.0.1:8000"
.\.venv\Scripts\python.exe -m src.views.view
```

Para volver al servicio de Render, elimina la variable de esa sesión con `Remove-Item Env:API_BASE_URL` o abre una terminal nueva.

## Endpoints disponibles

| Método | Ruta | Uso |
| --- | --- | --- |
| `GET` | `/` | Comprobar el mensaje de bienvenida |
| `POST` | `/trainee` | Crear un aprendiz; responde con HTTP 201 |
| `GET` | `/trainees` | Listar aprendices |
| `GET` | `/trainee/{id}` | Consultar por ID de MongoDB |
| `PUT` | `/trainee/{id}` | Actualizar los campos enviados |
| `DELETE` | `/trainee/{id}` | Eliminar por ID de MongoDB |

Los datos requeridos para crear son `document`, `firstname`, `lastname`, `email`, `age`, `program` y `record_number`. Las rutas por ID usan el `id` hexadecimal que devuelve la API, no el número de documento.

## Comprobaciones de desarrollo

Desde `Py-Fast-api`:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m unittest discover -s test -p "test_*.py" -v
.\.venv\Scripts\python.exe -m pip check
```

Las pruebas están diseñadas para usar dobles y datos ficticios, sin escrituras en la base de datos.

## Documentación adicional

- [Guía detallada de Py-Fast-api](Py-Fast-api/README.md)
- [Guía para contribuir](CONTRIBUTING.md)
