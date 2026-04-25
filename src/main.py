import socket
import time
import tkinter as Tk
import threading

from core.emisor import Emisor
from core.receptor import Receptor

from pathlib import Path
from tkinter import filedialog

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
            print("Conexion Exitosa!")

            while True:
                try:
                    socket_conectado, IP = servidor.accept()
                    unReceptor = Receptor(socket_conectado, IP, ruta)
                    unReceptor.iniciar_transferencia()

                except Exception as e:
                    print(f"Conexion finalizada por un error: {e}")

    except OSError as error:
        pass
            


def seleccionar_archivos():
    """
    Me da paja hacer la logica del autocompletado para la terminal
    de momento usaremos esto.
    """

    root = Tk.Tk()
    root.withdraw()
    ruta = filedialog.askopenfilename(title="Selecciona el archivo a enviar")
    return ruta

if __name__ == "__main__":
    puerto = 5000
    menu = True

    try:
        while menu:
            print("Seleccione las Opciones:")
            op = int(input("""
            0: Cerrar Programa
            1: Emisor
            2: Receptor
            """))

            if op == 1:
                archivo = seleccionar_archivos()
                ip = input("Ingrese la IP destino: ")
                unEmisor = Emisor(archivo,ip, puerto)
                unEmisor.iniciar_conexion()
            elif op == 2:
                try:
                    ruta = input("Ingrese la ruta destino: ")
                    ruta_real = Path(ruta).expanduser()
                    unHilo = threading.Thread(target=iniciar_servidor,daemon=True, args=(puerto,ruta_real))
                    unHilo.start()
                    time.sleep(0.5)
                    print("Esperando Conexiones...")
                    print("Use Ctrl + C para cerrar el servidor.")
                    menu = False
                    unHilo.join()
                except Exception as error:
                    print(f"Fallo al crear el hilo de ejecucion del servidor")
                except KeyboardInterrupt:
                    print("\nCerrando Servidor...")
            elif op == 0:
                print("Cerrando Programa...")
                break
            else:
                print("Ingrese una Opcion valida.")
                continue
    except KeyboardInterrupt:
        print("\nCerrando Programa...")
