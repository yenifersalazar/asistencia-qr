
from flask import Flask, render_template, request
from pathlib import Path
from datetime import datetime
from uuid import uuid4
from threading import Lock
from openpyxl import Workbook, load_workbook
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Directorio donde se encuentra app.py
BASE_DIR = Path(__file__).resolve().parent

# Cargar las variables del archivo .env
load_dotenv(BASE_DIR / ".env")

# Leer las variables de entorno exclusivamente desde .env
IP_LOCAL = os.environ["IP_LOCAL"]
PORT = int(os.environ["PORT"])

# Rutas de archivos
DATA_DIR = BASE_DIR / "data"
EXCEL_FILE = DATA_DIR / "asistencias.xlsx"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Evita escrituras simultáneas en Excel
excel_lock = Lock()


def preparar_excel():
    """Crea el archivo Excel y sus encabezados si no existe."""
    if not EXCEL_FILE.exists():
        with excel_lock:
            if not EXCEL_FILE.exists():
                libro = Workbook()
                hoja = libro.active
                hoja.title = "Asistencias"
                hoja.append([
                    "ID_Asistencia",
                    "Nombre",
                    "Apellido",
                    "Fecha",
                    "Hora"
                ])
                libro.save(EXCEL_FILE)
                libro.close()


@app.route("/", methods=["GET"])
def inicio():
    return render_template("asistencia.html")


@app.route("/registrar", methods=["POST"])
def registrar():
    nombre = request.form.get("nombre", "").strip()
    apellido = request.form.get("apellido", "").strip()

    # Validar campos obligatorios
    if not nombre or not apellido:
        return render_template(
            "asistencia.html",
            error="Por favor, escribe tu nombre y apellido.",
            nombre=nombre,
            apellido=apellido
        ), 400

    # Validar longitud
    if len(nombre) > 100 or len(apellido) > 100:
        return render_template(
            "asistencia.html",
            error="El nombre y el apellido no pueden superar 100 caracteres.",
            nombre=nombre,
            apellido=apellido
        ), 400

    ahora = datetime.now()
    id_asistencia = f"AST-{uuid4().hex[:12].upper()}"

    try:
        with excel_lock:
            preparar_excel()
            libro = load_workbook(EXCEL_FILE)

            try:
                hoja = libro["Asistencias"]
                hoja.append([
                    id_asistencia,
                    nombre,
                    apellido,
                    ahora.strftime("%Y-%m-%d"),
                    ahora.strftime("%H:%M:%S")
                ])
                libro.save(EXCEL_FILE)
            finally:
                libro.close()

    except PermissionError:
        return render_template(
            "asistencia.html",
            error=(
                "No se pudo guardar el Excel. Cierra el archivo "
                "asistencias.xlsx si está abierto e inténtalo de nuevo."
            ),
            nombre=nombre,
            apellido=apellido
        ), 500

    except Exception:
        app.logger.exception("Error al guardar una asistencia")
        return render_template(
            "asistencia.html",
            error="Ocurrió un error al guardar la asistencia. Inténtalo de nuevo.",
            nombre=nombre,
            apellido=apellido
        ), 500

    return render_template(
        "confirmacion.html",
        id_asistencia=id_asistencia,
        nombre=nombre
    )


@app.route("/qr", methods=["GET"])
def mostrar_qr():
    return render_template("qr.html")


if __name__ == "__main__":
    preparar_excel()

    print(f"Servidor disponible en http://{IP_LOCAL}:{PORT}")

    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False
    )