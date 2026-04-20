import socket

class Emisor:

    def __init__(self, ruta, IP):
        self.__ruta = ruta
        self.__IP = IP

    def iniciar_conexion(self):
        socket_emisor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_emisor.connect((self.__IP,5000))
        socket_emisor.send(b"Pene")
        socket_emisor.close()