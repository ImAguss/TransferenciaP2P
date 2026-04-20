import socket
import tkinter as Tk
import threading

from core.emisor import Emisor
from tkinter import filedialog
from pathlib import Path

def iniciar_servidor():
    unSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    unSocket.bind(('0.0.0.0',5000))
    unSocket.listen(5)

    while True:
        conexion, IP = unSocket.accept()
        mensaje = conexion.recv(1024)
        print(mensaje.decode('utf-8'))
        print(f"Conexion establecida con {IP}")

def seleccionar_archivos():
    root = Tk.Tk()
    root.withdraw()
    ruta = filedialog.askopenfilename(title="Selecciona el archivo a enviar")
    return ruta

if __name__ == "__main__":
    unHilo = threading.Thread(target=iniciar_servidor,daemon=True)
    unHilo.start()

        #ruta = seleccionar_archivos()
        #IP = input("Direccion IP\n")
    unEmisor = Emisor("nada","127.0.0.1")
    unEmisor.iniciar_conexion()