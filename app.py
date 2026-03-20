import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# Importamos tus funciones (vas a reutilizar tu script unificado)
from main import procesar_pdf, generar_html

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ruta principal
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        archivo = request.files["pdf"]

        if archivo:
            nombre_archivo = secure_filename(archivo.filename)
            ruta_pdf = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)
            archivo.save(ruta_pdf)

            # Procesar PDF
            procesar_pdf(ruta_pdf)
            generar_html()

            return render_template("index.html", resultado=True)

    return render_template("index.html", resultado=False)

if __name__ == "__main__":
    app.run(debug=True)