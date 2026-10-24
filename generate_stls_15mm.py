import glob
import os
import xml.etree.ElementTree as ET
import numpy as np
import trimesh
import mapbox_earcut as earcut
from shapely.geometry import Polygon, MultiPolygon
from svg.path import parse_path

def resample_polygon(poly, n_points=360):
    exterior = poly.exterior
    total_len = exterior.length
    dists = np.linspace(0, total_len, n_points, endpoint=False)
    pts = [exterior.interpolate(d) for d in dists]
    return np.array([[p.x, p.y] for p in pts])

def align_points(pts_prev, pts_curr):
    dists = np.sum((pts_curr - pts_prev[0])**2, axis=1)
    best_idx = np.argmin(dists)
    return np.roll(pts_curr, -best_idx, axis=0)

def generate_3d_stl_15mm(svg_path, out_stl_path, target_height=70.0, total_thickness=15.0, fillet_radius=1.2, n_points=360, n_fillet_steps=8):
    tree = ET.parse(svg_path)
    paths = tree.getroot().findall('.//{http://www.w3.org/2000/svg}path')
    if not paths:
        raise ValueError(f"No path found in {svg_path}")
        
    best_p = max(paths, key=lambda p: len(p.get('d', '')))
    parsed = parse_path(best_p.get('d'))
    
    pts_raw = []
    for seg in parsed:
        for t in np.linspace(0, 1, 16, endpoint=False):
            pt = seg.point(t)
            pts_raw.append([pt.real, -pt.imag])
    pts_raw = np.array(pts_raw)
    
    h_current = pts_raw[:, 1].max() - pts_raw[:, 1].min()
    pts_raw = pts_raw * (target_height / h_current)
    
    base_poly = Polygon(pts_raw).buffer(0)
    if isinstance(base_poly, MultiPolygon):
        base_poly = max(base_poly.geoms, key=lambda g: g.area)
    if not base_poly.exterior.is_ccw:
        base_poly = Polygon(list(base_poly.exterior.coords)[::-1])
        
    bounds = base_poly.bounds
    cx = (bounds[0] + bounds[2]) / 2.0
    cy = (bounds[1] + bounds[3]) / 2.0
    
    base_ring = resample_polygon(base_poly, n_points)
    base_ring[:, 0] -= cx
    base_ring[:, 1] -= cy
    
    centered_poly = Polygon(base_ring)
    if not centered_poly.exterior.is_ccw:
        centered_poly = Polygon(list(centered_poly.exterior.coords)[::-1])
        base_ring = np.array(centered_poly.exterior.coords)[:-1]
        
    R = fillet_radius
    h_vert_top = total_thickness - R # 15.0 - 1.2 = 13.8 mm
    theta_vals = np.linspace(0, np.pi/2, n_fillet_steps)
    
    rings = []
    z_vals = []
    
    # 1. Boleado inferior: Z = 0 a 1.2 mm
    prev_ring = None
    for theta in theta_vals:
        z = R * (1.0 - np.cos(theta))
        dr = R * (1.0 - np.sin(theta))
        if dr > 0.001:
            inset_poly = centered_poly.buffer(-dr)
            if isinstance(inset_poly, MultiPolygon):
                inset_poly = max(inset_poly.geoms, key=lambda g: g.area)
            if not inset_poly.exterior.is_ccw:
                inset_poly = Polygon(list(inset_poly.exterior.coords)[::-1])
            ring = resample_polygon(inset_poly, n_points)
        else:
            ring = base_ring.copy()
            
        if prev_ring is not None:
            ring = align_points(prev_ring, ring)
        rings.append(ring)
        z_vals.append(z)
        prev_ring = ring
        
    # 2. Pared vertical central extendida: hasta Z = 13.8 mm (12.6 mm de altura recta!)
    top_base_ring = align_points(prev_ring, base_ring.copy())
    rings.append(top_base_ring)
    z_vals.append(h_vert_top)
    prev_ring = top_base_ring
    
    # 3. Boleado superior: Z = 13.8 a 15.0 mm
    for theta in theta_vals[1:]:
        dz = R * np.sin(theta)
        dr = R * (1.0 - np.cos(theta))
        z = h_vert_top + dz
        
        inset_poly = centered_poly.buffer(-dr)
        if isinstance(inset_poly, MultiPolygon):
            inset_poly = max(inset_poly.geoms, key=lambda g: g.area)
        if not inset_poly.exterior.is_ccw:
            inset_poly = Polygon(list(inset_poly.exterior.coords)[::-1])
            
        ring = resample_polygon(inset_poly, n_points)
        ring = align_points(prev_ring, ring)
        rings.append(ring)
        z_vals.append(z)
        prev_ring = ring
        
    vertices = []
    for ring, z in zip(rings, z_vals):
        vertices.append(np.column_stack([ring, np.full(n_points, z)]))
    vertices = np.vstack(vertices)
    
    faces = []
    n_layers = len(rings)
    for l in range(n_layers - 1):
        for i in range(n_points):
            i_next = (i + 1) % n_points
            v0 = l * n_points + i
            v1 = l * n_points + i_next
            v2 = (l + 1) * n_points + i_next
            v3 = (l + 1) * n_points + i
            faces.append([v0, v1, v2])
            faces.append([v0, v2, v3])
            
    # Tapa inferior (Z = 0)
    bottom_pts = rings[0]
    tris_bottom = earcut.triangulate_float64(
        bottom_pts.astype(np.float64),
        np.array([n_points], dtype=np.uint32)
    ).reshape(-1, 3)[:, ::-1]
    faces.extend(tris_bottom.tolist())
    
    # Tapa superior (Z = 15.0)
    top_offset = (n_layers - 1) * n_points
    top_pts = rings[-1]
    tris_top = earcut.triangulate_float64(
        top_pts.astype(np.float64),
        np.array([n_points], dtype=np.uint32)
    ).reshape(-1, 3) + top_offset
    faces.extend(tris_top.tolist())
    
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=True)
    trimesh.repair.fix_normals(mesh)
    
    mesh.export(out_stl_path, file_type='stl')
    
    mbounds = mesh.bounds
    dims = mbounds[1] - mbounds[0]
    file_size_kb = os.path.getsize(out_stl_path) / 1024.0
    
    return {
        "file": os.path.basename(out_stl_path),
        "watertight": mesh.is_watertight,
        "euler": mesh.euler_number,
        "volume_cm3": mesh.volume / 1000.0,
        "width_mm": dims[0],
        "height_mm": dims[1],
        "thickness_mm": dims[2],
        "size_kb": file_size_kb
    }

