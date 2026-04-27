import hashlib

class VerificacionArchivos:
    hashing = hashlib.sha256()

    def GenerarHashArchivo(self, ruta):
        """
        Calcula el hash descomprimiendo el archivo en pedazos para poder
        ir actualizando el hash con update.
        """

        tamanio_chunk = 4096
        
        with open(ruta, "rb") as archivo:
            while True:
                chunk = archivo.read(tamanio_chunk)
                if not chunk:
                    break
                self.__hashing.update(chunk)

        # Retorna el valor en Hexadecimal
        return hashing.hexdigest()
