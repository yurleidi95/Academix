@echo off
chcp 65001 >nul
title ACADEMIX - Servidor de Red Local

cd /d "%~dp0"

echo ======================================================================
echo             INICIANDO ACADEMIX EN MODO RED LOCAL (LAN)
echo ======================================================================
echo.

:: Verificar si existe el entorno virtual
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] No se encontro el entorno virtual en 'venv\Scripts\python.exe'.
    echo Por favor asegurese de tener Python instalado y el entorno configurado.
    pause
    exit /b 1
)

:: Ejecutar el script inteligente de red
"venv\Scripts\python.exe" iniciar_servidor_red.py

if %errorLevel% neq 0 (
    echo.
    echo [AVISO] El servidor se ha detenido.
    pause
)
