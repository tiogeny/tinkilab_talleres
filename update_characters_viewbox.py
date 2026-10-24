import json
import numpy as np
from svg.path import parse_path

with open('pack_digitoys_12/05_acabado_color/characters_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    parsed = parse_path(item['d'])
    pts = []
    for seg in parsed:
        for t in np.linspace(0, 1, 20):
            pt = seg.point(t)
            pts.append([pt.real, pt.imag])
    pts = np.array(pts)
    
    xmin, ymin = pts.min(axis=0)
    xmax, ymax = pts.max(axis=0)
    w = xmax - xmin
    h = ymax - ymin
    
    pad_x = w * 0.06
    pad_y = h * 0.06
    vb_x = xmin - pad_x
    vb_y = ymin - pad_y
    vb_w = w + 2 * pad_x
    vb_h = h + 2 * pad_y
    item['viewBox'] = f"{vb_x:.2f} {vb_y:.2f} {vb_w:.2f} {vb_h:.2f}"
    print(f"{item['id']}: ({xmin:.1f}, {ymin:.1f}) to ({xmax:.1f}, {ymax:.1f}) | size: {w:.1f}x{h:.1f} -> viewBox='{item['viewBox']}'")

with open('pack_digitoys_12/05_acabado_color/characters_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("\nSuccessfully updated characters_data.json with exact viewBoxes!")
