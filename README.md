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