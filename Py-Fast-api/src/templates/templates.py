"""Router reservado para nuevas rutas fuera de main.py.

Las rutas CRUD de aprendices ya se definen en src/main.py. No se vuelven a
registrar aqui para evitar conflictos y duplicados en OpenAPI.
"""

from fastapi import APIRouter

router = APIRouter()
