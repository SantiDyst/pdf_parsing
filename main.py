import os
import re
import markdown
from pypdf import PdfReader, PdfWriter
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

# =========================
# CONFIG
# =========================
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
# PROCESAR PDF → Retorna MD
# =========================
def procesar_pdf(ruta_pdf):
    print(f"--- Procesando PDF: {ruta_pdf} ---")

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

    # Variable en memoria para acumular el Markdown
    texto_md_completo = ""

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
            # Acumulamos el texto en la variable
            texto_md_completo += texto_md + "\n\n"

        except Exception as e:
            print(f"Error en chunk {i}: {e}")

        if os.path.exists(pdf_temp):
            os.remove(pdf_temp)

    print("--- PDF procesado correctamente ---")
    return texto_md_completo

# =========================
# GENERAR HTML → Retorna String HTML
# =========================
def generar_html(contenido_md):
    print("--- Generando HTML en memoria ---")

    contenido = limpiar_notacion_cientifica(contenido_md)
    # Convertimos a HTML y lo retornamos
    html = markdown.markdown(contenido, extensions=['tables'])
    return html