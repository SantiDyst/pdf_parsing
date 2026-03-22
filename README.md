# 📄 PDF Parser Web App (Flask)

Una aplicación web ligera construida con Flask para extraer información estructurada (tablas y datos) de extractos bancarios en PDF y visualizarla en un formato HTML limpio.

## 🚀 Características Principales

*   **Interfaz Web Simple:** Sube archivos PDF directamente desde el navegador de forma intuitiva.
*   **Procesamiento en Memoria:** Convierte el PDF a Markdown y luego a HTML "al vuelo", sin generar archivos intermedios en el disco.
*   **Limpieza Automática:** El sistema elimina el PDF subido inmediatamente después de procesarlo para no consumir espacio en el servidor.
*   **Extracción de Datos Precisa:** Utiliza `docling` para mantener la estructura de las tablas originales y aplica limpieza con expresiones regulares (RegEx) para corregir formatos numéricos y notación científica.

## 🛠️ Tecnologías Utilizadas

*   **Backend:** Python 3, Flask, Werkzeug.
*   **Procesamiento de PDF:** Docling, PyPDF.
*   **Formatos:** Markdown a HTML.
*   **Frontend:** HTML5, CSS3 integrado.

## Pipeline de pdf_parsing

🧑‍💻 USUARIO (Navegador)
   │
   ├─ 1. Sube "archivo.pdf" y hace click en Procesar (POST Request)
   ▼
🌐 FLASK (app.py)
   │
   ├─ 2. Recibe "archivo.pdf" y lo guarda temporalmente en la carpeta /uploads
   ├─ 3. Llama a la función procesar_pdf(ruta)
   ▼
⚙️ BACKEND DE PROCESAMIENTO (main.py)
   │
   ├─ 4. Lee el PDF y lo divide en "chunks" de 10 páginas.
   ├─ 5. Docling procesa cada chunk en memoria.
   ├─ 6. Borra los chunks temporales del disco.
   ├─ 7. Une todo el texto y lo devuelve a Flask como un mega-texto Markdown.
   ▼
🌐 FLASK (app.py)
   │
   ├─ 8. Recibe el texto Markdown.
   ├─ 9. Llama a la función generar_html(texto_markdown).
   ├─ 10. Borra el "archivo.pdf" original de la carpeta /uploads.
   ▼
🎨 RENDERIZADO VISUAL
   │
   ├─ 11. Flask inyecta el HTML resultante adentro de "resultado.html"
   ├─ 12. Envía la página final de vuelta al usuario.
   ▼
🧑‍💻 USUARIO (Navegador)
   └─ 13. Ve la tabla perfecta en su pantalla. Fin del ciclo.


## 📂 Estructura del Proyecto

```text
pdf_parsing/
├── app.py                 # Servidor web y rutas de Flask
├── main.py                # Lógica de procesamiento (Docling/PyPDF)
├── requirements.txt       # Dependencias del proyecto
├── uploads/               # Carpeta temporal para subidas (se auto-limpia)
└── templates/
    ├── index.html         # Formulario de subida de PDF
    └── resultado.html     # Vista de la tabla procesada





