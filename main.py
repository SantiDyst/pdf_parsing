import os
import re
import uuid
import markdown
from pypdf import PdfReader, PdfWriter
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

# =========================
# CONFIG
# =========================
PAGINAS_POR_CHUNK = 10

# Inicialización global del convertidor para evitar recargas ineficientes
opciones = PdfPipelineOptions()
opciones.do_ocr = False
opciones.generate_page_images = False

converter = DocumentConverter(
    allowed_formats=[InputFormat.PDF],
    format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opciones)}
)

# =========================
# LIMPIEZA NUMÉRICA
# =========================
def limpiar_notacion_cientifica(texto):
    # Patrón refinado para capturar notación científica de forma más robusta
    patron = r'[-+]?(?:\d+\.?\d*|\.\d+)[eE][-+]?\d+'

    def formatear(match):
        try:
            numero = float(match.group())
            # Formatear a 2 decimales con separador de miles '.' y decimal ','
            texto_num = f"{numero:,.2f}"
            texto_num = texto_num.replace(',', 'X').replace('.', ',').replace('X', '.')
            return texto_num
        except (ValueError, TypeError):
            return match.group()

    return re.sub(patron, formatear, texto)

# =========================
# PROCESAR PDF → Generador de progreso
# =========================
def procesar_pdf(ruta_pdf):
    yield f"PROGRESS:Iniciando procesamiento de {os.path.basename(ruta_pdf)}..."

    reader = PdfReader(ruta_pdf)
    total_paginas = len(reader.pages)
    yield f"PROGRESS:Total de páginas detectadas: {total_paginas}"

    # Variable en memoria para acumular el Markdown
    texto_md_completo = ""

    for i in range(0, total_paginas, PAGINAS_POR_CHUNK):
        fin = min(i + PAGINAS_POR_CHUNK, total_paginas)
        yield f"PROGRESS:Procesando bloque: páginas {i+1} a {fin}..."

        writer = PdfWriter()
        for j in range(i, fin):
            writer.add_page(reader.pages[j])

        id_unico = uuid.uuid4().hex
        pdf_temp = f"temp_{id_unico}_{i}.pdf"

        try:
            with open(pdf_temp, "wb") as f:
                writer.write(f)

            resultado = converter.convert(pdf_temp)
            texto_md = resultado.document.export_to_markdown()
            texto_md_completo += texto_md + "\n\n"

        except Exception as e:
            yield f"PROGRESS:Error en bloque {i+1}-{fin}: {str(e)}"
            raise e
        
        finally:
            if os.path.exists(pdf_temp):
                os.remove(pdf_temp)

    yield f"RESULT:{texto_md_completo}"

# =========================
# GENERAR HTML → Retorna String HTML
# =========================
def generar_html(contenido_md):
    print("--- Generando HTML en memoria ---")

    contenido = limpiar_notacion_cientifica(contenido_md)
    # Convertimos a HTML y lo retornamos
    html = markdown.markdown(contenido, extensions=['tables'])
    return html