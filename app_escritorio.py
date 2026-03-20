import tkinter as tk
from tkinter import filedialog, messagebox
import os
import webbrowser

# Importamos tu lógica de procesamiento
from main import procesar_pdf, generar_html

# Variables globales para guardar la ruta
ruta_pdf_seleccionado = ""

def seleccionar_pdf():
    global ruta_pdf_seleccionado
    # Abre la ventana de Windows para elegir archivo
    ruta = filedialog.askopenfilename(
        title="Seleccionar Extracto PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    
    if ruta:
        ruta_pdf_seleccionado = ruta
        # Actualizamos la interfaz
        lbl_ruta.config(text="..." + ruta[-40:]) # Muestra el final de la ruta
        btn_procesar.config(state=tk.NORMAL) # Habilita el botón de procesar
        lbl_estado.config(text="Archivo cargado. Listo para procesar.", fg="black")

def procesar():
    global ruta_pdf_seleccionado
    
    # Cambiamos el estado visual para que el usuario sepa que está trabajando
    lbl_estado.config(text="Procesando... Por favor espera (puede tardar unos segundos).", fg="blue")
    ventana.update() # Fuerza a la interfaz a actualizar el texto inmediatamente

    try:
        # 1. Procesamos el PDF (tu función de main.py)
        markdown_text = procesar_pdf(ruta_pdf_seleccionado)
        
        # 2. Generamos el código HTML (tu función de main.py)
        html_result = generar_html(markdown_text)
        
        # 3. Guardamos el HTML en un archivo temporal en la misma carpeta
        ruta_html = os.path.abspath("reporte_generado.html")
        with open(ruta_html, "w", encoding="utf-8") as f:
            f.write(html_result)
        
        # 4. Abrimos el resultado en el navegador por defecto
        webbrowser.open(f"file:///{ruta_html}")
        
        # Restauramos la interfaz
        lbl_estado.config(text="¡Procesado con éxito! Revisa tu navegador.", fg="green")
        btn_procesar.config(state=tk.DISABLED)
        lbl_ruta.config(text="Ningún archivo seleccionado")
        ruta_pdf_seleccionado = ""
        
    except Exception as e:
        messagebox.showerror("Error de Procesamiento", f"Ocurrió un error:\n{str(e)}")
        lbl_estado.config(text="Error durante el proceso.", fg="red")

# =========================
# CONFIGURACIÓN DE LA VENTANA (UI)
# =========================
ventana = tk.Tk()
ventana.title("PDF Parser - Herramienta de Procesamiento")
ventana.geometry("450x250")
ventana.resizable(False, False) # Evita que cambien el tamaño de la ventana

# Centrar la ventana en la pantalla
ventana.eval('tk::PlaceWindow . center')

# Título
titulo = tk.Label(ventana, text="Procesador de Extractos", font=("Segoe UI", 16, "bold"))
titulo.pack(pady=15)

# Botón Subir
btn_subir = tk.Button(ventana, text="📁 Subir PDF", command=seleccionar_pdf, font=("Segoe UI", 11), width=20)
btn_subir.pack(pady=5)

# Etiqueta de la ruta
lbl_ruta = tk.Label(ventana, text="Ningún archivo seleccionado", fg="gray", font=("Segoe UI", 9))
lbl_ruta.pack(pady=5)

# Botón Procesar (Inicia deshabilitado hasta que se suba un PDF)
btn_procesar = tk.Button(ventana, text="⚙️ Procesar Documento", command=procesar, font=("Segoe UI", 11, "bold"), bg="#2ecc71", fg="white", width=20, state=tk.DISABLED)
btn_procesar.pack(pady=10)

# Etiqueta de estado
lbl_estado = tk.Label(ventana, text="", font=("Segoe UI", 10))
lbl_estado.pack(pady=5)

# Iniciar la aplicación
if __name__ == "__main__":
    ventana.mainloop()