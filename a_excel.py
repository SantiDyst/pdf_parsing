import pandas as pd
import markdown
from io import StringIO

inp = "resultado_final.md"
out = "datos.xlsx"

print(f"--- Unificando tablas de {inp} a Excel ---")

try:
    with open(inp, "r", encoding="utf-8") as f:
        contenido_md = f.read()

    # Convertimos Markdown a HTML internamente para que Pandas lo lea
    html_interno = markdown.markdown(contenido_md, extensions=['tables'])
    tablas = pd.read_html(StringIO(html_interno))

    if not tablas:
        print("No se encontraron tablas en el archivo.")
    else:
        # TRUCO: Apilamos todas las tablas en un solo DataFrame continuo
        df_combinado = pd.concat(tablas, ignore_index=True)
        
        # Limpieza rápida: borramos filas totalmente vacías
        df_combinado.dropna(how='all', inplace=True) 
        
        # Guardamos en un Excel con una sola hoja
        df_combinado.to_excel(out, sheet_name="Datos_Completos", index=False)
        
        print(f"--- ¡Éxito! Archivo '{out}' creado con 1 sola hoja y {len(df_combinado)} filas en total ---")

except Exception as e:
    print(f"Error: {e}")