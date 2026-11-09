"""!
@file app.py
@brief API de gestión de alumnos "Sistema Alumnos" (actividad OCY1102).
"""
import os

from flask import Flask, jsonify, request

## Aplicación Flask principal.
app = Flask(__name__)

## Alumnos almacenados en memoria para el laboratorio.
ALUMNOS = [
    {"id": 1, "nombre": "Ana Pérez", "carrera": "Ingeniería en Informática", "promedio": 6.1},
    {"id": 2, "nombre": "Benjamín Rojas", "carrera": "Ingeniería en Ciberseguridad", "promedio": 5.4},
    {"id": 3, "nombre": "Camila Soto", "carrera": "Analista Programador", "promedio": 6.8},
]

# La versión la inyecta el pipeline (ver Jenkinsfile). Sirve para la trazabilidad.
## Versión que vincula la aplicación con el build y el commit de origen.
VERSION = os.environ.get("APP_VERSION", "dev")


@app.route('/hello')
def hello():
    """!
    @brief Saluda al nombre recibido en el parámetro de consulta name de la URL.
    @return Texto de saludo con código HTTP 200.
    """
    name = request.args.get('name')
    return f"Hello, {name}!"


@app.route('/health')
def health():
    """!
    @brief Comprueba que el proceso de la API responde.
    @return JSON con estado ok y código HTTP 200.
    """
    return jsonify({"estado": "ok"})


@app.route('/version')
def version():
    """!
    @brief Informa la versión inyectada por Jenkins mediante APP_VERSION.
    @return JSON con el nombre de la aplicación y su versión.
    """
    return jsonify({"aplicacion": "Sistema Alumnos", "version": VERSION})


@app.route('/alumnos')
def listar_alumnos():
    """!
    @brief Lista los alumnos guardados en memoria.
    @return Lista JSON de alumnos con código HTTP 200.
    """
    return jsonify(ALUMNOS)


@app.route('/alumnos/<int:alumno_id>')
def obtener_alumno(alumno_id):
    """!
    @brief Busca un alumno por su identificador.
    @param alumno_id Identificador entero del alumno.
    @return Alumno en JSON con código 200 o mensaje de error con código 404.
    """
    for alumno in ALUMNOS:
        if alumno["id"] == alumno_id:
            return jsonify(alumno)
    return jsonify({"error": "Alumno no encontrado"}), 404


@app.route('/alumnos', methods=['POST'])
def crear_alumno():
    """!
    @brief Crea un alumno a partir del cuerpo JSON de la solicitud.
    El nombre debe ser un texto no vacío y el promedio un número entre 1 y 7.
    La carrera es opcional. Los datos se conservan solo mientras vive el proceso.
    @return Alumno creado con código 201 o error de validación con código 400.
    """
    datos = request.get_json(silent=True) or {}
    if not isinstance(datos, dict):
        return jsonify({"error": "El cuerpo debe ser un objeto JSON"}), 400
    nombre = datos.get("nombre", "")
    nombre = nombre.strip() if isinstance(nombre, str) else ""
    promedio = datos.get("promedio")

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400
    if isinstance(promedio, bool) or not isinstance(promedio, (int, float)) or not 1.0 <= promedio <= 7.0:
        return jsonify({"error": "El 'promedio' debe ser un número entre 1.0 y 7.0"}), 400

    nuevo = {
        "id": max((a["id"] for a in ALUMNOS), default=0) + 1,
        "nombre": nombre,
        "carrera": str(datos.get("carrera", "Sin carrera")),
        "promedio": promedio,
    }
    ALUMNOS.append(nuevo)
    return jsonify(nuevo), 201


def main():
    """!
    @brief Inicia el servidor de desarrollo local sin depuración.
    @return Ninguno mientras el servidor permanece activo.
    """
    app.run(debug=False)


if __name__ == '__main__':
    main()
