import os
import glob
import xml.etree.ElementTree as ET
import numpy as np
from svg.path import parse_path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def extract_scaled_points(svg_path, target_height_mm):
    tree = ET.parse(svg_path)
    paths = tree.getroot().findall('.//{http://www.w3.org/2000/svg}path')
    best_p = max(paths, key=lambda p: len(p.get('d', '')))
    parsed = parse_path(best_p.get('d'))
    
    pts = []
    for seg in parsed:
        for t in np.linspace(0, 1, 16, endpoint=False):
            pt = seg.point(t)
            pts.append([pt.real, -pt.imag]) # Invert Y for Cartesian/PDF coordinates
    pts = np.array(pts)
    
    h = pts[:, 1].max() - pts[:, 1].min()
    w = pts[:, 0].max() - pts[:, 0].min()
    scale = target_height_mm / h
    pts = pts * scale
    
    # Center points at (0, 0)
    cx = (pts[:, 0].max() + pts[:, 0].min()) / 2.0
    cy = (pts[:, 1].max() + pts[:, 1].min()) / 2.0
    pts[:, 0] -= cx
    pts[:, 1] -= cy
    
    return pts, w * scale, target_height_mm

def draw_corner_registration_marks(c, x1, y1, x2, y2, mark_len=15):
    # Standard photography calibration / corner crop marks
    c.setStrokeColor(colors.HexColor("#111827"))
    c.setLineWidth(1.5)
    
    # Top-Left
    c.line(x1, y2, x1 + mark_len, y2)
    c.line(x1, y2, x1, y2 - mark_len)
    
    # Top-Right
    c.line(x2, y2, x2 - mark_len, y2)
    c.line(x2, y2, x2, y2 - mark_len)
    
    # Bottom-Left
    c.line(x1, y1, x1 + mark_len, y1)
    c.line(x1, y1, x1, y1 + mark_len)
    
    # Bottom-Right
    c.line(x2, y1, x2 - mark_len, y1)
    c.line(x2, y1, x2, y1 + mark_len)

