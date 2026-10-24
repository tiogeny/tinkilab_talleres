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
    
    cx = (pts[:, 0].max() + pts[:, 0].min()) / 2.0
    cy = (pts[:, 1].max() + pts[:, 1].min()) / 2.0
    pts[:, 0] -= cx
    pts[:, 1] -= cy
    
    return pts, w * scale, target_height_mm

def draw_corner_marks(c, x1, y1, x2, y2, mark_len=8):
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

# --- 1. FICHA A5 DIRECTA (SOLO NEGRO PARA ESCANEAR, 2 POR HOJA A4) ---
def draw_single_card_a5(c, x_offset, svg_path):
    mm = 72.0 / 25.4
    card_w = 148.5 * mm
    card_h = 210.0 * mm
    
    m_pad = 12 * mm
    draw_corner_marks(c, x_offset + m_pad, m_pad, x_offset + card_w - m_pad, card_h - m_pad, mark_len=8 * mm)
    
    # Encabezado limpio
    c.setFillColor(colors.HexColor("#111827"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x_offset + 16 * mm, card_h - 18 * mm, "FICHA DE FABRICACIÓN 3D — SILUETA")
    
    # Instrucciones exactas
    c.setFont("Helvetica", 6.8)
    c.setFillColor(colors.HexColor("#4b5563"))
    c.drawString(x_offset + 16 * mm, card_h - 23 * mm, "1. Repasa el contorno punteado con plumón negro.")
    c.drawString(x_offset + 16 * mm, card_h - 27 * mm, "2. Rellena toda la silueta de negro sólido para escanear en 3D.")
    
    # Campos
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor("#1f2937"))
    c.drawString(x_offset + 16 * mm, card_h - 36 * mm, "NOMBRE DE TU CRIATURA:")
    c.setStrokeColor(colors.HexColor("#9ca3af"))
    c.setLineWidth(0.6)
    c.line(x_offset + 59 * mm, card_h - 36 * mm, x_offset + card_w - 16 * mm, card_h - 36 * mm)
    
    c.drawString(x_offset + 16 * mm, card_h - 43 * mm, "CREADOR(A):")
    c.line(x_offset + 39 * mm, card_h - 43 * mm, x_offset + card_w - 16 * mm, card_h - 43 * mm)
    
    # Silueta a escala 1:1 física (70.0 mm de altura)
    pts, w_mm, h_mm = extract_scaled_points(svg_path, 70.0)
    
    cx_drawing = x_offset + card_w / 2.0
    cy_drawing = 85 * mm
    
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
    
    # Interior 100% blanco
    c.setFillColor(colors.white)
    c.drawPath(p, fill=1, stroke=0)
    
    # Línea punteada en gris medio para repasar
    c.setStrokeColor(colors.HexColor("#64748b"))
    c.setLineWidth(0.9)
    c.setDash(3, 2.5)
    c.drawPath(p, fill=0, stroke=1)
    c.setDash()
    
    # Recordatorio sutil al pie (lejos de la silueta)
    c.setFont("Helvetica", 6.2)
    c.setFillColor(colors.HexColor("#9ca3af"))
    c.drawCentredString(cx_drawing, 16 * mm, "Llevar a la Estación 01 (Foto Estudio) con la silueta completamente rellenada de negro.")

def generate_fichas_a5():
    svg_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\01_siluetas_svg"
    out_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\03_plantillas_impresion_pdf"
    os.makedirs(out_dir, exist_ok=True)
    
    svg_files = sorted(glob.glob(os.path.join(svg_dir, "*.svg")))
    out_pdf = os.path.join(out_dir, "fichas_trabajo_A5_imprimir.pdf")
    
    mm = 72.0 / 25.4
    w_page, h_page = landscape(A4) # 297 x 210 mm
    c = canvas.Canvas(out_pdf, pagesize=landscape(A4))
    c.setTitle("Fichas de Trabajo DigiToys (A5 - 2 por A4)")
    
    for i in range(0, len(svg_files), 2):
        svg_left = svg_files[i]
        svg_right = svg_files[i + 1] if (i + 1) < len(svg_files) else None
        
        draw_single_card_a5(c, 0, svg_left)
        
        # Línea central sutil de corte (SIN TEXTO que distraiga)
        c.setStrokeColor(colors.HexColor("#e2e8f0"))
        c.setLineWidth(0.6)
        c.setDash(4, 3)
        c.line(w_page / 2.0, 10 * mm, w_page / 2.0, h_page - 10 * mm)
        c.setDash()
        
        if svg_right:
            draw_single_card_a5(c, w_page / 2.0, svg_right)
            
        c.showPage()
        
    c.save()
    print("Fichas A5 PDF saved:", out_pdf)