def main():
    svg_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\01_siluetas_svg"
    out_dir = r"c:\Users\Henry\Documents\antigravity\tinkilab_talleres\pack_digitoys_12\02_modelos_stl_15mm"
    os.makedirs(out_dir, exist_ok=True)
    
    svg_files = sorted(glob.glob(os.path.join(svg_dir, "*.svg")))
    print(f"Generando 12 modelos STL con GROSOR 15 MM y DOBLE BOLEADO...")
    
    results = []
    for svg_f in svg_files:
        base_name = os.path.splitext(os.path.basename(svg_f))[0]
        out_stl = os.path.join(out_dir, f"{base_name}.stl")
        res = generate_3d_stl_15mm(svg_f, out_stl)
        results.append(res)
        print(f"OK: {res['file']:28s} | Dim: {res['width_mm']:5.1f} x {res['height_mm']:5.1f} x {res['thickness_mm']:4.1f} mm | Vol: {res['volume_cm3']:4.1f} cm3 | Watertight: {res['watertight']} | Size: {res['size_kb']:5.1f} KB")

    print("\nResumen 15mm:")
    all_watertight = all(r['watertight'] for r in results)
    print(f"Total STLs 15mm: {len(results)} | Todos Watertight: {all_watertight}")

if __name__ == "__main__":
    main()
