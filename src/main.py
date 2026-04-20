import socket
import time
import tkinter as Tk
import threading

from core.emisor import Emisor
from tkinter import filedialog
from pathlib import Path

def iniciar_servidor():
    """
    Esta funcion se encarga de hacer que la PC actue como servidor y que pueda recibir
    archivos, ya que sera usado con un hilo para quedar en ejecucion esperando una 
    conexion.

    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind(("0.0.0.0",5000))
            servidor.listen(5)
            print("Conexion Exitosa!")

            while True:
                try:
                    socket_conectado, IP = servidor.accept()
                    while True:
                        "Este bucle es para probar la logica del emisor"
                        archivo = socket_conectado.recv(1024)

                        if not archivo:
                            print("Datos enviados correctamente")
                            break

                        print(archivo.decode("utf-8"))
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

    try:
        unHilo = threading.Thread(target=iniciar_servidor,daemon=True)
        unHilo.start()
        time.sleep(0.5)
    except Exception as error:
        print(f"Fallo al crear el hilo de ejecucion del servidor")



    while True:
        print("Seleccione las Opciones:")
        op = int(input("""
        1: Emisor
        2: Receptor
        """))

        if op == 1:
            unEmisor = Emisor("nada","127.0.0.1", 5000)
            unEmisor.iniciar_conexion()
        if op == 2:
            print("Esperando Conexiones...")
            break

    unHilo.join()