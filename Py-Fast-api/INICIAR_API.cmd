@echo off
setlocal
cd /d "%~dp0"
title API de aprendices - FastAPI

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: No se encontro el entorno virtual de Python.
    echo Ejecuta Preparar_entorno.cmd antes de iniciar la API.
    goto failed
)

if not exist ".env" if not defined MONGO_URI (
    echo ERROR: No se encontro .env ni la variable MONGO_URI.
    echo Copia .env.example a .env y configura MONGO_URI.
    goto failed
)

echo Iniciando la API desde %CD%
".venv\Scripts\python.exe" -m uvicorn src.main:app --app-dir . --reload
if errorlevel 1 goto failed
exit /b 0

:failed
echo.
echo No se pudo iniciar la API. Revisa el mensaje anterior.
pause
exit /b 1
