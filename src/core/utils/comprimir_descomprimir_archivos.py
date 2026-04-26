import zipfile

from pathlib import Path

class Comprimir_Descomprimir_Archivos:
    def __init__(self, nivel_compresion=None):
        self.__nivel_compresion = nivel_compresion

    def Comprimir(self, ruta):
        ruta_path = Path(ruta)
        ruta_absoluta = Path(ruta)
        ruta_zip = Path(str(ruta_path) + ".zip")

        with zipfile.ZipFile(ruta_zip, 'w', compression=zipfile.ZIP_DEFLATED) as carpeta_comprimida:
            for archivo in ruta_absoluta.rglob('*'):
                if archivo.is_file():
                    ruta_relativa = archivo.relative_to(ruta)
                    carpeta_comprimida.write(archivo, arcname=ruta_relativa)

        print(ruta_zip)
        return ruta_zip

    def Descomprimir(self, ruta_carpeta_comprimida, ruta_destino):
        with zipfile.ZipFile(ruta_carpeta_comprimida,'r') as carpeta_descomprimida:
            carpeta_descomprimida.extractall(ruta_destino)

