import os
import bleach
import json
from flask import Flask, render_template, request, Response, stream_with_context
from werkzeug.utils import secure_filename

# Importamos las funciones actualizadas
from main import procesar_pdf, generar_html

app = Flask(__name__)

# [MEJORA] Límite de tamaño de archivo (16MB por defecto, ajustable)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# [MEJORA] Validación de extensiones permitidas
ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Asegurarse de que la carpeta uploads exista
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/procesar", methods=["POST"])
def procesar():
    archivo = request.files.get("pdf")
    
    if not archivo or archivo.filename == "" or not allowed_file(archivo.filename):
        return Response(json.dumps({"error": "Archivo no válido"}), status=400)

    nombre_archivo = secure_filename(archivo.filename)
    ruta_pdf = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)
    archivo.save(ruta_pdf)

    def generate():
        try:
            # Iteramos sobre el generador de progreso
            for mensaje in procesar_pdf(ruta_pdf):
                if mensaje.startswith("PROGRESS:"):
                    # Enviamos solo el texto del progreso
                    yield f"data: {json.dumps({'status': 'processing', 'msg': mensaje[9:]})}\n\n"
                
                elif mensaje.startswith("RESULT:"):
                    # Generamos el HTML final y lo enviamos
                    markdown_text = mensaje[7:]
                    html_raw = generar_html(markdown_text)
                    
                    # Sanear HTML
                    tags_permitidas = [
                        'h1', 'h2', 'h3', 'p', 'br', 'strong', 'em', 'u',
                        'table', 'thead', 'tbody', 'tr', 'th', 'td', 'ul', 'ol', 'li'
                    ]
                    html_sanitizado = bleach.clean(html_raw, tags=tags_permitidas)
                    
                    yield f"data: {json.dumps({'status': 'completed', 'html': html_sanitizado})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'status': 'error', 'msg': str(e)})}\n\n"
        
        finally:
            if os.path.exists(ruta_pdf):
                os.remove(ruta_pdf)

    return Response(stream_with_context(generate()), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)