def build_pdf_catalog(svg_files, out_pdf):
    mm = 72.0 / 25.4
    w_page, h_page = landscape(A4) # 297 x 210 mm
    c = canvas.Canvas(out_pdf, pagesize=landscape(A4))
    c.setTitle("Catálogo de Selección DigiToys 12")
    
    # Header (Bandera blanca)
    c.setFillColor(colors.HexColor("#111827"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, h_page - 18 * mm, "CATÁLOGO DE SELECCIÓN DE PERSONAJES — DIGITOYS")
    
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#6b7280"))
    c.drawString(20 * mm, h_page - 23 * mm, "Selecciona una silueta para personalizar, escanear y fabricar en 3D (Escala estándar: 70 mm de altura)")
    
    # User fields in top right
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#374151"))
    c.drawRightString(w_page - 65 * mm, h_page - 18 * mm, "PARTICIPANTE:")
    c.setStrokeColor(colors.HexColor("#9ca3af"))
    c.setLineWidth(0.6)
    c.line(w_page - 63 * mm, h_page - 18 * mm, w_page - 20 * mm, h_page - 18 * mm)
    
    c.drawString(w_page - 100 * mm, h_page - 23 * mm, "GRUPO / FECHA:")
    c.line(w_page - 75 * mm, h_page - 23 * mm, w_page - 20 * mm, h_page - 23 * mm)
    
    # Grid 4 columns x 3 rows
    cols = 4
    rows = 3
    margin_x = 20 * mm
    margin_y = 18 * mm
    grid_w = w_page - 2 * margin_x
    grid_h = h_page - margin_y - 32 * mm
    
    cell_w = grid_w / cols
    cell_h = grid_h / rows
    
    clean_names = [
        "01 Dino Bebé 1", "02 Dino Bebé 2", "03 Fantasmita", "04 Frijolito",
        "05 Monstruo Cuernitos", "06 Mostrito Orejón", "07 Monstruo Espinoso", "08 Mostrito Periscopio",
        "09 Marciano Zog", "10 Monstruo Crestas", "11 Robot Bip Bop", "12 Gato Miau"
    ]
    
    for idx, (svg_f, name) in enumerate(zip(svg_files, clean_names)):
        col = idx % cols
        row = idx // cols
        
        # cell bounds
        cx_cell = margin_x + col * cell_w + cell_w / 2.0
        cy_cell = h_page - 30 * mm - (row * cell_h + cell_h / 2.0)
        
        # Draw cell card outline
        card_x = margin_x + col * cell_w + 2 * mm
        card_y = h_page - 30 * mm - (row + 1) * cell_h + 2 * mm
        card_w = cell_w - 4 * mm
        card_h = cell_h - 4 * mm
        
        c.setStrokeColor(colors.HexColor("#e5e7eb"))
        c.setLineWidth(0.8)
        c.setFillColor(colors.HexColor("#f9fafb"))
        c.roundRect(card_x, card_y, card_w, card_h, 3 * mm, stroke=1, fill=1)
        
        # Target silhouette height in card: 30 mm
        pts, w_mm, h_mm = extract_scaled_points(svg_f, 26.0)
        
        # Draw silhouette
        p = c.beginPath()
        first = True
        center_y_sil = card_y + card_h / 2.0 + 2 * mm
        for pt in pts:
            px = cx_cell + pt[0] * mm
            py = center_y_sil + pt[1] * mm
            if first:
                p.moveTo(px, py)
                first = False
            else:
                p.lineTo(px, py)
        p.close()
        c.setFillColor(colors.HexColor("#1f2937"))
        c.setStrokeColor(colors.HexColor("#111827"))
        c.drawPath(p, fill=1, stroke=0)
        
        # Card title
        c.setFillColor(colors.HexColor("#111827"))
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(cx_cell, card_y + 11 * mm, name)
        
        # Checkbox
        c.setStrokeColor(colors.HexColor("#9ca3af"))
        c.setFillColor(colors.white)
        c.setLineWidth(0.7)
        c.rect(cx_cell - 20 * mm, card_y + 4 * mm, 3.5 * mm, 3.5 * mm, stroke=1, fill=1)
        c.setFont("Helvetica", 6.5)
        c.setFillColor(colors.HexColor("#4b5563"))
        c.drawString(cx_cell - 14 * mm, card_y + 5 * mm, "Seleccionar este modelo")
        
    c.save()
    print("Catalog PDF generated:", out_pdf)

def build_pdf_worksheets(svg_files, out_pdf):
    mm = 72.0 / 25.4
    w_page, h_page = A4 # 210 x 297 mm
    c = canvas.Canvas(out_pdf, pagesize=A4)
    c.setTitle("Hojas de Trabajo y Diseño DigiToys 12")
    
    clean_names = [
        "01 Dino Bebé 1", "02 Dino Bebé 2", "03 Fantasmita", "04 Frijolito",
        "05 Monstruo Cuernitos", "06 Mostrito Orejón", "07 Monstruo Espinoso", "08 Mostrito Periscopio",
        "09 Marciano Zog", "10 Monstruo Crestas", "11 Robot Bip Bop", "12 Gato Miau"
    ]
    
    for idx, (svg_f, name) in enumerate(zip(svg_files, clean_names)):
        # Corner marks for Station 01 camera alignment
        draw_corner_registration_marks(c, 15 * mm, 15 * mm, w_page - 15 * mm, h_page - 15 * mm, mark_len=12 * mm)
        
        # Header (White-label)
        c.setFillColor(colors.HexColor("#111827"))
        c.setFont("Helvetica-Bold", 13)
        c.drawString(20 * mm, h_page - 24 * mm, "FICHA DE DISEÑO & PERSONALIZACIÓN DE PERSONAJE")
        
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor("#6b7280"))
        c.drawString(20 * mm, h_page - 29 * mm, "Dibuja los rasgos, ojos, boca y patrones de color directamente sobre la silueta a escala real.")
        
        # User details card
        c.setStrokeColor(colors.HexColor("#e5e7eb"))
        c.setFillColor(colors.HexColor("#f9fafb"))
        c.roundRect(20 * mm, h_page - 52 * mm, w_page - 40 * mm, 18 * mm, 2 * mm, stroke=1, fill=1)
        
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#374151"))
        c.drawString(24 * mm, h_page - 41 * mm, "CREADOR(A):")
        c.line(48 * mm, h_page - 41 * mm, 115 * mm, h_page - 41 * mm)
        
        c.drawString(122 * mm, h_page - 41 * mm, "PERSONAJE:")
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#0284c7"))
        c.drawString(146 * mm, h_page - 41 * mm, name)
        
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#374151"))
        c.drawString(24 * mm, h_page - 48 * mm, "NOMBRE DE LA CRIATURA:")
        c.line(69 * mm, h_page - 48 * mm, 130 * mm, h_page - 48 * mm)
        
        c.drawString(136 * mm, h_page - 48 * mm, "FECHA:")
        c.line(150 * mm, h_page - 48 * mm, w_page - 24 * mm, h_page - 48 * mm)
        
        # Main Canvas Area (Exact 1:1 Scale = 70.0 mm height)
        # Bounding frame for the silhouette
        canvas_y = 110 * mm
        canvas_h = 125 * mm
        c.setStrokeColor(colors.HexColor("#e5e7eb"))
        c.setLineWidth(0.6)
        c.setFillColor(colors.white)
        c.roundRect(20 * mm, canvas_y, w_page - 40 * mm, canvas_h, 3 * mm, stroke=1, fill=1)
        
        # Watermark label in canvas
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(colors.HexColor("#9ca3af"))
        c.drawString(25 * mm, canvas_y + canvas_h - 8 * mm, "LIENZO DE DIBUJO — ESCALA 1:1 REAL (ALTURA 70.0 mm)")
        
        # Extract silhouette at EXACT 70.0 mm
        pts, w_mm, h_mm = extract_scaled_points(svg_f, 70.0)
        
        # Center of drawing area
        cx_drawing = w_page / 2.0
        cy_drawing = canvas_y + canvas_h / 2.0
        
        # 1. Light background fill of silhouette
        p_fill = c.beginPath()
        first = True
        for pt in pts:
            px = cx_drawing + pt[0] * mm
            py = cy_drawing + pt[1] * mm
            if first:
                p_fill.moveTo(px, py)
                first = False
            else:
                p_fill.lineTo(px, py)
        p_fill.close()
        c.setFillColor(colors.HexColor("#f3f4f6"))
        c.drawPath(p_fill, fill=1, stroke=0)
        
        # 2. Outline of silhouette (dashed gray line so child can easily draw over)
        c.setStrokeColor(colors.HexColor("#9ca3af"))
        c.setLineWidth(1.0)
        c.setDash(3, 2)
        c.drawPath(p_fill, fill=0, stroke=1)
        c.setDash() # reset
        
        # Dimensions annotations on canvas
        c.setFont("Helvetica", 6.5)
        c.setFillColor(colors.HexColor("#9ca3af"))
        c.drawString(cx_drawing - 18 * mm, cy_drawing - 42 * mm, f"Ancho: {w_mm:.1f} mm  ×  Alto: 70.0 mm")
        
        # Lower section: Palette and Notes
        # Left: Color Palette Swatches
        bot_y = 22 * mm
        bot_h = 80 * mm
        
        c.setStrokeColor(colors.HexColor("#e5e7eb"))
        c.setFillColor(colors.HexColor("#f9fafb"))
        c.roundRect(20 * mm, bot_y, 75 * mm, bot_h, 2 * mm, stroke=1, fill=1)
        
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#111827"))
        c.drawString(25 * mm, bot_y + bot_h - 9 * mm, "PALETA DE COLOR")
        c.setFont("Helvetica", 6.5)
        c.setFillColor(colors.HexColor("#6b7280"))
        c.drawString(25 * mm, bot_y + bot_h - 14 * mm, "Pinta las muestras con tus marcadores:")
        
        # 5 color swatch circles
        for ci in range(5):
            cy_c = bot_y + bot_h - 24 * mm - ci * 11 * mm
            c.setStrokeColor(colors.HexColor("#9ca3af"))
            c.setFillColor(colors.white)
            c.setLineWidth(0.8)
            c.circle(32 * mm, cy_c, 4 * mm, stroke=1, fill=1)
            c.setFont("Helvetica", 7)
            c.setFillColor(colors.HexColor("#4b5563"))
            c.drawString(40 * mm, cy_c - 2 * mm, f"Color {ci + 1}: _________________")
            
        # Right: Notes, Superpowers and Instructions
        notes_x = 100 * mm
        notes_w = w_page - 20 * mm - notes_x
        c.roundRect(notes_x, bot_y, notes_w, bot_h, 2 * mm, stroke=1, fill=1)
        
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#111827"))
        c.drawString(notes_x + 5 * mm, bot_y + bot_h - 9 * mm, "NOTAS & HISTORIA DEL PERSONAJE")
        
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#4b5563"))
        c.drawString(notes_x + 5 * mm, bot_y + bot_h - 18 * mm, "Superpoder o habilidad:")
        c.setStrokeColor(colors.HexColor("#d1d5db"))
        c.line(notes_x + 5 * mm, bot_y + bot_h - 26 * mm, notes_x + notes_w - 5 * mm, bot_y + bot_h - 26 * mm)
        c.line(notes_x + 5 * mm, bot_y + bot_h - 34 * mm, notes_x + notes_w - 5 * mm, bot_y + bot_h - 34 * mm)
        
        c.drawString(notes_x + 5 * mm, bot_y + bot_h - 43 * mm, "Detalles de acabado (ojos, boca, accesorios):")
        c.line(notes_x + 5 * mm, bot_y + bot_h - 51 * mm, notes_x + notes_w - 5 * mm, bot_y + bot_h - 51 * mm)
        c.line(notes_x + 5 * mm, bot_y + bot_h - 59 * mm, notes_x + notes_w - 5 * mm, bot_y + bot_h - 59 * mm)
        
        # Mini tip box
        c.setFillColor(colors.HexColor("#e0f2fe"))
        c.roundRect(notes_x + 4 * mm, bot_y + 4 * mm, notes_w - 8 * mm, 14 * mm, 2 * mm, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 6.5)
        c.setFillColor(colors.HexColor("#0369a1"))
        c.drawString(notes_x + 7 * mm, bot_y + 13 * mm, "CONSEJO PARA LA ESTACIÓN DE FOTO:")
        c.setFont("Helvetica", 6)
        c.drawString(notes_x + 7 * mm, bot_y + 8 * mm, "Coloca la hoja completamente plana con buena iluminación sin sombras.")
        
        c.showPage()
        
    c.save()
    print("Worksheets PDF generated:", out_pdf)

