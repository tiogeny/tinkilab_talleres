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
    
    cx = (pts[:, 0].max() + pts[:, 0].min()) / 2.0
    min_y = pts[:, 1].min()
    pts[:, 0] -= cx
    pts[:, 1] -= min_y # 0 is at bottom (feet)
    
    return pts, w * scale, target_height_mm

def generate_official_laser_box():
    out_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\04_packaging_box"
    os.makedirs(out_dir, exist_ok=True)
    
    pdf_path = os.path.join(out_dir, "caja_laser_80x80x17_oficial.pdf")
    svg_path = os.path.join(out_dir, "caja_laser_80x80x17_oficial.svg")
    
    mm = 72.0 / 25.4
    page_w = 210.0 * mm
    page_h = 297.0 * mm
    
    W = 80.0
    L = 80.0
    H = 17.0
    
    origin_x = (210.0 - W) / 2.0 * mm
    origin_y = 32.0 * mm
    
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
    
    COLOR_CUT = colors.HexColor("#ff0000")     # Red = Vector Cut
    COLOR_SCORE = colors.HexColor("#0000ff")   # Blue = Vector Score/Fold
    COLOR_ENGRAVE = colors.HexColor("#000000") # Black = Raster Engrave
    
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.setTitle("Caja DigiToys Corte Láser Oficial - 80x80x17 mm")
    
    # Leyenda técnica
    c.setFillColor(colors.HexColor("#111827"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(15 * mm, 287 * mm, "PLANTILLA OFICIAL CORTE LÁSER — CAJA DIGITOYS (80 × 80 × 17 mm)")
    
    c.setFont("Helvetica-Bold", 7)
    c.setStrokeColor(COLOR_CUT)
    c.setLineWidth(1.0)
    c.line(15 * mm, 281 * mm, 25 * mm, 281 * mm)
    c.setFillColor(COLOR_CUT)
    c.drawString(28 * mm, 279.5 * mm, "ROJO: Corte Vectorial (Hairline)")
    
    c.setStrokeColor(COLOR_SCORE)
    c.line(85 * mm, 281 * mm, 95 * mm, 281 * mm)
    c.setFillColor(COLOR_SCORE)
    c.drawString(98 * mm, 279.5 * mm, "AZUL: Marcado / Plecado Vectorial")
    
    c.setFillColor(COLOR_ENGRAVE)
    c.rect(155 * mm, 279 * mm, 5 * mm, 4 * mm, fill=1, stroke=0)
    c.drawString(163 * mm, 279.5 * mm, "NEGRO: Grabado Láser (Raster)")
    
    # --- 1. LÍNEAS DE MARCADO / PLEGADO (AZUL) ---
    c.setStrokeColor(COLOR_SCORE)
    c.setLineWidth(0.5)
    
    # Dobleces horizontales
    c.line(bx, y_front_wall, bx + bw, y_front_wall)
    c.line(bx, y_base, bx + bw, y_base)
    c.line(bx, y_back_wall, bx + bw, y_back_wall)
    c.line(bx, y_lid, bx + bw, y_lid)
    c.line(bx, y_tuck_wall, bx + bw, y_tuck_wall)
    
    # Dobleces verticales
    c.line(bx, y_base, bx, y_base + bl)
    c.line(bx + bw, y_base, bx + bw, y_base + bl)
    c.line(bx - bh, y_base, bx - bh, y_base + bl)
    c.line(bx + bw + bh, y_base, bx + bw + bh, y_base + bl)
    c.line(bx, y_lid, bx, y_lid + bl)
    c.line(bx + bw, y_lid, bx + bw, y_lid + bl)
    
    # --- 2. GRABADO LÁSER NEGRO (LOGO DIGITOYS SUTIL) ---
    c.setFillColor(COLOR_ENGRAVE)
    c.setFont("Helvetica-Bold", 10)
    # Grabado en la pestaña frontal o tapa
    c.drawCentredString(bx + bw / 2.0, y_lid + bl - 9 * mm, "DIGITOYS")
    
    # --- 3. CONTORNO EXTERIOR DE CORTE LIMPIO (ROJO - SIN LÍNEAS HORIZONTALES CRUZADAS) ---
    c.setStrokeColor(COLOR_CUT)
    c.setLineWidth(0.8)
    
    p = c.beginPath()
    # Pestaña frontal inferior
    p.moveTo(bx, y_front_tab)
    p.lineTo(bx + bw, y_front_tab)
    p.lineTo(bx + bw, y_front_wall)
    p.lineTo(bx + bw + bh, y_front_wall)
    
    # Pared lateral derecha
    p.lineTo(bx + bw + bh, y_base)
    p.lineTo(bx + bw + 2*bh, y_base + 3*mm)
    p.lineTo(bx + bw + 2*bh, y_base + bl - 3*mm)
    p.lineTo(bx + bw + bh, y_base + bl)
    
    # Aleta trasera derecha
    p.lineTo(bx + bw + bh, y_back_wall + bh)
    p.lineTo(bx + bw, y_back_wall + bh)
    
    # Aleta tapa derecha
    p.lineTo(bx + bw + bh - 2*mm, y_lid + 3*mm)
    p.lineTo(bx + bw + bh - 2*mm, y_lid + bl - 3*mm)
    p.lineTo(bx + bw, y_tuck_wall)
    
    # Lengüeta superior de cierre
    p.lineTo(bx + bw - 4*mm, y_tuck_lip)
    p.lineTo(bx + 4*mm, y_tuck_lip)
    p.lineTo(bx, y_tuck_wall)
    
    # Aleta tapa izquierda
    p.lineTo(bx - (bh - 2*mm), y_lid + bl - 3*mm)
    p.lineTo(bx - (bh - 2*mm), y_lid + 3*mm)
    p.lineTo(bx, y_lid)
    
    # Aleta trasera izquierda
    p.lineTo(bx, y_back_wall + bh)
    p.lineTo(bx - bh, y_back_wall + bh)
    
    # Pared lateral izquierda
    p.lineTo(bx - bh, y_base + bl)
    p.lineTo(bx - 2*bh, y_base + bl - 3*mm)
    p.lineTo(bx - 2*bh, y_base + 3*mm)
    p.lineTo(bx - bh, y_base)
    
    # Pestaña frontal izquierda
    p.lineTo(bx - bh, y_front_wall)
    p.lineTo(bx, y_front_wall)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    
    # Cortes de liberación verticales precisos (solo entre aletas y pared base)
    c.line(bx, y_base, bx, y_front_wall)
    c.line(bx + bw, y_base, bx + bw, y_front_wall)
    c.line(bx, y_base + bl, bx, y_back_wall + bh)
    c.line(bx + bw, y_base + bl, bx + bw, y_back_wall + bh)
    
    # --- VENTANA TROQUELADA EN LA TAPA (ROJO - ALINEADA CON LOS PIES) ---
    svg_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\01_siluetas_svg"
    dino_svg = os.path.join(svg_dir, "01_dino_bebe_1.svg")
    sil_pts, _, _ = extract_scaled_points(dino_svg, 52.0)
    
    p_sil = c.beginPath()
    first = True
    cx_lid = bx + bw / 2.0
    cy_lid_feet = y_lid + 5 * mm
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
    
    c.save()
    print("Clean Laser Box PDF generated:", pdf_path)
    
    # Generate matching clean SVG
    k = 3.779527559
    cx_lid_mm = (bx + bw / 2.0) / mm
    cy_lid_feet_mm = (y_lid + 5 * mm) / mm
    svg_points = []
    for pt in sil_pts:
        sx = (cx_lid_mm + pt[0]) * k
        sy = ((page_h / mm) - (cy_lid_feet_mm + pt[1])) * k
        svg_points.append(f"{sx:.2f},{sy:.2f}")
    svg_pts_str = f'<polygon points="{" ".join(svg_points)}" stroke="#ff0000" stroke-width="0.8" fill="none" />'
    
    svg_content = f'''<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {210*k:.2f} {297*k:.2f}" width="210mm" height="297mm">
  <g id="SCORE_AZUL" stroke="#0000ff" stroke-width="0.5" fill="none">
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_front_wall/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_front_wall/mm))*k:.2f}" />
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_base/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_base/mm))*k:.2f}" />
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_back_wall/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_back_wall/mm))*k:.2f}" />
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_lid/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_lid/mm))*k:.2f}" />
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_tuck_wall/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_tuck_wall/mm))*k:.2f}" />
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_base/mm))*k:.2f}" x2="{(bx/mm)*k:.2f}" y2="{((page_h/mm)-(y_base/mm+bl/mm))*k:.2f}" />
    <line x1="{((bx+bw)/mm)*k:.2f}" y1="{((page_h/mm)-(y_base/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_base/mm+bl/mm))*k:.2f}" />
    <line x1="{((bx-bh)/mm)*k:.2f}" y1="{((page_h/mm)-(y_base/mm))*k:.2f}" x2="{((bx-bh)/mm)*k:.2f}" y2="{((page_h/mm)-(y_base/mm+bl/mm))*k:.2f}" />
    <line x1="{((bx+bw+bh)/mm)*k:.2f}" y1="{((page_h/mm)-(y_base/mm))*k:.2f}" x2="{((bx+bw+bh)/mm)*k:.2f}" y2="{((page_h/mm)-(y_base/mm+bl/mm))*k:.2f}" />
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_lid/mm))*k:.2f}" x2="{(bx/mm)*k:.2f}" y2="{((page_h/mm)-(y_lid/mm+bl/mm))*k:.2f}" />
    <line x1="{((bx+bw)/mm)*k:.2f}" y1="{((page_h/mm)-(y_lid/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_lid/mm+bl/mm))*k:.2f}" />
  </g>
  <g id="ENGRAVE_NEGRO" font-family="Helvetica, Arial, sans-serif" fill="#000000">
    <text x="{((bx+bw/2.0)/mm)*k:.2f}" y="{((page_h/mm)-(y_lid/mm+bl/mm-9))*k:.2f}" font-size="10" font-weight="bold" text-anchor="middle">DIGITOYS</text>
  </g>
  <g id="CUT_ROJO" stroke="#ff0000" stroke-width="0.8" fill="none">
    {svg_pts_str}
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_base/mm))*k:.2f}" x2="{(bx/mm)*k:.2f}" y2="{((page_h/mm)-(y_front_wall/mm))*k:.2f}" />
    <line x1="{((bx+bw)/mm)*k:.2f}" y1="{((page_h/mm)-(y_base/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_front_wall/mm))*k:.2f}" />
    <line x1="{(bx/mm)*k:.2f}" y1="{((page_h/mm)-(y_base/mm+bl/mm))*k:.2f}" x2="{(bx/mm)*k:.2f}" y2="{((page_h/mm)-(y_back_wall/mm+bh/mm))*k:.2f}" />
    <line x1="{((bx+bw)/mm)*k:.2f}" y1="{((page_h/mm)-(y_base/mm+bl/mm))*k:.2f}" x2="{((bx+bw)/mm)*k:.2f}" y2="{((page_h/mm)-(y_back_wall/mm+bh/mm))*k:.2f}" />
  </g>
</svg>'''
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print("Clean Laser Box SVG generated:", svg_path)

if __name__ == "__main__":
    generate_official_laser_box()
