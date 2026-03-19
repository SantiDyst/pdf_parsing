import os
from pypdf import PdfReader, PdfWriter
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

archivo_entrada = "entradas/test.pdf"
archivo_salida = "resultado_final.md"
paginas_por_chunk = 10  # Cortamos de a 10 páginas para cuidar tu RAM

print(f"--- Iniciando procesamiento por lotes de {archivo_entrada} ---")

try:
    # 1. Configuramos Docling (sin OCR para que sea rápido)
    opciones = PdfPipelineOptions()
    opciones.do_ocr = False
    opciones.generate_page_images = False

    converter = DocumentConverter(
        allowed_formats=[InputFormat.PDF],
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opciones)}
    )

    # 2. Leemos el PDF original para saber cuántas páginas tiene
    reader = PdfReader(archivo_entrada)
    total_paginas = len(reader.pages)
    print(f"Total de páginas detectadas: {total_paginas}")

    # Vaciamos el archivo de salida si ya existía
    open(archivo_salida, 'w', encoding='utf-8').close()

    # 3. Empezamos a cortar y procesar
    for i in range(0, total_paginas, paginas_por_chunk):
        fin = min(i + paginas_por_chunk, total_paginas)
        print(f"\nProcesando páginas de la {i+1} a la {fin}...")
        
        # Creamos un PDF temporal chiquito
        writer = PdfWriter()
        for j in range(i, fin):
            writer.add_page(reader.pages[j])
            
        pdf_temp = f"temp_chunk_{i}.pdf"
        with open(pdf_temp, "wb") as f_temp:
            writer.write(f_temp)

        # 4. Docling procesa solo el pedacito
        try:
            resultado = converter.convert(pdf_temp)
            texto_md = resultado.document.export_to_markdown()
            
            # Agregamos el texto al Markdown final
            with open(archivo_salida, "a", encoding="utf-8") as f_out:
                f_out.write(texto_md + "\n\n")
            print("Chunk procesado y guardado con éxito.")
            
        except Exception as e_docling:
            print(f"Error al procesar el chunk {i}: {e_docling}")
            
        # 5. Borramos el archivo temporal para limpiar
        if os.path.exists(pdf_temp):
            os.remove(pdf_temp)

    print(f"\n--- ¡Proceso completado al 100%! Revisá {archivo_salida} ---")

except Exception as e:
    print(f"Error general: {e}")