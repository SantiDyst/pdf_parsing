from flask import Flask, render_template_string
import markdown

app = Flask(__name__)

# CSS mejorado para que parezca un reporte profesional (como el PDF)
CSS = """
<style>
    body { font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; padding: 40px; }
    .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 1200px; margin: auto; }
    
    /* Estilo para que la tabla sea idéntica a la del PDF */
    table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 12px; }
    th { background-color: #f8f9fa; color: #333; font-weight: bold; border: 1px solid #dee2e6; padding: 10px; text-align: center; }
    td { border: 1px solid #dee2e6; padding: 8px; text-align: left; }
    tr:nth-child(even) { background-color: #f9f9f9; }
    tr:hover { background-color: #f1f1f1; }
    
    h1 { color: #2c3e50; text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
</style>
"""

@app.route('/')
def index():
    try:
        with open("resultado_final.md", "r", encoding="utf-8") as f:
            contenido_md = f.read()
        
        # El HTML de la tabla dentro del MD pasará directo gracias a esta conversión
        contenido_html = markdown.markdown(contenido_md, extensions=['tables'])
        
        return render_template_string(f"""
            <html>
                <head><title>Visor de PDF parsed</title></head>
                <body>
                    <div class="container">
                        {CSS}
                        {contenido_html}
                    </div>
                </body>
            </html>
        """)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)