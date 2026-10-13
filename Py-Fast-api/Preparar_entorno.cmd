@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" goto install
where py >nul 2>&1
if errorlevel 1 goto python
py -3 -m venv .venv
if errorlevel 1 goto failed
goto install
:python
where python >nul 2>&1
if errorlevel 1 goto missing
python -m venv .venv
if errorlevel 1 goto failed
:install
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto failed
echo.
echo Entorno preparado. Para activarlo en CMD: .venv\Scripts\activate.bat
pause
exit /b 0
:missing
echo No se encontro Python. Instala Python 3 y vuelve a ejecutar este archivo.
pause
exit /b 1
:failed
echo No se pudo preparar el entorno. Revisa el error anterior.
pause
exit /b 1