import socket
import threading
import time
import os
from pathlib import Path
from src.core.emisor import Emisor
from src.core.receptor import Receptor

# 1. Creamos un archivo de prueba
ruta_origen = Path("mensaje_secreto.txt")
with open(ruta_origen, "w") as f:
    f.write("¡Hola! Este es un mensaje secreto enviado a traves de P2P.\n" * 100) # Un archivo con algo de peso

ruta_destino_dir = Path("carpeta_destino_prueba")
ruta_destino_dir.mkdir(exist_ok=True)

puerto_prueba = 5005

# 2. Creamos una versión "modificada" del Receptor que acepta la transferencia automáticamente para la prueba
class ReceptorTest(Receptor):
    def iniciar_transferencia(self):
        import struct, json
        tamaño_json = self._Receptor__emisor.recv(4)
        tamaño_header, = struct.unpack("!I",tamaño_json)

        header = self._Receptor__emisor.recv(tamaño_header).decode('utf-8')
        if header:
            print(f"[RECEPTOR] Header Recibido de forma automatica:\n{header}")
            header_json = json.loads(header)
            # Aceptamos directamente sin preguntar S/N
            self.recibir_archivo(header_json)

# 3. Función para levantar el servidor
def servidor_mock():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind(("127.0.0.1", puerto_prueba))
        servidor.listen(1)
        print("[RECEPTOR] Servidor escuchando en el puerto", puerto_prueba)
        
        socket_conectado, IP = servidor.accept()
        print(f"[RECEPTOR] Conexion entrante desde {IP}")
        unReceptor = ReceptorTest(socket_conectado, IP, ruta_destino_dir)
        unReceptor.iniciar_transferencia()

# 4. Levantamos el servidor en un hilo
hilo_servidor = threading.Thread(target=servidor_mock, daemon=True)
hilo_servidor.start()
time.sleep(1) # Le damos 1 segundo al servidor para que levante

# 5. Iniciamos el Emisor
print(f"[EMISOR] Iniciando conexion para enviar: {ruta_origen.name}")
unEmisor = Emisor(ruta_origen, "127.0.0.1", puerto_prueba)
unEmisor.iniciar_conexion()

# Damos tiempo para que termine la transferencia
time.sleep(1)

# 6. Comprobamos que el archivo llegó correctamente
ruta_final = ruta_destino_dir / ruta_origen.name
if ruta_final.exists():
    print(f"\n✅ ¡ÉXITO! El archivo fue recibido en: {ruta_final}")
    print(f"✅ Tamaño original: {ruta_origen.stat().st_size} bytes")
    print(f"✅ Tamaño recibido: {ruta_final.stat().st_size} bytes")
else:
    print("\n❌ Falló la transferencia, el archivo no existe en el destino.")

# Limpieza (opcional, lo dejamos para que lo veas)
# os.remove(ruta_origen)
