import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# Importamos las funciones actualizadas
from main import procesar_pdf, generar_html

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Asegurarse de que la carpeta uploads exista
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        archivo = request.files.get("pdf")

        if archivo and archivo.filename != "":
            try:
                nombre_archivo = secure_filename(archivo.filename)
                ruta_pdf = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)
                archivo.save(ruta_pdf)

                # 1. Procesar PDF y obtener Markdown en memoria
                markdown_text = procesar_pdf(ruta_pdf)
                
                # 2. Convertir Markdown a HTML puro
                html_result = generar_html(markdown_text)

                # 3. Eliminar el PDF subido por seguridad y limpieza
                if os.path.exists(ruta_pdf):
                    os.remove(ruta_pdf)

                # 4. Renderizar la nueva plantilla con el resultado
                return render_template("resultado.html", contenido_html=html_result)

            except Exception as e:
                error = f"Ocurrió un error al procesar el archivo: {str(e)}"
        else:
            error = "Por favor, selecciona un archivo PDF válido."

    return render_template("index.html", error=error)

if __name__ == "__main__":
    app.run(debug=True)