import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def generate_laser_box():
    out_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\04_packaging_box"
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, "caja_laser_80x80x16_A4.pdf")
    svg_path = os.path.join(out_dir, "caja_laser_80x80x16_A4.svg")
    
    mm = 72.0 / 25.4
    page_w = 210.0 * mm
    page_h = 297.0 * mm
    
    # Box parameters in mm
    W = 80.0 # Width
    L = 80.0 # Length
    H = 16.0 # Height
    flap_lip = 12.0
    
    origin_x = (210.0 - W) / 2.0 * mm
    origin_y = 35.0 * mm
    
    y_front_tab = origin_y
    y_front_wall = y_front_tab + H * mm
    y_base = y_front_wall + H * mm
    y_back_wall = y_base + L * mm
    y_lid = y_back_wall + H * mm
    y_tuck_wall = y_lid + L * mm
    y_tuck_lip = y_tuck_wall + H * mm
    
    bx = origin_x
    bw = W * mm
    bh = H * mm
    bl = L * mm
    
    # Laser Colors
    COLOR_CUT = colors.HexColor("#ff0000")   # Red = Cut
    COLOR_SCORE = colors.HexColor("#0000ff") # Blue = Vector score/fold
    COLOR_ENGRAVE = colors.HexColor("#000000") # Black = Engrave
    
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.setTitle("Caja de Empaque DigiToy - Corte Láser (Fab Lab)")
    
    # Header legend (Outside cutting boundary)
    c.setFillColor(colors.HexColor("#111827"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(15 * mm, 285 * mm, "PLANTILLA DE CORTE LÁSER — CAJA DIGITOY (80 × 80 × 16 mm)")
    
    # Legend boxes
    c.setFont("Helvetica-Bold", 7.5)
    # Red Cut
    c.setStrokeColor(COLOR_CUT)
    c.setLineWidth(1.0)
    c.line(15 * mm, 278 * mm, 25 * mm, 278 * mm)
    c.setFillColor(COLOR_CUT)
    c.drawString(28 * mm, 276.5 * mm, "ROJO: Corte Vectorial (Atraviesa)")
    
    # Blue Score
    c.setStrokeColor(COLOR_SCORE)
    c.line(85 * mm, 278 * mm, 95 * mm, 278 * mm)
    c.setFillColor(COLOR_SCORE)
    c.drawString(98 * mm, 276.5 * mm, "AZUL: Marcado / Plecado (Dobleces)")
    
    # Black Engrave
    c.setFillColor(COLOR_ENGRAVE)
    c.rect(155 * mm, 276 * mm, 6 * mm, 4 * mm, fill=1, stroke=0)
    c.drawString(164 * mm, 276.5 * mm, "NEGRO: Grabado Láser")
    
    # --- 1. BLUE SCORE LINES (FOLD LINES) ---
    c.setStrokeColor(COLOR_SCORE)
    c.setLineWidth(0.5) # Fine score line
    
    # Horizontal score lines
    c.line(bx, y_front_wall, bx + bw, y_front_wall)
    c.line(bx, y_base, bx + bw, y_base)
    c.line(bx, y_back_wall, bx + bw, y_back_wall)
    c.line(bx, y_lid, bx + bw, y_lid)
    c.line(bx, y_tuck_wall, bx + bw, y_tuck_wall)
    
    # Vertical score lines (base side walls)
    c.line(bx, y_base, bx, y_base + bl)
    c.line(bx + bw, y_base, bx + bw, y_base + bl)
    
    # Vertical score lines (outer roll-over flaps)
    c.line(bx - bh, y_base, bx - bh, y_base + bl)
    c.line(bx + bw + bh, y_base, bx + bw + bh, y_base + bl)
    
    # Vertical score lines (lid side flaps)
    c.line(bx, y_lid, bx, y_lid + bl)
    c.line(bx + bw, y_lid, bx + bw, y_lid + bl)
    
    # --- 2. RED CUT LINES (PERIMETER & SLOTS) ---
    c.setStrokeColor(COLOR_CUT)
    c.setLineWidth(0.8)
    
    # Outer cut perimeter
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
    
    # Tuck flap & Lip top
    p.lineTo(bx + bw - 3*mm, y_tuck_lip)
    p.lineTo(bx + 3*mm, y_tuck_lip)
    p.lineTo(bx, y_tuck_wall)
    
    # Left lid flap
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
    
    # Internal corner release cuts (Red)
    c.line(bx, y_front_wall, bx - bh, y_front_wall)
    c.line(bx + bw, y_front_wall, bx + bw + bh, y_front_wall)
    c.line(bx, y_back_wall, bx - bh, y_back_wall)
    c.line(bx + bw, y_back_wall, bx + bw + bh, y_back_wall)
    
    # RED CUT: Ventana calada opcional en la tapa (44 x 44 mm centrada)
    # Permite ver la carita del personaje desde afuera
    win_w = 44 * mm
    win_h = 44 * mm
    win_x = bx + (bw - win_w) / 2.0
    win_y = y_lid + (bl - win_h) / 2.0 + 3 * mm
    c.roundRect(win_x, win_y, win_w, win_h, 4 * mm, stroke=1, fill=0)
    
    # --- 3. BLACK ENGRAVE (GRABADO LÁSER MÍNIMO Y ELEGANTE) ---
    c.setFillColor(COLOR_ENGRAVE)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(bx + bw/2.0, y_lid + bl - 7 * mm, "DIGITOY")
    
    c.setFont("Helvetica", 6)
    c.drawString(bx + 12 * mm, y_lid + 7 * mm, "NOMBRE:")
    c.setStrokeColor(COLOR_ENGRAVE)
    c.setLineWidth(0.4)
    c.line(bx + 26 * mm, y_lid + 6.5 * mm, bx + bw - 12 * mm, y_lid + 6.5 * mm)
    
    c.save()
    print("Laser Box PDF generated:", pdf_path)
    
    # Export clean laser SVG (Standard px = mm * 3.779527559)
    k = 3.779527559
    svg_content = f'''<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {210*k} {297*k}" width="210mm" height="297mm">
  <g id="LEGEND" font-family="Helvetica, Arial, sans-serif" font-size="8">
    <text x="15mm" y="15mm" font-weight="bold" fill="#000000">CORTE LÁSER FAB LAB - CAJA DIGITOY (80x80x16 mm)</text>
    <line x1="15mm" y1="20mm" x2="25mm" y2="20mm" stroke="#ff0000" stroke-width="0.8" />
    <text x="28mm" y="22mm" fill="#ff0000">ROJO: Corte Vectorial (Hairline 0.01 mm)</text>
    <line x1="85mm" y1="20mm" x2="95mm" y2="20mm" stroke="#0000ff" stroke-width="0.5" />
    <text x="98mm" y="22mm" fill="#0000ff">AZUL: Marcado / Plecado Vectorial</text>
  </g>
  <!-- MARCADOS (AZUL) -->
  <g id="SCORE_AZUL" stroke="#0000ff" stroke-width="0.5" fill="none">
    <line x1="{bx/mm}mm" y1="{y_front_wall/mm}mm" x2="{(bx+bw)/mm}mm" y2="{y_front_wall/mm}mm" />
    <line x1="{bx/mm}mm" y1="{y_base/mm}mm" x2="{(bx+bw)/mm}mm" y2="{y_base/mm}mm" />
    <line x1="{bx/mm}mm" y1="{y_back_wall/mm}mm" x2="{(bx+bw)/mm}mm" y2="{y_back_wall/mm}mm" />
    <line x1="{bx/mm}mm" y1="{y_lid/mm}mm" x2="{(bx+bw)/mm}mm" y2="{y_lid/mm}mm" />
    <line x1="{bx/mm}mm" y1="{y_tuck_wall/mm}mm" x2="{(bx+bw)/mm}mm" y2="{y_tuck_wall/mm}mm" />
    <line x1="{bx/mm}mm" y1="{y_base/mm}mm" x2="{bx/mm}mm" y2="{(y_base+bl)/mm}mm" />
    <line x1="{(bx+bw)/mm}mm" y1="{y_base/mm}mm" x2="{(bx+bw)/mm}mm" y2="{(y_base+bl)/mm}mm" />
    <line x1="{(bx-bh)/mm}mm" y1="{y_base/mm}mm" x2="{(bx-bh)/mm}mm" y2="{(y_base+bl)/mm}mm" />
    <line x1="{(bx+bw+bh)/mm}mm" y1="{y_base/mm}mm" x2="{(bx+bw+bh)/mm}mm" y2="{(y_base+bl)/mm}mm" />
    <line x1="{bx/mm}mm" y1="{y_lid/mm}mm" x2="{bx/mm}mm" y2="{(y_lid+bl)/mm}mm" />
    <line x1="{(bx+bw)/mm}mm" y1="{y_lid/mm}mm" x2="{(bx+bw)/mm}mm" y2="{(y_lid+bl)/mm}mm" />
  </g>
  <!-- CORTES (ROJO) -->
  <g id="CUT_ROJO" stroke="#ff0000" stroke-width="0.8" fill="none">
    <line x1="{bx/mm}mm" y1="{y_front_wall/mm}mm" x2="{(bx-bh)/mm}mm" y2="{y_front_wall/mm}mm" />
    <line x1="{(bx+bw)/mm}mm" y1="{y_front_wall/mm}mm" x2="{(bx+bw+bh)/mm}mm" y2="{y_front_wall/mm}mm" />
    <line x1="{bx/mm}mm" y1="{y_back_wall/mm}mm" x2="{(bx-bh)/mm}mm" y2="{y_back_wall/mm}mm" />
    <line x1="{(bx+bw)/mm}mm" y1="{y_back_wall/mm}mm" x2="{(bx+bw+bh)/mm}mm" y2="{y_back_wall/mm}mm" />
    <!-- Ventana calada en tapa -->
    <rect x="{win_x/mm}mm" y="{win_y/mm}mm" width="{win_w/mm}mm" height="{win_h/mm}mm" rx="4mm" />
  </g>
  <!-- GRABADO (NEGRO) -->
  <g id="ENGRAVE_NEGRO" font-family="Helvetica, Arial, sans-serif" fill="#000000">
    <text x="{(bx+bw/2.0)/mm}mm" y="{(y_lid+bl-7*mm)/mm}mm" font-size="8" font-weight="bold" text-anchor="middle">DIGITOY</text>
  </g>
</svg>'''
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print("Laser Box SVG generated:", svg_path)

if __name__ == "__main__":
    generate_laser_box()
