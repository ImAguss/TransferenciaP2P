import struct
import socket

from pathlib import Path

class Receptor:

    def __init__(self, emisor, IP):
        self.__emisor = emisor
        self.__IP = IP

    def iniciar_transferencia(self):
        datos = self.__emisor.recv(4)
        tamaño, = struct.unpack("!I",datos)

        header = self.__emisor.recv(tamaño).decode('utf-8')
        if header:
            print("Datos recibidos!")
            print(header)