#!/usr/bin/env python
"""
Lanzador Inteligente de ACADEMIX para Red Local (LAN / Wi-Fi / Ethernet).
Detecta la dirección IP de red de la máquina, verifica el estado del sistema,
muestra las URLs de acceso para otros dispositivos y ejecuta el servidor en 0.0.0.0.
"""

import os
import sys
import socket
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def get_network_ips():
    """Detecta las direcciones IP activas de la maquina en la red local."""
    ips = []
    
    # Metodo 1: Enrutamiento de socket UDP (obtiene la IP con salida a red activa)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        primary_ip = s.getsockname()[0]
        s.close()
        if primary_ip and not primary_ip.startswith("127."):
            ips.append(primary_ip)
    except Exception:
        pass

    # Metodo 2: Resolucion por hostname
    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if not ip.startswith("127.") and not ip.startswith("169.254.") and ip not in ips:
                ips.append(ip)
    except Exception:
        pass

    return ips

def is_port_in_use(port):
    """Comprueba si el puerto especificado ya esta en uso."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def print_banner(ips, port=8000):
    """Imprime un banner informativo con instrucciones claras de acceso en red."""
    width = 74
    print("=" * width)
    print("   ACADEMIX - SISTEMA DE GESTIÓN ACADÉMICA Y CONTROL ESCOLAR".center(width))
    print("                 MODO SERVIDOR DE RED LOCAL (LAN / Wi-Fi)".center(width))
    print("=" * width)
    print()
    print(f" [*] Estado del Servidor : INICIANDO...")
    print(f" [*] Escuchando en       : 0.0.0.0:{port} (Todas las interfaces de red)")
    print()
    print(" [1] ACCESO DESDE ESTA COMPUTADORA (Servidor):")
    print(f"     -> http://localhost:{port}/")
    print(f"     -> http://127.0.0.1:{port}/")
    print()
    print(" [2] ACCESO DESDE OTROS DISPOSITIVOS EN LA MISMA RED (Celulares, Tablets, PCs):")
    if ips:
        for ip in ips:
            print(f"     -> http://{ip}:{port}/")
    else:
        print("     [!] No se detecto IP de red externa activa. Verifique su conexion Wi-Fi o Ethernet.")
    print()
    print(" [i] RECOMENDACIONES CLAVE:")
    print("     * Asegúrese de que los otros equipos estén en la MISMA red Wi-Fi o cable.")
    print("     * Si otro equipo no puede entrar, ejecute 'firewall.bat' para permitir")
    print(f"       el puerto {port} en el Firewall de Windows.")
    print("     * Para detener el servidor, presione Ctrl + C en esta ventana.")
    print("=" * width)
    print()

def main():
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    ips = get_network_ips()

    if is_port_in_use(port):
        print(f"\n[ADVERTENCIA] El puerto {port} parece estar en uso.")
        print(f"Intentando iniciar de todos modos o puede cancelar con Ctrl+C.\n")

    print_banner(ips, port)

    # Asegurar el directorio de trabajo
    os.chdir(BASE_DIR)

    # Determinar el ejecutable de Python (preferir venv si existe)
    venv_python = BASE_DIR / "venv" / "Scripts" / "python.exe"
    python_bin = str(venv_python) if venv_python.exists() else sys.executable

    manage_py = BASE_DIR / "manage.py"

    cmd = [python_bin, str(manage_py), "runserver", f"0.0.0.0:{port}"]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n[INFO] Servidor ACADEMIX detenido por el usuario.")

if __name__ == '__main__':
    main()
