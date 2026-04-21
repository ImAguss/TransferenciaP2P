import struct
import json
import socket

from pathlib import Path

class Receptor:

    def __init__(self, emisor, IP, ruta):
        self.__emisor = emisor
        self.__IP = IP
        self.__ruta = ruta

    def iniciar_transferencia(self):
        tamaño_json = self.__emisor.recv(4)
        tamaño_header, = struct.unpack("!I",tamaño_json)

        header = self.__emisor.recv(tamaño_header).decode('utf-8')
        if header:
            print("Header Recibido!")
            header_json = json.loads(header)
            op = input(f"Desea recibir el archivo con la siguiente informacion: {header}? S/N\n")

            if op.upper() == 'S':
                self.recibir_archivo(header_json)
            if op.upper() == 'N':
                raise Exception

    def recibir_archivo(self, header):
        tamaño_chunk = 1024
        tamaño_archivo = header["size/bytes"]
        nombre_archivo = header["nombre"]
        bytes_recibidos = 0
        ruta = self.__ruta / nombre_archivo

        try:
            with open(ruta, "wb") as archivo_recibido:
                while bytes_recibidos < tamaño_archivo:
                    bytes_faltantes = tamaño_archivo - bytes_recibidos
                    chunk = self.__emisor.recv(min(tamaño_chunk,bytes_faltantes))

                    if not chunk:
                        break

                    archivo_recibido.write(chunk)
                    bytes_recibidos += len(chunk)

        except Exception as error:
            print(f"No se pudo recibir el archivo por: {error}")
        else:
            print(f"Archivo recibido! en {self.__ruta}")