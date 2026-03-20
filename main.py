import os
import re
import markdown
import webbrowser
from pypdf import PdfReader, PdfWriter
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

# =========================
# CONFIG
# =========================
""" ARCHIVO_ENTRADA = "entradas/test.pdf" """
ARCHIVO_MD = "resultado_final.md"
ARCHIVO_HTML = "reporte_limpio.html"
PAGINAS_POR_CHUNK = 10

# =========================
# LIMPIEZA NUMÉRICA
# =========================
def limpiar_notacion_cientifica(texto):
    patron = r'[-+]?\d*\.\d+[eE][-+]?\d+'

    def formatear(match):
        numero = float(match.group())
        texto_num = f"{numero:,.2f}"
        texto_num = texto_num.replace(',', 'X').replace('.', ',').replace('X', '.')
        return texto_num

    return re.sub(patron, formatear, texto)

# =========================
# PROCESAR PDF → MD
# =========================
def procesar_pdf(ruta_pdf):
    print(f"--- Procesando PDF: {ARCHIVO_ENTRADA} ---")

    opciones = PdfPipelineOptions()
    opciones.do_ocr = False
    opciones.generate_page_images = False

    converter = DocumentConverter(
        allowed_formats=[InputFormat.PDF],
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opciones)}
    )

    reader = PdfReader(ruta_pdf)
    total_paginas = len(reader.pages)

    print(f"Total páginas: {total_paginas}")

    open(ARCHIVO_MD, 'w', encoding='utf-8').close()

    for i in range(0, total_paginas, PAGINAS_POR_CHUNK):
        fin = min(i + PAGINAS_POR_CHUNK, total_paginas)
        print(f"Procesando páginas {i+1} a {fin}")

        writer = PdfWriter()
        for j in range(i, fin):
            writer.add_page(reader.pages[j])

        pdf_temp = f"temp_{i}.pdf"

        with open(pdf_temp, "wb") as f:
            writer.write(f)

        try:
            resultado = converter.convert(pdf_temp)
            texto_md = resultado.document.export_to_markdown()

            with open(ARCHIVO_MD, "a", encoding="utf-8") as f_out:
                f_out.write(texto_md + "\n\n")

        except Exception as e:
            print(f"Error en chunk {i}: {e}")

        if os.path.exists(pdf_temp):
            os.remove(pdf_temp)

    print("--- PDF procesado correctamente ---")

# =========================
# GENERAR HTML
# =========================
def generar_html():
    print("--- Generando HTML ---")

    CSS = """
    <style>
    body { font-family: 'Segoe UI'; background:#f4f4f9; padding:20px; }
    .container { background:white; padding:40px; border-radius:8px; max-width:1000px; margin:auto; }
    table { width:100%; border-collapse: collapse; }
    th { background:#2c3e50; color:white; padding:10px; }
    td { padding:8px; border:1px solid #ddd; text-align:right; }
    </style>
    """

    with open(ARCHIVO_MD, "r", encoding="utf-8") as f:
        contenido = f.read()

    contenido = limpiar_notacion_cientifica(contenido)
    html = markdown.markdown(contenido, extensions=['tables'])

    pagina = f"""
    <html>
    <head>{CSS}</head>
    <body><div class="container">{html}</div></body>
    </html>
    """

    with open(ARCHIVO_HTML, "w", encoding="utf-8") as f:
        f.write(pagina)

    ruta = os.path.abspath(ARCHIVO_HTML)
    webbrowser.open(f"file:///{ruta}")

    print("--- HTML generado y abierto ---")

# =========================
# MAIN
# =========================
def main():
    procesar_pdf()
    generar_html()
    print("🚀 Proceso completo finalizado")

if __name__ == "__main__":
    main()