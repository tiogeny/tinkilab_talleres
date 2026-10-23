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

def draw_corner_marks(c, x1, y1, x2, y2, mark_len=10):
    c.setStrokeColor(colors.HexColor("#111827"))
    c.setLineWidth(1.2)
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

def draw_single_card_a5(c, x_offset, svg_path):
    mm = 72.0 / 25.4
    card_w = 148.5 * mm
    card_h = 210.0 * mm
    
    # 4 Corner registration marks for Station 01 camera alignment
    m_pad = 10 * mm
    draw_corner_marks(c, x_offset + m_pad, m_pad, x_offset + card_w - m_pad, card_h - m_pad, mark_len=8 * mm)
    
    # Header - Ultra clean / Bandera blanca
    c.setFillColor(colors.HexColor("#111827"))
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(x_offset + 14 * mm, card_h - 18 * mm, "FICHA DE DISEÑO & CREACIÓN")
    
    # Simple direct step instructions
    c.setFont("Helvetica", 6.8)
    c.setFillColor(colors.HexColor("#4b5563"))
    c.drawString(x_offset + 14 * mm, card_h - 23 * mm, "1. Repasa el contorno punteado con plumón negro.")
    c.drawString(x_offset + 14 * mm, card_h - 27 * mm, "2. Dibuja los ojos, boca y detalles, luego coloréalo.")
    
    # Form fields (NO 'Personaje', NO date)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor("#1f2937"))
    c.drawString(x_offset + 14 * mm, card_h - 35 * mm, "NOMBRE DE TU CRIATURA:")
    c.setStrokeColor(colors.HexColor("#9ca3af"))
    c.setLineWidth(0.6)
    c.line(x_offset + 57 * mm, card_h - 35 * mm, x_offset + card_w - 14 * mm, card_h - 35 * mm)
    
    c.drawString(x_offset + 14 * mm, card_h - 42 * mm, "CREADOR(A):")
    c.line(x_offset + 37 * mm, card_h - 42 * mm, x_offset + card_w - 14 * mm, card_h - 42 * mm)
    
    # Main Canvas Area - 100% WHITE INTERIOR, NO TEXT AROUND SILHOUETTE
    # Silhouette at EXACT physical scale 1:1 (70.0 mm height)
    pts, w_mm, h_mm = extract_scaled_points(svg_path, 70.0)
    
    cx_drawing = x_offset + card_w / 2.0
    cy_drawing = 98 * mm # Centered vertically in canvas
    
    p = c.beginPath()
    first = True
    for pt in pts:
        px = cx_drawing + pt[0] * mm
        py = cy_drawing + pt[1] * mm
        if first:
            p.moveTo(px, py)
            first = False
        else:
            p.lineTo(px, py)
    p.close()
    
    # Fill 100% white
    c.setFillColor(colors.white)
    c.drawPath(p, fill=1, stroke=0)
    
    # Dashed stroke outline for child to trace
    c.setStrokeColor(colors.HexColor("#64748b")) # Clean visible medium gray
    c.setLineWidth(0.9)
    c.setDash(3, 2.5)
    c.drawPath(p, fill=0, stroke=1)
    c.setDash() # Reset dash
    
    # Bottom: Palette Swatches (5 circles)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(colors.HexColor("#374151"))
    c.drawString(x_offset + 14 * mm, 32 * mm, "PALETA DE COLOR (PRUEBA DE PLUMONES):")
    
    for ci in range(5):
        cx_swatch = x_offset + 22 * mm + ci * 24 * mm
        cy_swatch = 22 * mm
        c.setStrokeColor(colors.HexColor("#9ca3af"))
        c.setFillColor(colors.white)
        c.setLineWidth(0.7)
        c.circle(cx_swatch, cy_swatch, 4.5 * mm, stroke=1, fill=1)
        c.setFont("Helvetica", 6)
        c.setFillColor(colors.HexColor("#6b7280"))
        c.drawCentredString(cx_swatch, cy_swatch - 7.5 * mm, f"Color {ci + 1}")

def generate_all_fichas_a5():
    svg_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\01_siluetas_svg"
    out_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\03_plantillas_impresion_pdf"
    os.makedirs(out_dir, exist_ok=True)
    
    svg_files = sorted(glob.glob(os.path.join(svg_dir, "*.svg")))
    out_pdf = os.path.join(out_dir, "fichas_trabajo_A5_2porA4.pdf")
    
    mm = 72.0 / 25.4
    w_page, h_page = landscape(A4) # 297 x 210 mm
    
    c = canvas.Canvas(out_pdf, pagesize=landscape(A4))
    c.setTitle("Fichas de Trabajo y Diseño DigiToys (A5 - 2 por A4)")
    
    # Pair SVG files 2 per sheet
    for i in range(0, len(svg_files), 2):
        svg_left = svg_files[i]
        svg_right = svg_files[i + 1] if (i + 1) < len(svg_files) else None
        
        # Draw Left A5 Card
        draw_single_card_a5(c, 0, svg_left)
        
        # Center Cutting Line with Scissors indicator
        c.setStrokeColor(colors.HexColor("#cbd5e1"))
        c.setLineWidth(0.6)
        c.setDash(4, 3)
        c.line(w_page / 2.0, 8 * mm, w_page / 2.0, h_page - 8 * mm)
        c.setDash()
        
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#9ca3af"))
        c.drawCentredString(w_page / 2.0, 10 * mm, "✂  Corte aquí (Línea media A5)")
        c.drawCentredString(w_page / 2.0, h_page - 10 * mm, "✂  Corte aquí (Línea media A5)")
        
        # Draw Right A5 Card
        if svg_right:
            draw_single_card_a5(c, w_page / 2.0, svg_right)
            
        c.showPage()
        
    c.save()
    print("Fichas A5 PDF generated successfully:", out_pdf)

if __name__ == "__main__":
    generate_all_fichas_a5()
