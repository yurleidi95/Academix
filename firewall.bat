@echo off
chcp 65001 >nul
echo ======================================================================
echo          ACADEMIX - CONFIGURACION DE FIREWALL PARA RED LOCAL
echo ======================================================================
echo.
echo Este script abrira el puerto TCP 8000 en el Firewall de Windows
echo para que otros dispositivos en tu red local (PC, celular, tablet)
echo puedan conectarse sin ser bloqueados.
echo.

:: Verificar permisos de Administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [AVISO] Se requieren permisos de Administrador para modificar el Firewall.
    echo Solicitando elevacion de privilegios...
    powershell -Command "Start-Process cmd -ArgumentList '/c %~fn0' -Verb RunAs"
    exit /b
)

echo [1/2] Eliminando regla previa si existia...
netsh advfirewall firewall delete rule name="ACADEMIX Red Local (Puerto 8000)" >nul 2>&1

echo [2/2] Creando regla de entrada en el Firewall para el puerto 8000...
netsh advfirewall firewall add rule name="ACADEMIX Red Local (Puerto 8000)" dir=in action=allow protocol=TCP localport=8000

if %errorLevel% equ 0 (
    echo.
    echo ======================================================================
    echo  [EXITO] El puerto 8000 ha quedado habilitado correctamente.
    echo  Los dispositivos en tu red ya pueden comunicarse con ACADEMIX.
    echo ======================================================================
) else (
    echo.
    echo [ERROR] No se pudo crear la regla en el Firewall.
    echo Por favor ejecuta este archivo haciendo clic derecho -> "Ejecutar como administrador".
)

echo.
pause