def build_pdf_freeform(out_pdf):
    mm = 72.0 / 25.4
    w_page, h_page = A4
    c = canvas.Canvas(out_pdf, pagesize=A4)
    c.setTitle("Plantilla de Diseño Libre DigiToy")
    
    draw_corner_registration_marks(c, 15 * mm, 15 * mm, w_page - 15 * mm, h_page - 15 * mm, mark_len=12 * mm)
    
    # Header
    c.setFillColor(colors.HexColor("#111827"))
    c.setFont("Helvetica-Bold", 13)
    c.drawString(20 * mm, h_page - 24 * mm, "FICHA DE DISEÑO LIBRE — CREA TU PROPIA SILUETA")
    
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#6b7280"))
    c.drawString(20 * mm, h_page - 29 * mm, "Dibuja una silueta cerrada con plumón negro grueso dentro del área de trabajo para vectorizarla en 3D.")
    
    # Header card
    c.setStrokeColor(colors.HexColor("#e5e7eb"))
    c.setFillColor(colors.HexColor("#f9fafb"))
    c.roundRect(20 * mm, h_page - 52 * mm, w_page - 40 * mm, 18 * mm, 2 * mm, stroke=1, fill=1)
    
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#374151"))
    c.drawString(24 * mm, h_page - 41 * mm, "CREADOR(A):")
    c.line(48 * mm, h_page - 41 * mm, 115 * mm, h_page - 41 * mm)
    
    c.drawString(122 * mm, h_page - 41 * mm, "TIPO: DISEÑO 100% ORIGINAL")
    
    c.drawString(24 * mm, h_page - 48 * mm, "NOMBRE DE LA CRIATURA:")
    c.line(69 * mm, h_page - 48 * mm, 130 * mm, h_page - 48 * mm)
    
    c.drawString(136 * mm, h_page - 48 * mm, "FECHA:")
    c.line(150 * mm, h_page - 48 * mm, w_page - 24 * mm, h_page - 48 * mm)
    
    # Main Canvas Area with Dot Grid (10 mm spacing)
    canvas_y = 65 * mm
    canvas_h = 170 * mm
    c.setStrokeColor(colors.HexColor("#9ca3af"))
    c.setLineWidth(1.0)
    c.setFillColor(colors.white)
    c.roundRect(20 * mm, canvas_y, w_page - 40 * mm, canvas_h, 3 * mm, stroke=1, fill=1)
    
    # Draw faint dots grid inside canvas
    c.setFillColor(colors.HexColor("#d1d5db"))
    for x in np.arange(30 * mm, w_page - 30 * mm, 10 * mm):
        for y in np.arange(canvas_y + 10 * mm, canvas_y + canvas_h - 10 * mm, 10 * mm):
            c.circle(x, y, 0.6, stroke=0, fill=1)
            
    # Center target mark
    c.setStrokeColor(colors.HexColor("#9ca3af"))
    c.setLineWidth(0.5)
    c.setDash(2, 2)
    c.circle(w_page / 2.0, canvas_y + canvas_h / 2.0, 35 * mm, stroke=1, fill=0) # 70 mm circle guide
    c.setDash()
    c.setFont("Helvetica", 6.5)
    c.setFillColor(colors.HexColor("#9ca3af"))
    c.drawCentredString(w_page / 2.0, canvas_y + canvas_h / 2.0 - 38 * mm, "Zona recomendada de silueta (máx. 70 mm)")
    
    # Bottom Guidelines
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#111827"))
    c.drawString(20 * mm, 54 * mm, "REGLAS DE ORO PARA EL DIBUJO DE TU SILUETA:")
    
    rules = [
        "1. Contorno cerrado: Asegúrate de que todas las líneas se unan (no dejes aberturas).",
        "2. Trazo grueso y nítido: Usa un plumón negro oscuro de punta media o gruesa.",
        "3. Evita piezas flotantes: Todos los brazos, cuernos o patas deben nacer del cuerpo principal.",
        "4. Una vez terminado, llévalo a la Estación 01 (Foto Estudio) para escanear y generar tu archivo 3D."
    ]
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor("#4b5563"))
    for ri, rule in enumerate(rules):
        c.drawString(20 * mm, 46 * mm - ri * 7 * mm, rule)
        
    c.save()
    print("Freeform PDF generated:", out_pdf)

def main():
    svg_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\01_siluetas_svg"
    out_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\03_plantillas_impresion_pdf"
    os.makedirs(out_dir, exist_ok=True)
    
    svg_files = sorted(glob.glob(os.path.join(svg_dir, "*.svg")))
    
    catalog_pdf = os.path.join(out_dir, "01_catalogo_seleccion_12_A4.pdf")
    worksheets_pdf = os.path.join(out_dir, "02_hojas_trabajo_diseno_12_A4.pdf")
    freeform_pdf = os.path.join(out_dir, "03_plantilla_diseno_libre_A4.pdf")
    
    build_pdf_catalog(svg_files, catalog_pdf)
    build_pdf_worksheets(svg_files, worksheets_pdf)
    build_pdf_freeform(freeform_pdf)
    print("All printable worksheets successfully generated!")

if __name__ == "__main__":
    main()
