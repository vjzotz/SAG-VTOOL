import svgwrite
import os
import string
import math
import cairosvg
import pathlib
import base64

# ----------------- 1. PARÁMETROS DE ENTRADA -----------------
nombre_proyecto = "PANTALLA X"
ancho_metros = 4
alto_metros = 1
ruta_logo = "WATERMARK.fw.png"
texto_adicional_logo = "@vjzotz"

# ----------------- 2. CÁLCULOS Y CONSTANTES -----------------
ESCALA = 256
ancho_px = ancho_metros * ESCALA
alto_px = alto_metros * ESCALA

BREAKPOINT = 256 # 1 metro

# --- LÓGICA DE ESCALADO GLOBAL ---
if ancho_px < BREAKPOINT or alto_px < BREAKPOINT:
    print("--- MODO COMPACTO ACTIVADO ---")
    escala_layout = 0.5
else:
    print("--- MODO GRANDE ACTIVADO ---")
    escala_layout = 1.0

# Aplicar escala a las constantes de dibujo
TAMANO_CUADRADO_FONDO = int(64 * escala_layout)
# Asegurarse de que el tamaño del cuadrado no sea cero
if TAMANO_CUADRADO_FONDO == 0: TAMANO_CUADRADO_FONDO = 1
ANCHO_ZONA_BORDE = TAMANO_CUADRADO_FONDO

LOGO_WIDTH_BASE = 161 * 1.4
LOGO_HEIGHT_BASE = 162 * 1.4