# --- 2. FICHA DUAL A4 (LADO IZQUIERDO NEGRO / LADO DERECHO COLOR) ---
def generate_fichas_duales_a4():
    svg_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\01_siluetas_svg"
    out_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\03_plantillas_impresion_pdf"
    os.makedirs(out_dir, exist_ok=True)
    
    svg_files = sorted(glob.glob(os.path.join(svg_dir, "*.svg")))
    out_pdf = os.path.join(out_dir, "fichas_trabajo_A4_dual.pdf")
    
    mm = 72.0 / 25.4
    w_page, h_page = landscape(A4) # 297 x 210 mm
    c = canvas.Canvas(out_pdf, pagesize=landscape(A4))
    c.setTitle("Ficha Dual de Diseño DigiToys (Negro + Color)")
    
    col_w = w_page / 2.0
    
    for svg_f in svg_files:
        # Encabezado general
        c.setFillColor(colors.HexColor("#111827"))
        c.setFont("Helvetica-Bold", 11)
        c.drawString(16 * mm, h_page - 16 * mm, "FICHA DE CREACIÓN & ACABADO 3D")
        
        # Campos superiores
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(16 * mm, h_page - 23 * mm, "NOMBRE DE TU CRIATURA:")
        c.setStrokeColor(colors.HexColor("#9ca3af"))
        c.setLineWidth(0.6)
        c.line(58 * mm, h_page - 23 * mm, 140 * mm, h_page - 23 * mm)
        
        c.drawString(155 * mm, h_page - 23 * mm, "CREADOR(A):")
        c.line(177 * mm, h_page - 23 * mm, w_page - 16 * mm, h_page - 23 * mm)
        
        # Línea divisoria central
        c.setStrokeColor(colors.HexColor("#e2e8f0"))
        c.setLineWidth(0.8)
        c.line(col_w, 14 * mm, col_w, h_page - 28 * mm)
        
        # --- LADO IZQUIERDO: ESTACIÓN 01/02 (SILUETA NEGRA PARA ESCANEAR) ---
        draw_corner_marks(c, 16 * mm, 16 * mm, col_w - 12 * mm, h_page - 30 * mm, mark_len=8 * mm)
        
        c.setFillColor(colors.HexColor("#0f172a"))
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(20 * mm, h_page - 36 * mm, "LADO 1: ESCANEO 3D (RELLENAR DE NEGRO)")
        c.setFont("Helvetica", 6.5)
        c.setFillColor(colors.HexColor("#64748b"))
        c.drawString(20 * mm, h_page - 41 * mm, "Repasa el contorno y rellena toda la figura de negro sólido con plumón.")
        
        # Silueta izquierda a 70 mm
        pts, w_mm, h_mm = extract_scaled_points(svg_f, 70.0)
        cx_left = col_w / 2.0
        cy_left = 90 * mm
        
        p_left = c.beginPath()
        first = True
        for pt in pts:
            px = cx_left + pt[0] * mm
            py = cy_left + pt[1] * mm
            if first:
                p_left.moveTo(px, py)
                first = False
            else:
                p_left.lineTo(px, py)
        p_left.close()
        
        c.setFillColor(colors.white)
        c.drawPath(p_left, fill=1, stroke=0)
        c.setStrokeColor(colors.HexColor("#64748b"))
        c.setLineWidth(0.9)
        c.setDash(3, 2.5)
        c.drawPath(p_left, fill=0, stroke=1)
        c.setDash()
        
        # --- LADO DERECHO: ESTACIÓN 05 (BOCETO DE COLOR Y CARITA) ---
        c.setFillColor(colors.HexColor("#0284c7"))
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(col_w + 16 * mm, h_page - 36 * mm, "LADO 2: PLAN DE COLOR (BOCETO DE PINTURA)")
        c.setFont("Helvetica", 6.5)
        c.setFillColor(colors.HexColor("#64748b"))
        c.drawString(col_w + 16 * mm, h_page - 41 * mm, "Dibuja los ojos, boca, manchas y colores como pintarás tu pieza en 3D.")
        
        # Silueta derecha a 70 mm
        cx_right = col_w + col_w / 2.0
        cy_right = 100 * mm
        
        p_right = c.beginPath()
        first = True
        for pt in pts:
            px = cx_right + pt[0] * mm
            py = cy_right + pt[1] * mm
            if first:
                p_right.moveTo(px, py)
                first = False
            else:
                p_right.lineTo(px, py)
        p_right.close()
        
        c.setFillColor(colors.HexColor("#f8fafc"))
        c.drawPath(p_right, fill=1, stroke=0)
        c.setStrokeColor(colors.HexColor("#94a3b8"))
        c.setLineWidth(0.9)
        c.setDash(3, 2.5)
        c.drawPath(p_right, fill=0, stroke=1)
        c.setDash()
        
        # Paleta de 5 colores en el lado derecho
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col_w + 16 * mm, 36 * mm, "PALETA DE COLOR PARA TU MUÑECO:")
        for ci in range(5):
            cx_swatch = col_w + 24 * mm + ci * 22 * mm
            cy_swatch = 24 * mm
            c.setStrokeColor(colors.HexColor("#9ca3af"))
            c.setFillColor(colors.white)
            c.setLineWidth(0.7)
            c.circle(cx_swatch, cy_swatch, 4.5 * mm, stroke=1, fill=1)
            c.setFont("Helvetica", 6)
            c.setFillColor(colors.HexColor("#64748b"))
            c.drawCentredString(cx_swatch, cy_swatch - 7 * mm, f"C{ci+1}")
            
        c.showPage()
        
    c.save()
    print("Fichas Duales A4 PDF saved:", out_pdf)

if __name__ == "__main__":
    generate_fichas_a5()
    generate_fichas_duales_a4()
