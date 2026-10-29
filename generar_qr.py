
import qrcode
from pathlib import Path
from dotenv import load_dotenv
import os

# Directorio donde se encuentra este archivo
BASE_DIR = Path(__file__).resolve().parent

# Cargar las variables del archivo .env
load_dotenv(BASE_DIR / ".env")

# Leer las variables de entorno
IP_LOCAL = os.environ["IP_LOCAL"]
PORT = int(os.environ["PORT"])

# Construir la dirección del formulario
direccion = f"http://{IP_LOCAL}:{PORT}/"

# Generar el código QR
qr = qrcode.make(direccion)

# Crear la carpeta static si no existe
carpeta = BASE_DIR / "static"
carpeta.mkdir(parents=True, exist_ok=True)

# Guardar la imagen del QR
qr.save(carpeta / "codigo_qr.png")

print("QR generado correctamente.")
print("Dirección del formulario:", direccion)
print("Imagen guardada en:", carpeta / "codigo_qr.png")
