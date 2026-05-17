@echo off
title Instalador de Dependencias de Plantilla PyQuarto
color 0A

echo ========================================================
echo   Generando archivo de requerimientos de la plantilla
echo ========================================================
python scripts\generar_requerimientos.py
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Hubo un problema al generar los requerimientos.
    pause
    exit /b %errorlevel%
)

echo.
echo ========================================================
echo   Instalando dependencias...
echo ========================================================
python -m pip install -r scripts\requirements.txt
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Hubo un problema durante la instalacion.
    pause
    exit /b %errorlevel%
)

echo.
echo ========================================================
echo   Instalacion completada con exito.
echo ========================================================
pause
