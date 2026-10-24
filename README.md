# Tinkilab Talleres - Pack DigiToys 12 🧸🚀

Colección de 12 personajes oficiales (siluetas vectoriales SVG y modelos 3D STL) para talleres de fabricación digital, escaneo, vectorizado, impresión 3D y personalización de color.

---

## 📁 Estructura del Proyecto

```text
tinkilab_talleres/
├── pack_digitoys_12/
│   ├── 01_siluetas_svg/               # 12 Siluetas vectoriales limpias (curvas Bézier pulidas en Inkscape)
│   ├── 02_modelos_stl_10mm/           # 12 Modelos 3D STL estándar (70x10 mm, doble boleado simétrico)
│   ├── 02_modelos_stl_15mm/           # 12 Modelos 3D STL gruesos de alta estabilidad (70x15 mm, doble boleado)
│   ├── 03_plantillas_impresion_pdf/   # Plantillas en PDF bandera blanca:
│   │   ├── fichas_trabajo_A5_imprimir.pdf  # Fichas ágiles (2 por A4, solo negro para escanear)
│   │   ├── fichas_trabajo_A4_dual.pdf      # Fichas completas A4 (Izquierda: Negro / Derecha: Color)
│   │   └── 03_plantilla_diseno_libre_A4.pdf
│   ├── 04_packaging_box/              # Cajas láser (80x80x17 mm) en PDF y SVG (Rojo corte / Azul marcado)
│   │   ├── caja_laser_80x80x17.pdf / .svg                 # Versión Universal con ventana
│   │   └── caja_laser_80x80x17_01_Dino_Bebe_1.pdf / .svg # Ventana con silueta troquelada alineada
│   ├── 05_acabado_color/              # Estación 05: Guía web con biblioteca de rasgos y fotos 2.5D
│   ├── 01_lamina_siluetas_12.png      # Lámina general de siluetas 2D
│   ├── preview_3d_pack12.png          # Vista previa 3D con doble curvatura
│   └── visor_3d_pack12.html           # Visor interactivo WebGL (Three.js)
├── generate_fichas_a5_2porA4.py       # Generador de fichas A5 y duales A4
├── generate_laser_packaging_box_17mm.py # Generador de cajas para corte láser
├── generate_stls_10mm.py              # Generador de modelos 3D STL (10 mm)
├── generate_stls_15mm.py              # Generador de modelos 3D STL (15 mm alta estabilidad)
└── README.md
```

---

## 📐 Especificaciones de los Modelos 3D STL

- **Altura física ($Y$):** $70.0\text{ mm}$ ($7\text{ cm}$).
- **Espesor disponible:**
  - **Colección 10 mm (`02_modelos_stl_10mm`):** Espesor $10.0\text{ mm}$ (ligero, ~25-35g PLA).
  - **Colección 15 mm (`02_modelos_stl_15mm`):** Espesor $15.0\text{ mm}$ (alta estabilidad en mesa, huella plana de $12.6\text{ mm}$).
- **Doble boleado simétrico:**
  - **Inferior ($Z = 0.0$ a $1.2\text{ mm}$):** Filete curvo con radio $R = 1.2\text{ mm}$ para un despegue y tacto suave.
  - **Cuerpo central:** Pared vertical recta.
  - **Superior:** Filete curvo con radio $R = 1.2\text{ mm}$ que cierra en la cara superior plana.
- **Topología de malla:** $100\%$ Manifold / Watertight (Euler characteristic = 2), sin huecos ni caras invertidas.
- **Orientación de impresión:** Acostados sobre la cama de impresión (eje $Z$).

---

## 👾 Catálogo de los 12 Personajes

| # | Personaje | Dimensiones ($X \times Y \times Z$) | Volumen aproximado |
|---|---|:---:|:---:|
| **01** | Dino Bebé 1 | $75.5 \times 70.0 \times 10.0\text{ mm}$ | $28.3\text{ cm}^3$ |
| **02** | Dino Bebé 2 | $69.5 \times 70.0 \times 10.0\text{ mm}$ | $27.1\text{ cm}^3$ |
| **03** | Fantasmita | $75.9 \times 70.0 \times 10.0\text{ mm}$ | $37.2\text{ cm}^3$ |
| **04** | Frijolito | $70.7 \times 70.0 \times 10.0\text{ mm}$ | $37.4\text{ cm}^3$ |
| **05** | Monstruo Cuernitos | $56.6 \times 70.0 \times 10.0\text{ mm}$ | $26.2\text{ cm}^3$ |
| **06** | Mostrito Orejón | $62.6 \times 70.0 \times 10.0\text{ mm}$ | $29.6\text{ cm}^3$ |
| **07** | Monstruo Espinoso | $65.3 \times 69.9 \times 10.0\text{ mm}$ | $31.8\text{ cm}^3$ |
| **08** | Mostrito Periscopio | $60.0 \times 70.0 \times 10.0\text{ mm}$ | $25.7\text{ cm}^3$ |
| **09** | Marciano Zog | $44.2 \times 70.0 \times 10.0\text{ mm}$ | $19.8\text{ cm}^3$ |
| **10** | Monstruo Crestas | $73.6 \times 70.0 \times 10.0\text{ mm}$ | $32.6\text{ cm}^3$ |
| **11** | Robot Bip Bop | $55.0 \times 70.0 \times 10.0\text{ mm}$ | $20.9\text{ cm}^3$ |
| **12** | Gato Miau | $68.6 \times 70.0 \times 10.0\text{ mm}$ | $29.8\text{ cm}^3$ |

---

## 🖨️ Recomendaciones de Impresión 3D (FDM)

- **Material recomendado:** PLA o PLA Matte.
- **Altura de capa:** $0.16\text{ mm}$ o $0.20\text{ mm}$ (con soporte adaptativo de capa variable si se desea ultra-definición en el boleado superior).
- **Relleno (Infill):** $10\%$ a $15\%$ (Giroide o Cuadrícula).
- **Paredes:** 2 a 3 perímetros.
- **Soportes:** No requeridos.
- **Tiempo estimado por pieza:** 30 a 45 minutos (según velocidad de la impresora).

---

Desarrollado para los talleres educativos de **Tinkilab**.
