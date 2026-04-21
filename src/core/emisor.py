import socket
import json
import struct

from pathlib import Path

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
                archivo = Path(self.__ruta)
                info_archivo = {
                    "nombre": archivo.name,
                    "tamaño": archivo.stat().st_size,
                    "tipo": archivo.suffix
                }
                
                info = json.dumps(info_archivo, indent=4).encode('utf-8')
                tamaño_json = struct.pack("!I", len(info))
                emisor.sendall(tamaño_json)
                emisor.sendall(info)

            except Exception as error:
                print(f"Ocurrio un error al realizar la conexion con {self.__IP} en el puerto {self.__puerto}, error: {error}")
            finally:
                emisor.close()
                print("Conexion finalizada")