@echo off
title Instalador de Dependencias PyQuarto
color 0A

echo ========================================================
echo   Instalando dependencias de la plantilla PyQuarto...
echo ========================================================
echo.

:: Cambiar al directorio donde está el script (útil si se ejecuta como administrador)
cd /d "%~dp0"

:: Verifica si python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] No se detecto Python en tu sistema. 
    echo Por favor instala Python antes de continuar.
    echo.
    pause
    exit /b 1
)

:: Ejecuta el script de instalación dinámica de librerías
python scripts\instalar_dependencias.py
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [ERROR] Hubo un problema durante la instalacion.
    echo Por favor revisa los mensajes de error arriba.
    echo.
    pause
    exit /b %errorlevel%
)

echo.
echo ========================================================
echo   Instalacion completada con exito.
echo   Ya puedes renderizar tus informes con Quarto.
echo ========================================================
echo.
pause
