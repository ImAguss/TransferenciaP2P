import socket

class Emisor:

    def __init__(self, ruta, IP, puerto):
        self.__ruta = ruta
        self.__IP = IP
        self.__puerto = puerto

    def iniciar_conexion(self):
        socket_emisor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as emisor:
            try:
                emisor.connect((self.__IP,self.__puerto))
                print(f"Emisor conectado a la IP: {self.__IP}, en el puerto: {self.__puerto}")

                print("Enviando Datos...")
                emisor.sendall(b"Hola mundo")

            except Exception as error:
                print(f"Ocurrio un error al realizar la conexion con {self.__IP} en el puerto {self.__puerto}, error: {error}")
            finally:
                emisor.close()
                print("Conexion finalizada")