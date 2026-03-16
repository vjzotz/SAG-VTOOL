# SAG-VTOOL
Script de Automatización de Grillas (Visual Tool)
Desarrollado por vjzotz.

🚀 Descripción
SAG (VTOOL) es una herramienta técnica diseñada para generar automáticamente grillas de alineación y archivos de referencia para proyectos de pantallas LED, Proyecciones y Video Mapping. El script calcula proporciones reales en metros y las exporta a formatos SVG (vectorial) y PNG (imagen) de alta calidad.

🛠️ Requisitos de Sistema
Para que el generador funcione, necesitas tener instalado:

Python 3.x.

Biblioteca Cairo (necesaria para la conversión a PNG):

Windows: Instalar GTK for Windows.

macOS: brew install cairo.

📦 Instalación
Clona este repositorio o descarga los archivos y ejecuta el siguiente comando para instalar las dependencias de Python:

Bash
pip install -r requirements.txt
📖 Modo de Uso
Abre el archivo grilla.py con cualquier editor de texto.

Modifica los Parámetros de Entrada según tu necesidad:

nombre_proyecto: El título que aparecerá en el visual.

ancho_metros / alto_metros: Dimensiones reales de tu pantalla.

ruta_logo: Nombre de tu archivo de logo (debe estar en la misma carpeta).

Ejecuta el script:

Bash
python grilla.py
Busca los archivos generados con el sufijo _final en tu carpeta.

👤 Créditos y Personalización
Autor: Yankel Dickerman / vjzotz.

Instagram: @vjzotz

Personalización: El archivo WATERMARK.fw.png es un ejemplo. Puedes reemplazarlo por tu propio logo manteniendo el mismo nombre para que el script lo integre automáticamente.

_____________________________________________________________________________________________________________________________________________________________________________

SAG (V/TOOL)
Grid Alignment Script for Video Mapping and A/V Sets.

Developed by vjzotz.

🚀 Overview
SAG (V/TOOL) is a technical utility designed to automatically generate alignment grids and reference files for LED screens, projections, and Video Mapping projects. The script calculates real-world proportions in meters and exports them into high-quality SVG (vector) and PNG (image) formats.

🛠️ System Requirements
To run the generator, you need:

Python 3.x.

Cairo Library (required for PNG conversion):

Windows: Install GTK for Windows.

macOS: brew install cairo.

📦 Installation
Clone this repository or download the files and run the following command to install Python dependencies:

Bash
pip install -r requirements.txt
📖 How to Use
Open the grilla.py file with any text editor.

Modify the Input Parameters as needed:

nombre_proyecto: The title that will appear on the visual.

ancho_metros / alto_metros: Real dimensions of your screen/surface.

ruta_logo: Your logo filename (must be in the same folder).

Run the script:

Bash
python grilla.py
Look for the generated files with the _final suffix in your folder.

👤 Credits & Customization
Author: Yankel Dickerman / vjzotz.

Instagram: @vjzotz

Customization: The WATERMARK.fw.png file is a placeholder. You can replace it with your own logo file using the same name to automatically integrate it into the grid.
