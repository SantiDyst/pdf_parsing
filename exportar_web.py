import os
import markdown
import webbrowser
import re

# Archivos de entrada y salida
archivo_md = "resultado_final.md"
archivo_html = "reporte_limpio.html"

# CSS para el diseño
CSS = """
<style>
    body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f4f9; color: #333; padding: 20px; }
    .container { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 1000px; margin: auto; }
    h1, h2, h3 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin-top: 30px; }
    table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 13px; }
    th { background-color: #2c3e50; color: white; border: 1px solid #dee2e6; padding: 12px; text-align: left; }
    td { border: 1px solid #dee2e6; padding: 10px; text-align: right; /* Alineamos números a la derecha */ }
    tr:nth-child(even) { background-color: #f9f9f9; }
    tr:hover { background-color: #f1f1f1; }
    blockquote { border-left: 4px solid #ccc; margin: 1.5em 10px; padding: 0.5em 10px; background-color: #fdfdfd; }
</style>
"""

def limpiar_notacion_cientifica(texto):
    """
    Busca números como -4.59353e+06 y los convierte a formato -4.593.530,00
    """
    # Patrón para detectar notación científica
    patron = r'[-+]?\d*\.\d+[eE][-+]?\d+'
    
    def formatear(match):
        numero = float(match.group())
        # Formateamos con 2 decimales y separador de miles gringo (1,000,000.00)
        texto_num = f"{numero:,.2f}"
        # Lo traducimos al formato argentino (1.000.000,00)
        texto_num = texto_num.replace(',', 'X').replace('.', ',').replace('X', '.')
        return texto_num

    return re.sub(patron, formatear, texto)

print(f"--- Generando reporte visual y limpiando números... ---")

try:
    with open(archivo_md, "r", encoding="utf-8") as f:
        contenido_md = f.read()

    # 1. PASO MÁGICO: Limpiamos los números rotos antes de hacer nada
    contenido_limpio = limpiar_notacion_cientifica(contenido_md)

    # 2. Convertimos a HTML
    html_tablas = markdown.markdown(contenido_limpio, extensions=['tables'])

    # 3. Ensamblamos la página
    pagina_completa = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Reporte Documental Extraído</title>
        {CSS}
    </head>
    <body>
        <div class="container">
            {html_tablas}
        </div>
    </body>
    </html>
    """

    # 4. Guardamos y abrimos
    ruta_absoluta = os.path.abspath(archivo_html)
    with open(ruta_absoluta, "w", encoding="utf-8") as f:
        f.write(pagina_completa)
        
    print("--- ¡Listo! Abriendo el reporte corregido en tu navegador... ---")
    webbrowser.open(f"file:///{ruta_absoluta}")

except Exception as e:
    print(f"Error: {e}")