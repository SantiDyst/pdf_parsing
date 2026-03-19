# 📄 PDF Intelligent Parser & Web Reporter

Este proyecto es un extractor avanzado de datos para PDFs complejos (Leyes, Estatutos y Reportes con tablas) optimizado para ejecutarse en hardware con recursos limitados (probado en **Intel i3 con 8GB de RAM**).

Utiliza el motor **Docling** para reconstruir estructuras jerárquicas y tablas de forma precisa, exportando los resultados a un formato Markdown limpio y reportes HTML interactivos.

## ✨ Características Principales

- **Procesamiento por Chunks:** Divide PDFs extensos (60+ páginas) para procesarlos por lotes, evitando errores de memoria (`std::bad_alloc`).
- **Extracción Digital Optimizada:** Configurado para lectura de texto nativo (sin OCR innecesario), lo que reduce drásticamente el uso de CPU y RAM.
- **Corrector de Notación Científica:** Limpieza automática de datos numéricos (convierte formatos como `-4.59e+06` a moneda contable `-4.590.000,00`).
- **Visor Web Automático:** Genera reportes HTML con CSS profesional que se abren automáticamente al finalizar el proceso.
- **Exportación Flexible:** Capacidad de unificar múltiples tablas en una sola hoja de Excel.

## 🛠️ Requisitos Técnicos

- Python 3.10+
- **Librerías clave:** `docling`, `pandas`, `markdown`, `pypdf`, `openpyxl`.
- **Hardware recomendado:** Mínimo 8GB de RAM.

## 🚀 Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/pdf_parsing.git](https://github.com/tu-usuario/pdf_parsing.git)
   cd pdf_parsing