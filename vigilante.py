import psutil
import time
import os
from pathlib import Path
from datetime import datetime

# Configuración
ruta = "/"
umbral = 10             # porcentaje libre mínimo
intervalo = 1           # segundos entre comprobaciones
archivo_alerta = Path("/tmp/alerta_disco.txt")

alerta_activa = False   # evita alertas repetidas

while True:
    os.system("clear")
    uso = psutil.disk_usage(ruta)
    porcentaje_libre = uso.free / uso.total * 100

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}]")
    print(f"Espacio total: {uso.total / (1024**3):.2f} GB")
    print(f"Espacio usado: {uso.used / (1024**3):.2f} GB")
    print(f"Espacio libre: {uso.free / (1024**3):.2f} GB")
    print(f"Porcentaje libre: {porcentaje_libre:.2f}%\n")

    if porcentaje_libre < umbral:
        if not alerta_activa:  # solo una alerta por incidente
            alerta_activa = True
            archivo_alerta.write_text(
                f"[ALERTA] Espacio crítico: {porcentaje_libre:.2f}% libre"
                f"Espacio total: {uso.total / (1024**3):.2f} GB"
                f"Espacio usado: {uso.used / (1024**3):.2f} GB"
                f"Espacio libre: {uso.free / (1024**3):.2f} GB"
                f"Porcentaje libre: {porcentaje_libre:.2f}%"
                f"Fecha: {timestamp}\n"
            )
            print("ALERTA generada")
    else:
        alerta_activa = False  # se resetea cuando el disco sube

    time.sleep(intervalo)