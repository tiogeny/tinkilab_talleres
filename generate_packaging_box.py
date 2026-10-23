import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Group

def generate_packaging_box():
    out_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\04_packaging_box"
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, "caja_empaque_80x80x16_A4.pdf")
    svg_path = os.path.join(out_dir, "caja_empaque_80x80x16_A4.svg")
    
    # A4 Dimensions in points (1 mm = 72 / 25.4 = 2.834645669 pt)
    mm = 72.0 / 25.4
    page_w = 210.0 * mm
    page_h = 297.0 * mm
    
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.setTitle("Plantilla Caja de Empaque DigiToy - 80x80x16 mm")
    
    # Box parameters in mm
    W = 80.0 # Width
    L = 80.0 # Length
    H = 16.0 # Height
    flap_lip = 12.0 # Tuck flap
    dust_flap_w = 14.0 # Dust flaps
    
    # Center on A4 page
    # Total footprint in X: W + 2*H + 2*H (with roll-over / side tabs) ~ 80 + 32 + 28 = 140 mm
    # Total footprint in Y: L + 2*H + L + H + flap_lip + H = 80 + 32 + 80 + 16 + 12 + 16 = 236 mm
    total_w = W + 2 * (H + dust_flap_w)
    total_h = L + 2 * H + L + H + flap_lip + H
    
    origin_x = (210.0 - W) / 2.0 * mm # Left edge of base
    origin_y = 35.0 * mm # Bottom edge of front tab
    
    # Coordinates in mm from origin
    # Base is at x in [0, W], y in [front_wall_y, front_wall_y + L]
    # Let's define Y levels:
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
    
    # Header & Instructions (Bandera Blanca / Clean & Pro)
    c.setFillColor(colors.HexColor("#111827"))
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, 282 * mm, "PLANTILLA DE EMPAQUE DIGITOY")
    
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#4b5563"))
    c.drawString(20 * mm, 276 * mm, "Formato: Caja plegable para figura de 70x70x10 mm | Dimensiones internas: 80 × 80 × 16 mm")
    
    # Legend
    # Solid black = Cut line
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.2)
    c.line(135 * mm, 281 * mm, 150 * mm, 281 * mm)
    c.drawString(153 * mm, 279 * mm, "Línea de corte continuo")
    
    # Dashed = Fold line
    c.setStrokeColor(colors.HexColor("#0284c7")) # Cyan / blue dashed
    c.setLineWidth(0.8)
    c.setDash(3, 2)
    c.line(135 * mm, 274 * mm, 150 * mm, 274 * mm)
    c.setFillColor(colors.HexColor("#0284c7"))
    c.drawString(153 * mm, 272 * mm, "Línea de doblado / pliegue")
    
    c.setDash() # Reset dash
    
    # --- DRAW CUT OUTLINE (Outer boundary) ---
    p = c.beginPath()
    # Start at bottom-left of front wall
    p.moveTo(bx, y_front_tab)
    p.lineTo(bx + bw, y_front_tab)
    p.lineTo(bx + bw + 4*mm, y_front_wall - 2*mm)
    p.lineTo(bx + bw + bh, y_front_wall)
    
    # Right side wall base
    p.lineTo(bx + bw + bh, y_base)
    # Right side wall outer roll-over flap
    p.lineTo(bx + bw + 2*bh, y_base + 3*mm)
    p.lineTo(bx + bw + 2*bh, y_base + bl - 3*mm)
    p.lineTo(bx + bw + bh, y_base + bl)
    
    # Right side dust flap (back wall)
    p.lineTo(bx + bw + bh, y_back_wall + bh)
    p.lineTo(bx + bw, y_back_wall + bh)
    
    # Lid right side flap
    p.lineTo(bx + bw + bh - 2*mm, y_lid + 3*mm)
    p.lineTo(bx + bw + bh - 2*mm, y_lid + bl - 3*mm)
    p.lineTo(bx + bw, y_tuck_wall)
    
    # Tuck flap & Lip top
    p.lineTo(bx + bw - 3*mm, y_tuck_lip)
    p.lineTo(bx + 3*mm, y_tuck_lip)
    p.lineTo(bx, y_tuck_wall)
    
    # Lid left side flap
    p.lineTo(bx - (bh - 2*mm), y_lid + bl - 3*mm)
    p.lineTo(bx - (bh - 2*mm), y_lid + 3*mm)
    p.lineTo(bx, y_lid)
    
    # Left side dust flap (back wall)
    p.lineTo(bx, y_back_wall + bh)
    p.lineTo(bx - bh, y_back_wall + bh)
    
    # Left side wall outer roll-over flap
    p.lineTo(bx - bh, y_base + bl)
    p.lineTo(bx - 2*bh, y_base + bl - 3*mm)
    p.lineTo(bx - 2*bh, y_base + 3*mm)
    p.lineTo(bx - bh, y_base)
    
    # Left front corner
    p.lineTo(bx - bh, y_front_wall)
    p.lineTo(bx - 4*mm, y_front_wall - 2*mm)
    p.close()
    
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.2)
    c.drawPath(p, stroke=1, fill=0)
    
    # --- DRAW FOLD LINES (Dashed blue) ---
    c.setStrokeColor(colors.HexColor("#0284c7"))
    c.setLineWidth(0.8)
    c.setDash(3, 2)
    
    # Horizontal folds
    c.line(bx, y_front_wall, bx + bw, y_front_wall)
    c.line(bx, y_base, bx + bw, y_base)
    c.line(bx, y_back_wall, bx + bw, y_back_wall)
    c.line(bx, y_lid, bx + bw, y_lid)
    c.line(bx, y_tuck_wall, bx + bw, y_tuck_wall)
    
    # Vertical folds (sides of base)
    c.line(bx, y_base, bx, y_base + bl)
    c.line(bx + bw, y_base, bx + bw, y_base + bl)
    
    # Vertical folds (roll-over flaps)
    c.line(bx - bh, y_base, bx - bh, y_base + bl)
    c.line(bx + bw + bh, y_base, bx + bw + bh, y_base + bl)
    
    # Vertical folds (lid side flaps)
    c.line(bx, y_lid, bx, y_lid + bl)
    c.line(bx + bw, y_lid, bx + bw, y_lid + bl)
    
    # Small inner cuts for corner flaps
    c.setDash() # Solid cut
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    c.line(bx, y_front_wall, bx - bh, y_front_wall)
    c.line(bx + bw, y_front_wall, bx + bw + bh, y_front_wall)
    c.line(bx, y_back_wall, bx - bh, y_back_wall)
    c.line(bx + bw, y_back_wall, bx + bw + bh, y_back_wall)
    
    # --- GRAPHICS & LABELS ON LID (TAPA SUPERIOR) ---
    # The lid is located at y in [y_lid, y_lid + bl], x in [bx, bx + bw]
    # We place a clean, minimalist design frame on the lid
    c.setStrokeColor(colors.HexColor("#9ca3af"))
    c.setLineWidth(0.6)
    c.rect(bx + 6*mm, y_lid + 6*mm, bw - 12*mm, bl - 12*mm)
    
    c.setFillColor(colors.HexColor("#111827"))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(bx + bw/2.0, y_lid + bl - 14*mm, "DIGITOY COLLECTIBLE")
    
    c.setFont("Helvetica", 6.5)
    c.setFillColor(colors.HexColor("#6b7280"))
    c.drawCentredString(bx + bw/2.0, y_lid + bl - 18*mm, "EDICIÓN TALLER DE FABRICACIÓN DIGITAL")
    
    # Box for child drawing/sticker or window
    c.setStrokeColor(colors.HexColor("#d1d5db"))
    c.setLineWidth(0.5)
    c.setDash(2, 2)
    c.roundRect(bx + 14*mm, y_lid + 22*mm, bw - 28*mm, 28*mm, 3*mm)
    c.setFont("Helvetica", 6)
    c.setFillColor(colors.HexColor("#9ca3af"))
    c.drawCentredString(bx + bw/2.0, y_lid + 34*mm, "[ ESPACIO PARA FIRMA / DIBUJO ]")
    c.setDash()
    
    # Form fields on lid
    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(colors.HexColor("#374151"))
    c.drawString(bx + 10*mm, y_lid + 15*mm, "CREADOR(A):")
    c.setStrokeColor(colors.HexColor("#9ca3af"))
    c.setLineWidth(0.5)
    c.line(bx + 26*mm, y_lid + 14*mm, bx + bw - 10*mm, y_lid + 14*mm)
    
    c.drawString(bx + 10*mm, y_lid + 10*mm, "CRIATURA:")
    c.line(bx + 24*mm, y_lid + 9*mm, bx + bw - 10*mm, y_lid + 9*mm)
    
    # Label inside bottom base
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#9ca3af"))
    c.drawCentredString(bx + bw/2.0, y_base + bl/2.0, "BASE INTERIOR — COLOCAR FIGURA 3D AQUÍ")
    
    # Footer guide notes
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#6b7280"))
    c.drawString(20 * mm, 16 * mm, "Instrucciones de armado:")
    c.drawString(20 * mm, 12 * mm, "1. Cortar por la línea negra continua exterior.")
    c.drawString(20 * mm, 8 * mm, "2. Marcar con una regla y la punta de un bolígrafo sin tinta las líneas azules punteadas para doblar con facilidad.")
    c.drawString(110 * mm, 12 * mm, "3. Doblar las paredes hacia adentro. Levantar laterales y doblar solapas.")
    c.drawString(110 * mm, 8 * mm, "4. Introducir tu DigiToy 3D y cerrar la tapa superior.")
    
    c.save()
    print("Packaging PDF generated:", pdf_path)
    
    # Also generate matching SVG for laser cutting or digital viewing
    # Simple SVG template
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 595.28 841.89" width="210mm" height="297mm">
  <style>
    .cut {{ stroke: #000000; stroke-width: 1.5; fill: none; }}
    .fold {{ stroke: #0284c7; stroke-width: 1.0; stroke-dasharray: 4, 3; fill: none; }}
    .text {{ font-family: Helvetica, Arial, sans-serif; fill: #374151; }}
  </style>
  <text x="56.7" y="56.7" class="text" font-size="14" font-weight="bold">PLANTILLA DE EMPAQUE DIGITOY (80x80x16 mm)</text>
  <text x="56.7" y="73.7" class="text" font-size="9" fill="#6b7280">Corte continuo (Negro) | Pliegue (Azul punteado)</text>
  <!-- Cut and Fold vectors -->
  <rect x="{bx}" y="{y_base}" width="{bw}" height="{bl}" class="fold" />
  <rect x="{bx}" y="{y_lid}" width="{bw}" height="{bl}" class="fold" />
</svg>'''
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print("Packaging SVG generated:", svg_path)

if __name__ == "__main__":
    generate_packaging_box()
