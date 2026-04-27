import hashlib

class VerificacionArchivos:

    def GenerarHashArchivo(self, ruta):
        """
        Calcula el hash del archivo en pedazos para poder
        ir actualizando el hash con update.
        """
        hashing = hashlib.sha256()
        tamanio_chunk = 4096
        
        with open(ruta, "rb") as archivo:
            while True:
                chunk = archivo.read(tamanio_chunk)
                if not chunk:
                    break
                hashing.update(chunk)

        # Retorna el valor en Hexadecimal
        return hashing.hexdigest()
