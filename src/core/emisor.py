import socket
import json
import struct

from pathlib import Path
from .utils.verificacion_archivos import VerificacionArchivos
from .utils.comprimir_descomprimir_archivos import Comprimir_Descomprimir_Archivos

class Emisor:

    def __init__(self, ruta, IP, puerto):
        self.__ruta = ruta
        self.__IP = IP
        self.__puerto = puerto
        self.__verificador = VerificacionArchivos()
        self.__zip = Comprimir_Descomprimir_Archivos()

    def iniciar_conexion(self):

        if not self.__ruta.is_file():
            self.__ruta = self.__zip.Comprimir(self.__ruta)


        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as emisor:
            try:
                emisor.connect((self.__IP,self.__puerto))
                print(f"Emisor conectado a la IP: {self.__IP}, en el puerto: {self.__puerto}")
                self.crear_enviar_header(emisor)
                self.enviar_datos(emisor)

            except Exception as error:
                print(f"Ocurrio un error al realizar la conexion con {self.__IP} en el puerto {self.__puerto}, error: {error}")
            finally:
                emisor.close()
                print("Conexion finalizada")

    def crear_enviar_header(self,emisor):
        archivo = Path(self.__ruta)
        print(self.__ruta)
        hashing_archivo = self.__verificador.GenerarHashArchivo(self.__ruta)
        info_archivo = {
            "nombre": archivo.name,
            "size/bytes": archivo.stat().st_size,
            "tipo": archivo.suffix,
            "hash": hashing_archivo
        }
        
        info = json.dumps(info_archivo, indent=4).encode('utf-8')
        tamaño_json = struct.pack("!I", len(info))
        emisor.sendall(tamaño_json)
        emisor.sendall(info)

    def enviar_datos(self, emisor):
        tamaño_chunk = 1024

        try:
            with open (self.__ruta, "rb") as archivo:
                while True:
                    chunk = archivo.read(tamaño_chunk)

                    if not chunk:
                        break

                    emisor.sendall(chunk)
        except Exception as error:
            print(f"No se pudo completar el envio por {error}")
        else:
            print("Envio del archivo completado con exito!")
                
