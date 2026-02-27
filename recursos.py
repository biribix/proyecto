import shutil
import time
import os
from datetime import datetime

# ================= Configuración =================
ruta = "/"
umbral = 15             # porcentaje libre mínimo
intervalo = 2           # segundos entre actualizaciones de pantalla
archivo_alerta = "alerta_disco_structiva.txt"
# =================================================

alerta_activa = False   # evita escribir la misma alerta repetidas veces

# Códigos de color para la terminal de Linux
ROJO = '\033[91m'
VERDE = '\033[92m'
AMARILLO = '\033[93m'
RESET = '\033[0m'

while True:
    # Borra la pantalla para dar efecto de actualización
    os.system("clear")
    
    # 1. Obtenemos los datos con shutil (nativa de Python)
    uso = shutil.disk_usage(ruta)
    porcentaje_libre = (uso.free / uso.total) * 100
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 2. Imprimimos el Dashboard en la pantalla
    print("=============================================")
    print("    MONITOR DE ALMACENAMIENTO STRUCTIVA      ")
    print("=============================================")
    print(f"Fecha y Hora : {timestamp}")
    print(f"Espacio total: {uso.total / (1024**3):.2f} GB")
    print(f"Espacio usado: {uso.used / (1024**3):.2f} GB")
    print(f"Espacio libre: {uso.free / (1024**3):.2f} GB")
    
    # Cambiamos el color según el estado del disco
    if porcentaje_libre < umbral:
        print(f"Estado       : {ROJO}CRÍTICO - {porcentaje_libre:.2f}% libre{RESET}")
    elif porcentaje_libre < (umbral + 10):
        # Si está cerca del umbral avisa en amarillo
        print(f"Estado       : {AMARILLO}PRECAUCIÓN - {porcentaje_libre:.2f}% libre{RESET}")
    else:
        print(f"Estado       : {VERDE}ÓPTIMO - {porcentaje_libre:.2f}% libre{RESET}")
    print("=============================================\n")

    # 3. Lógica para guardar la alerta en el archivo de texto
    if porcentaje_libre < umbral:
        if not alerta_activa:
            alerta_activa = True
            
            # Preparamos el texto a guardar
            mensaje_log = (
                f"[{timestamp}] ALERTA CRÍTICA\n"
                f"El almacenamiento de Structiva ha caído por debajo del {umbral}%.\n"
                f"Espacio actual libre: {porcentaje_libre:.2f}%\n"
                f"---------------------------------------------------\n"
            )
            
            # Guardamos en modo "a" (append) para no sobreescribir alertas anteriores
            with open(archivo_alerta, "a") as f:
                f.write(mensaje_log)
                
            print(f"{ROJO}>> ¡NUEVA ALERTA ESCRITA EN EL ARCHIVO DE LOG! <<{RESET}")
        else:
            print(f"{ROJO}>> (El disco sigue lleno. Alerta ya notificada anteriormente) <<{RESET}")
    else:
        # Si el disco vuelve a tener espacio (borraron cosas), reseteamos la alerta
        alerta_activa = False
        print(f"{VERDE}>>  Monitorizando sistema sin incidencias  <<{RESET}")

    # Esperamos los segundos configurados antes de volver a comprobar
    time.sleep(intervalo)