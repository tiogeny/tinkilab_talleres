import os
import glob
import xml.etree.ElementTree as ET
import numpy as np
from svg.path import parse_path
from reportlab.lib.pagesizes import A4
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
            pts.append([pt.real, -pt.imag])
    pts = np.array(pts)
    
    h = pts[:, 1].max() - pts[:, 1].min()
    w = pts[:, 0].max() - pts[:, 0].min()
    scale = target_height_mm / h
    pts = pts * scale
    
    # Align feet to 0 in Y, center in X
    cx = (pts[:, 0].max() + pts[:, 0].min()) / 2.0
    min_y = pts[:, 1].min()
    pts[:, 0] -= cx
    pts[:, 1] -= min_y # 0 is at bottom (feet)
    
    return pts, w * scale, target_height_mm

def generate_box_17mm(sil_pts=None, char_name="Universal"):
    out_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\04_packaging_box"
    os.makedirs(out_dir, exist_ok=True)
    
    suffix = f"_{char_name}" if char_name != "Universal" else ""
    pdf_path = os.path.join(out_dir, f"caja_laser_80x80x17{suffix}.pdf")
    svg_path = os.path.join(out_dir, f"caja_laser_80x80x17{suffix}.svg")
    
    mm = 72.0 / 25.4
    page_w = 210.0 * mm
    page_h = 297.0 * mm
    
    # Internal dimensions in mm
    W = 80.0 # Width
    L = 80.0 # Height/Length
    H = 17.0 # Depth/Thickness for 15mm toy
    
    origin_x = (210.0 - W) / 2.0 * mm
    origin_y = 30.0 * mm
    
    y_front_tab = origin_y
    y_front_wall = y_front_tab + H * mm
    y_base = y_front_wall + H * mm
    y_back_wall = y_base + L * mm
    y_lid = y_back_wall + H * mm
    y_tuck_wall = y_lid + L * mm
    y_tuck_lip = y_tuck_wall + (H - 2) * mm
    
    bx = origin_x
    bw = W * mm
    bh = H * mm
    bl = L * mm
    
    COLOR_CUT = colors.HexColor("#ff0000")   # Red = Vector Cut
    COLOR_SCORE = colors.HexColor("#0000ff") # Blue = Vector Score/Fold
    
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.setTitle(f"Caja DigiToys Corte Láser 80x80x17 mm - {char_name}")
    
    # Header legend (outside cut area)
    c.setFillColor(colors.HexColor("#111827"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(15 * mm, 286 * mm, f"CORTE LÁSER FAB LAB — CAJA DIGITOYS (80 × 80 × 17 mm) [{char_name}]")
    
    c.setFont("Helvetica-Bold", 7.5)
    c.setStrokeColor(COLOR_CUT)
    c.setLineWidth(1.0)
    c.line(15 * mm, 280 * mm, 25 * mm, 280 * mm)
    c.setFillColor(COLOR_CUT)
    c.drawString(28 * mm, 278.5 * mm, "ROJO: Corte Vectorial (Hairline)")
    
    c.setStrokeColor(COLOR_SCORE)
    c.line(85 * mm, 280 * mm, 95 * mm, 280 * mm)
    c.setFillColor(COLOR_SCORE)
    c.drawString(98 * mm, 278.5 * mm, "AZUL: Marcado / Plecado Vectorial")
    
    # --- 1. BLUE SCORE LINES (FOLD LINES & WRITING FRAME) ---
    c.setStrokeColor(COLOR_SCORE)
    c.setLineWidth(0.5)
    
    # Horizontal fold lines
    c.line(bx, y_front_wall, bx + bw, y_front_wall)
    c.line(bx, y_base, bx + bw, y_base)
    c.line(bx, y_back_wall, bx + bw, y_back_wall)
    c.line(bx, y_lid, bx + bw, y_lid)
    c.line(bx, y_tuck_wall, bx + bw, y_tuck_wall)
    
    # Vertical fold lines
    c.line(bx, y_base, bx, y_base + bl)
    c.line(bx + bw, y_base, bx + bw, y_base + bl)
    c.line(bx - bh, y_base, bx - bh, y_base + bl)
    c.line(bx + bw + bh, y_base, bx + bw + bh, y_base + bl)
    c.line(bx, y_lid, bx, y_lid + bl)
    c.line(bx + bw, y_lid, bx + bw, y_lid + bl)
    
    # BLUE SCORE: Recuadro en la tapa para escribir el nombre a mano
    # Ubicado en la parte superior de la tapa (sobre la ventana)
    c.rect(bx + 8 * mm, y_lid + bl - 16 * mm, bw - 16 * mm, 11 * mm, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(COLOR_SCORE)
    c.drawString(bx + 11 * mm, y_lid + bl - 10 * mm, "DIGITOYS")
    c.line(bx + 26 * mm, y_lid + bl - 10 * mm, bx + bw - 11 * mm, y_lid + bl - 10 * mm)
    
    # --- 2. RED CUT LINES (PERIMETER & SLOTS) ---
    c.setStrokeColor(COLOR_CUT)
    c.setLineWidth(0.8)
    
    p = c.beginPath()
    p.moveTo(bx, y_front_tab)
    p.lineTo(bx + bw, y_front_tab)
    p.lineTo(bx + bw + 4*mm, y_front_wall - 2*mm)
    p.lineTo(bx + bw + bh, y_front_wall)
    
    p.lineTo(bx + bw + bh, y_base)
    p.lineTo(bx + bw + 2*bh, y_base + 3*mm)
    p.lineTo(bx + bw + 2*bh, y_base + bl - 3*mm)
    p.lineTo(bx + bw + bh, y_base + bl)
    
    p.lineTo(bx + bw + bh, y_back_wall + bh)
    p.lineTo(bx + bw, y_back_wall + bh)
    
    p.lineTo(bx + bw + bh - 2*mm, y_lid + 3*mm)
    p.lineTo(bx + bw + bh - 2*mm, y_lid + bl - 3*mm)
    p.lineTo(bx + bw, y_tuck_wall)
    
    p.lineTo(bx + bw - 3*mm, y_tuck_lip)
    p.lineTo(bx + 3*mm, y_tuck_lip)
    p.lineTo(bx, y_tuck_wall)
    
    p.lineTo(bx - (bh - 2*mm), y_lid + bl - 3*mm)
    p.lineTo(bx - (bh - 2*mm), y_lid + 3*mm)
    p.lineTo(bx, y_lid)
    
    p.lineTo(bx, y_back_wall + bh)
    p.lineTo(bx - bh, y_back_wall + bh)
    
    p.lineTo(bx - bh, y_base + bl)
    p.lineTo(bx - 2*bh, y_base + bl - 3*mm)
    p.lineTo(bx - 2*bh, y_base + 3*mm)
    p.lineTo(bx - bh, y_base)
    
    p.lineTo(bx - bh, y_front_wall)
    p.lineTo(bx - 4*mm, y_front_wall - 2*mm)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    
    # Internal corner release cuts
    c.line(bx, y_front_wall, bx - bh, y_front_wall)
    c.line(bx + bw, y_front_wall, bx + bw + bh, y_front_wall)
    c.line(bx, y_back_wall, bx - bh, y_back_wall)
    c.line(bx + bw, y_back_wall, bx + bw + bh, y_back_wall)
    
    # --- RED CUT: VENTANA EN LA TAPA ---
    # La tapa mide bw (80mm) x bl (80mm) y va de y_lid a y_lid + bl
    # El muñeco parado apoya sus pies contra y_lid (que es la pared inferior cuando la caja está en pie)
    # Por lo tanto, la ventana debe nacer a 5 mm arriba de y_lid para coincidir exactamente con los pies!
    if sil_pts is not None:
        # Ventana troquelada con silueta exacta a 52 mm de altura
        p_sil = c.beginPath()
        first = True
        cx_lid = bx + bw / 2.0
        cy_lid_feet = y_lid + 5 * mm # 5 mm de margen sobre los pies
        for pt in sil_pts:
            px = cx_lid + pt[0] * mm
            py = cy_lid_feet + pt[1] * mm
            if first:
                p_sil.moveTo(px, py)
                first = False
            else:
                p_sil.lineTo(px, py)
        p_sil.close()
        c.drawPath(p_sil, stroke=1, fill=0)
    else:
        # Ventana universal: Ventana redondeada vertical (48 mm ancho x 55 mm alto)
        win_w = 48 * mm
        win_h = 55 * mm
        win_x = bx + (bw - win_w) / 2.0
        win_y = y_lid + 5 * mm
        c.roundRect(win_x, win_y, win_w, win_h, 6 * mm, stroke=1, fill=0)
        
    c.save()
    print("PDF generated:", pdf_path)
    
    # Generate clean standard SVG (Inkscape / LightBurn compatible)
    k = 3.779527559 # 1 mm in px
    svg_pts_str = ""
    if sil_pts is not None:
        cx_lid_mm = (bx + bw / 2.0) / mm
        cy_lid_feet_mm = (y_lid + 5 * mm) / mm
        # Convert Cartesian to SVG coordinates (invert Y relative to page_h)
        # In SVG y = 0 is top
        svg_points = []
        for pt in sil_pts:
            sx = (cx_lid_mm + pt[0]) * k
            sy = ((page_h / mm) - (cy_lid_feet_mm + pt[1])) * k
            svg_points.append(f"{sx:.2f},{sy:.2f}")
        svg_pts_str = f'<polygon points="{" ".join(svg_points)}" stroke="#ff0000" stroke-width="0.8" fill="none" />'
    else:
        win_x_mm = (bx + (bw - 48*mm)/2.0) / mm
        win_y_mm = (page_h/mm) - (y_lid/mm + 5 + 55)
        svg_pts_str = f'<rect x="{win_x_mm*k:.2f}" y="{win_y_mm*k:.2f}" width="{48*k:.2f}" height="{55*k:.2f}" rx="{6*k:.2f}" stroke="#ff0000" stroke-width="0.8" fill="none" />'
        
    svg_content = f'''<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {210*k:.2f} {297*k:.2f}" width="210mm" height="297mm">
  <g id="SCORE_AZUL" stroke="#0000ff" stroke-width="0.5" fill="none">
    <!-- Dobleces horizontales -->
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_front_wall/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_front_wall/mm))*k:.2f}" />
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_base/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_base/mm))*k:.2f}" />
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_back_wall/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_back_wall/mm))*k:.2f}" />
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_lid/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_lid/mm))*k:.2f}" />
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_tuck_wall/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_tuck_wall/mm))*k:.2f}" />
    <!-- Dobleces verticales -->
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_base/mm))*k:.2f}" x2="{(bx/mm)*k:.2f}" y2="{((page_h/mm)-(y_base/mm+bl/mm))*k:.2f}" />
    <line x1="{((bx+bw)/mm)*k:.2f}" y1="{((page_h/mm)-(y_base/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_base/mm+bl/mm))*k:.2f}" />
    <line x1="{((bx-bh)/mm)*k:.2f}" y1="{((page_h/mm)-(y_base/mm))*k:.2f}" x2="{((bx-bh)/mm)*k:.2f}" y2="{((page_h/mm)-(y_base/mm+bl/mm))*k:.2f}" />
    <line x1="{((bx+bw+bh)/mm)*k:.2f}" y1="{((page_h/mm)-(y_base/mm))*k:.2f}" x2="{((bx+bw+bh)/mm)*k:.2f}" y2="{((page_h/mm)-(y_base/mm+bl/mm))*k:.2f}" />
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_lid/mm))*k:.2f}" x2="{(bx/mm)*k:.2f}" y2="{((page_h/mm)-(y_lid/mm+bl/mm))*k:.2f}" />
    <line x1="{((bx+bw)/mm)*k:.2f}" y1="{((page_h/mm)-(y_lid/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_lid/mm+bl/mm))*k:.2f}" />
    <!-- Recuadro para escribir nombre -->
    <rect x="{((bx+8*mm)/mm)*k:.2f}" y="{((page_h/mm)-(y_lid/mm+bl/mm-5))*k:.2f}" width="{(64)*k:.2f}" height="{(11)*k:.2f}" />
  </g>
  <g id="CUT_ROJO" stroke="#ff0000" stroke-width="0.8" fill="none">
    <!-- Ventana -->
    {svg_pts_str}
    <!-- Cortes de liberación -->
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_front_wall/mm))*k:.2f}" x2="{((bx-bh)/mm)*k:.2f}" y2="{((page_h/mm)-(y_front_wall/mm))*k:.2f}" />
    <line x1="{((bx+bw)/mm)*k:.2f}" y1="{((page_h/mm)-(y_front_wall/mm))*k:.2f}" x2="{((bx+bw+bh)/mm)*k:.2f}" y2="{((page_h/mm)-(y_front_wall/mm))*k:.2f}" />
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_back_wall/mm))*k:.2f}" x2="{((bx-bh)/mm)*k:.2f}" y2="{((page_h/mm)-(y_back_wall/mm))*k:.2f}" />
    <line x1="{((bx+bw)/mm)*k:.2f}" y1="{((page_h/mm)-(y_back_wall/mm))*k:.2f}" x2="{((bx+bw+bh)/mm)*k:.2f}" y2="{((page_h/mm)-(y_back_wall/mm))*k:.2f}" />
  </g>
</svg>'''
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print("SVG generated:", svg_path)

def main():
    svg_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\01_siluetas_svg"
    out_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\04_packaging_box"
    
    # 1. Clean old files in packaging_box
    old_files = glob.glob(os.path.join(out_dir, "*80x80x16*"))
    for of in old_files:
        try:
            os.remove(of)
            print("Removed old file:", of)
        except Exception:
            pass
            
    # 2. Generate Universal 17mm Box
    generate_box_17mm(None, "Universal")
    
    # 3. Generate Dino Bebé 1 Box with Die-Cut Silhouette Window
    dino_svg = os.path.join(svg_dir, "01_dino_bebe_1.svg")
    pts_dino, _, _ = extract_scaled_points(dino_svg, 52.0)
    generate_box_17mm(pts_dino, "01_Dino_Bebe_1")

if __name__ == "__main__":
    main()
