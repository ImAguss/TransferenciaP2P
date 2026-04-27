import socket
import time
import threading
import os
import readline
import glob

from core.emisor import Emisor
from core.receptor import Receptor

from pathlib import Path
from tkinter import filedialog

ruta = Path("~/Descargas/")

def iniciar_servidor(puerto:int, ruta):
    """
    Esta funcion se encarga de hacer que la PC actue como servidor y que pueda recibir
    archivos, ya que sera usado con un hilo para quedar en ejecucion esperando una 
    conexion.

    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024*1024)
            servidor.bind(("0.0.0.0",puerto))
            servidor.listen(5)
            print("Esperando por archivos...")

            while True:
                try:
                    socket_conectado, IP = servidor.accept()
                    unReceptor = Receptor(socket_conectado, IP, ruta)
                    unReceptor.iniciar_transferencia()

                except Exception as e:
                    print(f"Conexion finalizada por un error: {e}")

    except OSError as error:
        pass
            
def autocompletar_rutas(texto, estado):
    texto = os.path.expanduser(texto)
    if os.path.isdir(texto) and not texto.endswith(os.sep):
        coincidencias = glob.glob(texto + os.sep + '*')
    else:
        coincidencias = glob.glob(texto + '*')
        coincidencias = [c + os.sep if os.path.isdir(c) else c for c in coincidencias]

    try:
        return coincidencias[estado]
    except IndexError:
        return None

def seleccionar_archivos(solo_carpetas=False):
    readline.set_completer_delims(' \t\n; ')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(autocompletar_rutas)

    ruta = Path(input("Ingrese la ruta del archivo/carpeta a enviar: ")).expanduser()

    if solo_carpetas and ruta.is_file():
        print("Ingrese una carpeta, no un archivo.")
    else:
        return ruta

def menu():
    try:
        while True:
            print("Seleccione las Opciones:")
            op = int(input("""
            1: Enviar Archivo.
            2: Especificar Ruta Destino, Por defecto: Descargas.
            3: Esperar Archivos.
            """))

            if op == 1:
                archivo = seleccionar_archivos()
                ip = input("Ingrese la IP destino: ")
                unEmisor = Emisor(archivo,ip, puerto)
                unEmisor.iniciar_conexion()
            elif op == 2:
                ruta = seleccionar_archivos(solo_carpetas=False)
            elif op == 3:
                break
            else:
                print("Ingrese una Opcion valida.")
                continue
    except KeyboardInterrupt:
        print("\nCerrando Menu...")

if __name__ == "__main__":
    puerto = 5000

    menu()

    try:
        unHilo = threading.Thread(target=iniciar_servidor,daemon=True, args=(puerto,ruta))
        unHilo.start()
        time.sleep(0.5)
        unHilo.join()
    except Exception as error:
        print(f"Fallo al crear el hilo de ejecucion del servidor")
    except KeyboardInterrupt:
        print("\nCerrando Programa...")

