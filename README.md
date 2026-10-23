# Tinkilab Talleres - Pack DigiToys 12 🧸🚀

Colección de 12 personajes oficiales (siluetas vectoriales SVG y modelos 3D STL) para talleres de fabricación digital, escaneo, vectorizado, impresión 3D y personalización de color.

---

## 📁 Estructura del Proyecto

```text
tinkilab_talleres/
├── pack_digitoys_12/
│   ├── 01_siluetas_svg/          # 12 Siluetas vectoriales limpias (curvas Bézier pulidas en Inkscape)
│   ├── 02_modelos_stl_10mm/      # 12 Modelos 3D STL (70 mm altura, 10 mm grosor, doble boleado)
│   ├── preview_3d_pack12.png     # Vista previa de los 12 modelos 3D
│   └── visor_3d_pack12.html      # Visor interactivo WebGL (Three.js)
├── generate_stls_10mm.py         # Script generador automatizado de STLs a partir de SVGs
└── README.md
```

---

## 📐 Especificaciones de los Modelos 3D STL

- **Altura física ($Y$):** $70.0\text{ mm}$ ($7\text{ cm}$).
- **Espesor total ($Z$):** $10.0\text{ mm}$ ($1\text{ cm}$).
- **Doble boleado simétrico:**
  - **Inferior ($Z = 0.0$ a $1.2\text{ mm}$):** Filete curvo con radio $R = 1.2\text{ mm}$ para un despegue y tacto suave.
  - **Cuerpo central ($Z = 1.2$ a $8.8\text{ mm}$):** Pared vertical de $7.6\text{ mm}$.
  - **Superior ($Z = 8.8$ a $10.0\text{ mm}$):** Filete curvo con radio $R = 1.2\text{ mm}$ que cierra en la cara superior plana.
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