# ----------------- 3. LÓGICA DE DIBUJO -----------------
def generar_grilla_final():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    nombre_base_archivo = f'{nombre_proyecto}_final'
    ruta_svg = os.path.join(script_dir, f'{nombre_base_archivo}.svg')
    ruta_png = os.path.join(script_dir, f'{nombre_base_archivo}.png')

    lienzo = svgwrite.Drawing(viewBox=(f"0 0 {ancho_px} {alto_px}"))

    # --- DEFINIR ESTILOS (CSS) ---
    styles = """
        .st0 { stroke: red; stroke-width: 1px; fill: none; }
        .st1 { stroke: red; stroke-width: .5px; fill: none; }
        .st3 { stroke: orange; stroke-width: 3px; fill: none; }
        .st4 { stroke: lime; stroke-width: 10px; fill: none; }
        .st5 { fill: #fff; font-family: Arial-BoldMT, Arial; font-weight: 700; text-anchor: middle; dominant-baseline: central; }
        .st7 { fill: #fff; font-family: ArialMT, Arial; text-anchor: middle; dominant-baseline: central; }
        .st8 { fill: #fff; font-family: Arial-BoldMT, Arial; font-weight: 700; text-anchor: middle; dominant-baseline: central; }
        .st-vjzotz { fill: #FF0000; font-family: Arial-BoldMT, Arial; font-weight: 700; text-anchor: middle; dominant-baseline: central; }
        .st9 { fill: #081700; } .st10 { fill: #0b2300; }
        .black { fill: #000000; } .st12 { fill: #101010; }
    """
    lienzo.defs.add(lienzo.style(styles))

    # --- DIBUJAR FONDO ---
    grupo_fondo = lienzo.g()
    for y in range(0, int(alto_px), TAMANO_CUADRADO_FONDO):
        for x in range(0, int(ancho_px), TAMANO_CUADRADO_FONDO):
            is_border = x < ANCHO_ZONA_BORDE or x >= ancho_px - ANCHO_ZONA_BORDE or y < ANCHO_ZONA_BORDE or y >= alto_px - ANCHO_ZONA_BORDE
            is_even_pattern = (x // TAMANO_CUADRADO_FONDO + y // TAMANO_CUADRADO_FONDO) % 2 == 0
            clase_css = ('st9' if is_even_pattern else 'st10') if is_border else ('black' if is_even_pattern else 'st12')
            grupo_fondo.add(lienzo.rect(insert=(x, y), size=(TAMANO_CUADRADO_FONDO, TAMANO_CUADRADO_FONDO), class_=clase_css))
    lienzo.add(grupo_fondo)
    
    # --- GRILLA ROJA ALINEADA ---
    GRILLA_ROJA_START_X = ANCHO_ZONA_BORDE; GRILLA_ROJA_END_X = int(ancho_px) - ANCHO_ZONA_BORDE; GRILLA_ROJA_START_Y = ANCHO_ZONA_BORDE; GRILLA_ROJA_END_Y = int(alto_px) - ANCHO_ZONA_BORDE; ESPACIADO_GRILLA_ROJA = TAMANO_CUADRADO_FONDO
    grupo_grilla_roja = lienzo.g(class_='st1')
    for y in range(GRILLA_ROJA_START_Y, GRILLA_ROJA_END_Y + 1, ESPACIADO_GRILLA_ROJA): grupo_grilla_roja.add(lienzo.line(start=(GRILLA_ROJA_START_X, y), end=(GRILLA_ROJA_END_X, y)))
    for x in range(GRILLA_ROJA_START_X, GRILLA_ROJA_END_X + 1, ESPACIADO_GRILLA_ROJA): grupo_grilla_roja.add(lienzo.line(start=(x, GRILLA_ROJA_START_Y), end=(x, GRILLA_ROJA_END_Y)))
    lienzo.add(grupo_grilla_roja)

    # --- CÍRCULOS ---
    clip_path = lienzo.defs.add(lienzo.clipPath(id="canvas_clip")); clip_path.add(lienzo.rect(insert=(0, 0), size=(ancho_px, alto_px)))
    grupo_circulos = lienzo.g(class_='st0', clip_path="url(#canvas_clip)")
    radio = alto_px / 2; centro_y_circulos = alto_px / 2
    grupo_circulos.add(lienzo.circle(center=(ancho_px/2, centro_y_circulos), r=radio))
    current_cx_derecha = ancho_px/2 + radio
    while current_cx_derecha - radio < ancho_px: grupo_circulos.add(lienzo.circle(center=(current_cx_derecha, centro_y_circulos), r=radio)); current_cx_derecha += radio
    current_cx_izquierda = ancho_px/2 - radio
    while current_cx_izquierda + radio > 0: grupo_circulos.add(lienzo.circle(center=(current_cx_izquierda, centro_y_circulos), r=radio)); current_cx_izquierda -= radio
    lienzo.add(grupo_circulos)
    
    # --- COORDENADAS ---
    grupo_coordenadas = lienzo.g(); font_size_coords = TAMANO_CUADRADO_FONDO / 2.5
    x_izq = ANCHO_ZONA_BORDE / 2; x_der = ancho_px - ANCHO_ZONA_BORDE / 2; y_arr = ANCHO_ZONA_BORDE / 2; y_abj = alto_px - ANCHO_ZONA_BORDE / 2
    grupo_coordenadas.add(lienzo.text('NO', insert=(x_izq, y_arr), font_size=f"{font_size_coords}px", class_='st8')); grupo_coordenadas.add(lienzo.text('NE', insert=(x_der, y_arr), font_size=f"{font_size_coords}px", class_='st8'))
    grupo_coordenadas.add(lienzo.text('SO', insert=(x_izq, y_abj), font_size=f"{font_size_coords}px", class_='st8')); grupo_coordenadas.add(lienzo.text('SE', insert=(x_der, y_abj), font_size=f"{font_size_coords}px", class_='st8'))
    celda_central_x = math.floor((ancho_px / 2) / TAMANO_CUADRADO_FONDO); num_celdas_x = int(ancho_px / TAMANO_CUADRADO_FONDO)
    if num_celdas_x > 2:
        for i in range(1, num_celdas_x - 1):
            x = i * TAMANO_CUADRADO_FONDO; numero = (i - celda_central_x) if i < celda_central_x else (i - celda_central_x + 1)
            pos_x_texto = x + (TAMANO_CUADRADO_FONDO / 2); grupo_coordenadas.add(lienzo.text(str(numero), insert=(pos_x_texto, y_arr), font_size=f"{font_size_coords}px", class_='st8')); grupo_coordenadas.add(lienzo.text(str(numero), insert=(pos_x_texto, y_abj), font_size=f"{font_size_coords}px", class_='st8'))
    celda_central_y = math.floor((alto_px / 2) / TAMANO_CUADRADO_FONDO); num_celdas_y = int(alto_px / TAMANO_CUADRADO_FONDO)
    letras_mayusculas = string.ascii_uppercase; letras_minusculas = string.ascii_lowercase
    if num_celdas_y > 2:
        for j in range(1, num_celdas_y - 1):
            y = j * TAMANO_CUADRADO_FONDO; caracter = ''
            if j < celda_central_y:
                idx = celda_central_y - j - 1
                if idx < len(letras_minusculas): caracter = letras_minusculas[idx]
            else:
                idx = j - celda_central_y
                if idx < len(letras_mayusculas): caracter = letras_mayusculas[idx]
            if caracter:
                pos_y_texto = y + (TAMANO_CUADRADO_FONDO / 2); grupo_coordenadas.add(lienzo.text(caracter, insert=(x_izq, pos_y_texto), font_size=f"{font_size_coords}px", class_='st8')); grupo_coordenadas.add(lienzo.text(caracter, insert=(x_der, pos_y_texto), font_size=f"{font_size_coords}px", class_='st8'))
    lienzo.add(grupo_coordenadas)
    
    # --- LÍNEAS PRINCIPALES Y BORDE ---
    lineas_principales = lienzo.g(class_='st3')
    lineas_principales.add(lienzo.line(start=(0, alto_px/2), end=(ancho_px, alto_px/2))); lineas_principales.add(lienzo.line(start=(ancho_px/2, 0), end=(ancho_px/2, alto_px)))
    lineas_principales.add(lienzo.line(start=(0, 0), end=(ancho_px, alto_px))); lineas_principales.add(lienzo.line(start=(ancho_px, 0), end=(0, alto_px)))
    lienzo.add(lineas_principales)
    lienzo.add(lienzo.rect(insert=(0,0), size=(ancho_px, alto_px), class_='st4'))
    
    # --- ÚLTIMOS ELEMENTOS: TEXTOS Y LOGO ---
    centro_horizontal = ancho_px / 2
    font_size_titulo = (alto_px * 0.20) * escala_layout
    font_size_subtitulo = font_size_titulo / 2
    font_size_firma = font_size_subtitulo / 2
    logo_width_final = LOGO_WIDTH_BASE * escala_layout / 2
    logo_height_final = LOGO_HEIGHT_BASE * escala_layout / 2
    distancia_titulo_subtitulo = (alto_px * 0.15) * escala_layout
    distancia_subtitulo_logo = (alto_px * 0.10) * escala_layout
    pos_y_titulo = alto_px / 3
    pos_y_subtitulo = pos_y_titulo + distancia_titulo_subtitulo
    pos_y_logo_insert = pos_y_subtitulo + distancia_subtitulo_logo
    pos_x_logo_insert = centro_horizontal - (logo_width_final / 2)
    pos_y_texto_firma = pos_y_logo_insert + logo_height_final + (5 * escala_layout)

    # --- DIBUJAR ---
    ruta_completa_logo = os.path.join(script_dir, ruta_logo)
    if os.path.exists(ruta_completa_logo):
        with open(ruta_completa_logo, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        logo_data_uri = f"data:image/png;base64,{encoded_string}"
        lienzo.add(lienzo.image(href=logo_data_uri, insert=(pos_x_logo_insert, pos_y_logo_insert), size=(logo_width_final, logo_height_final)))
        lienzo.add(lienzo.text(texto_adicional_logo, insert=(centro_horizontal, pos_y_texto_firma), font_size=f"{font_size_firma}px", class_='st-vjzotz'))
    else:
        print(f"--- ADVERTENCIA: No se encontró el logo en la ruta esperada: {ruta_completa_logo}")
    lienzo.add(lienzo.text(nombre_proyecto.upper(), insert=(centro_horizontal, pos_y_titulo), font_size=f"{font_size_titulo}px", class_='st5'))
    lienzo.add(lienzo.text(f"{ancho_metros}x{alto_metros} mts", insert=(centro_horizontal, pos_y_subtitulo), font_size=f"{font_size_subtitulo}px", class_='st7'))
    
    # --- GUARDADO Y CONVERSIÓN ---
    svg_content_string = lienzo.tostring()
    with open(ruta_svg, 'w', encoding='utf-8') as f: f.write(svg_content_string)
    print(f"¡ÉXITO! Archivo '{os.path.basename(ruta_svg)}' creado.")
    
    cairosvg.svg2png(bytestring=svg_content_string.encode('utf-8'), write_to=ruta_png, output_width=int(ancho_px), output_height=int(alto_px))
    print(f"¡ÉXITO! Archivo '{os.path.basename(ruta_png)}' creado.")

# --- EJECUTAR LA FUNCIÓN PRINCIPAL ---
if __name__ == "__main__":
    try:
        generar_grilla_final()
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"HA OCURRIDO UN ERROR:")
        print(f"Error: {e}\nTipo de error: {type(e).__name__}")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        input("Presioná Enter para cerrar...")