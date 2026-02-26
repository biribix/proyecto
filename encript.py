import tkinter as tk
from tkinter import messagebox, filedialog
from cryptography.fernet import Fernet
from pathlib import Path

"""Hace que el botón copiar copie en el portapapeles la key"""
def copiar(ventana, contraseña):
    ventana.clipboard_clear()
    ventana.clipboard_append(contraseña)
    ventana.update()

"""Genera la key y crear una ventana para poder verla"""
def clave():
    # Genera la key y crea una ventana
    contraseña = Fernet.generate_key()
    ventana = tk.Toplevel()
    ventana.title("KEY")
    ventana.geometry("550x200")
    ventana.resizable(False, False)

    # Crea los botones, y debuelve la contraseña a la funcion seleccionar_e
    tk.Label(ventana, text="¡Guarda la key para poder desencriptar el archivo!", font=("Arial 15")).pack(pady=10)
    tk.Label(ventana, text=contraseña, font=("Arial 12")).pack(pady=10)
    tk.Button(ventana, text="Copiar", font=("Arial 20"), width=20, height=3, command=lambda: copiar(ventana, contraseña)).pack(pady=10)
    return contraseña

"""Encripta el archivo con la key creada anteriormente"""
def encriptar(ruta, contraseña):
    # Guarda el archivo bit a bit, guarda el contenido y lo encripta con la key ya creada
    ruta = Path(ruta)
    datos = ruta.read_bytes()
    clave = Fernet(contraseña)
    datos = clave.encrypt(datos)
    
    # Crea un nuevo archivo para dejar el original intacto y lo guarda en la misma ruta que el original
    nombre = ruta.stem + "_encriptado" + ruta.suffix
    guardar = ruta.parent / nombre

    # Escribe el texto encriptado en el archivo creado
    with open(guardar, "wb") as f:
        f.write(datos)  

"""Le da otra ventana a la interfaz grafica para poder introducir la key"""
def ingresar(ruta):
    # Crea una ventana con su titulo, su geometria y bloquea el redimensionamiento
    hola = tk.Toplevel()
    hola.title("key")
    hola.resizable(False, False)
    hola.geometry("350x200")

    # Crea y añade el texto de la ventana
    tk.Label(hola, text="Ingresa key:", font=("Arial 15")).pack(pady=10)

    # Pone una entrada de texto para poder poner la key
    texto = tk.Entry(hola, width=30, font=("Arial 12"))
    texto.pack(pady=10)
    
    # Pone un boton que lleva a la funcion confirmar
    tk.Button(hola, text="Ok", bg="white", font=("Arial 12"), width=15, height=2, command=lambda: confirmar(texto, ruta)).pack(pady = 20)

"""Confirma que la key introducida sea correcta"""
def confirmar(texto, ruta):
    # Recoje la key del Entry quitando los espacios en blanco del inicio y del final
    key = texto.get().strip()
    
    # Verifica que la key no sea erronea y si todo es correcto realiza la funcion desencriptar
    if key:
        desencriptar(ruta, key)
    else:
        messagebox.showinfo("ERROR", "la key no es valida buelva a intentarlo") 

"""Desencripta el archivo dado con la key proporcionada"""
def desencriptar(ruta, key):
    # Intenta hacer lo que hay dentro del try y si da un error realiza lo que hay en except
    try:
        # Guarda el archivo bit a bit, guarda el contenido y lo desencripta con la key ya creada
        ruta = Path(ruta)
        datos = ruta.read_bytes()
        clave = Fernet(key.encode())
        datos = clave.decrypt(datos)

        # Cambia el nombre quitandole _encriptado para ponerle _desencriptado, (si no lleva lo de _encriptado le pondra _desencriptado sin quitar nada)
        nombre = ruta.stem.replace("_encriptado", "_desencriptado") + ruta.suffix
        guardar = ruta.parent / nombre

        # Escribe el texto desencriptado en el archivo creado
        with open(guardar, "wb") as f:
            f.write(datos)

        # Elimina el archivo encriptado y notifica que se realizo todo
        ruta.unlink()
        messagebox.showinfo("Notificacion", "El archivo ({ruta}) se descodifico con exito")

    except Exception:
        messagebox.showerror("Error", "La key es incorrecta o el archivo no es válido")

"""Le da interfaz grafica a lo de seleccionar archivo y empieza el encriptado"""
def seleccionar_e():
    # te permite seleccionar solo archivos .txt
    ruta = filedialog.askopenfilename(
        title = "Seleccionar archivo para encripar",
        initialdir = "/",
        filetypes = [("Archivos de texto", "*.txt"),
            ("Archivos CAD/BIM", "*.dxf;*.dwt;*.rvt;*.rfa;*.max;*.skp;*.blend;*.c4d;*.ifc"),
            ("Imágenes", "*.png;*.jpg;*.jpeg;*.tiff;*.exr")]
        )
    
    # Verifica que ayas puesto algo en la ruta y si es asi realiza la funcion de encriptar
    if ruta:
        contraseña = clave()
        encriptar(ruta, contraseña)
        messagebox.showinfo("Notificacion", "El archivo (" + ruta + ") se codifico con exito")
    else:
        messagebox.showinfo("ERROR", "No se selecciono un archivo valido buelva a intentarlo")

"""Le da interfaz grafica a lo de seleccionar archivo y empieza el desencriptado"""
def seleccionar_d():
    ruta = filedialog.askopenfilename(
        title = "Seleccionar archivo para desencriptar",
        initialdir = "/",
        filetypes = [("Archivos de texto", "*.txt"),
            ("Archivos CAD/BIM", "*.dxf;*.dwt;*.rvt;*.rfa;*.max;*.skp;*.blend;*.c4d;*.ifc"),
            ("Imágenes", "*.png;*.jpg;*.jpeg;*.tiff;*.exr")]
        )
 
    # Verifica que ayas puesto algo en la ruta y si es asi realiza la funcion de ingresar
    if ruta:
        ingresar(ruta)
    else:
        messagebox.showinfo("ERROR", "No se selecciono un archivo valido buelva a intentar")

# Crea la interfaz grafica, pone una ventana con su titulo, su geometria y bloquea el redimensionamiento
menu = tk.Tk()
menu.title("Encriptador")
menu.geometry("350x250")
menu.resizable(False, False)

# Crea los botones y los añade
tk.Button(menu, text="Encriptar", bg="white", font=("Arial 20"), width=20, height=3, command = seleccionar_e).pack(pady = 5)
tk.Button(menu, text="Desencriptar", bg="white", font=("Arial 20"), width=20, height=3, command=seleccionar_d).pack(pady = 5)

menu.mainloop()

