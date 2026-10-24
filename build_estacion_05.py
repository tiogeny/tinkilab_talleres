import json

with open('pack_digitoys_12/05_acabado_color/characters_data.json', 'r', encoding='utf-8') as f:
    characters_json = f.read()

html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Estación 05 — Acabado & Color | DigiToys 2.5D</title>
    <style>
        :root {{
            --bg-main: #f8fafc;
            --bg-card: #ffffff;
            --border: #e2e8f0;
            --text-title: #0f172a;
            --text-body: #334155;
            --text-muted: #64748b;
            --primary: #0284c7;
            --primary-light: #e0f2fe;
            --accent: #10b981;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-body);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}

        header {{
            background-color: var(--bg-card);
            border-bottom: 1px solid var(--border);
            padding: 12px 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-shrink: 0;
        }}

        .header-title h1 {{
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-title);
            letter-spacing: -0.02em;
        }}

        .header-title p {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 2px;
        }}

        .header-badges {{
            display: flex;
            gap: 10px;
        }}

        .badge {{
            font-size: 0.72rem;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 999px;
            background: #f1f5f9;
            color: var(--text-muted);
            border: 1px solid var(--border);
        }}

        .badge.highlight {{
            background: var(--primary-light);
            color: var(--primary);
            border-color: #bae6fd;
        }}

        .main-layout {{
            flex: 1;
            display: grid;
            grid-template-columns: 260px 1fr;
            overflow: hidden;
        }}

        /* Columna 1: Lista de Siluetas */
        .sidebar-list {{
            background-color: var(--bg-card);
            border-right: 1px solid var(--border);
            overflow-y: auto;
            padding: 14px;
        }}

        .sidebar-title {{
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 12px;
            padding-left: 4px;
        }}

        .char-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 9px 12px;
            border-radius: 8px;
            cursor: pointer;
            border: 1px solid transparent;
            margin-bottom: 5px;
            transition: all 0.15s ease;
        }}

        .char-item:hover {{
            background-color: #f1f5f9;
            border-color: var(--border);
        }}

        .char-item.active {{
            background-color: var(--primary-light);
            border-color: #7dd3fc;
        }}

        .char-item svg {{
            width: 32px;
            height: 32px;
            flex-shrink: 0;
        }}

        .char-item.active svg path {{
            fill: var(--primary);
        }}

        .char-item-name {{
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text-title);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .char-item.active .char-item-name {{
            color: var(--primary);
            font-weight: 700;
        }}

        /* Columna 2: Canvas Principal (Silueta Superior + 3 Renders Horizontales Debajo) */
        .main-content {{
            padding: 20px 28px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 18px;
        }}

        /* Tarjeta Superior: Silueta + Ficha Rápida */
        .top-hero-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px 24px;
            display: flex;
            align-items: center;
            gap: 28px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            flex-shrink: 0;
        }}

        .silhouette-box {{
            width: 150px;
            height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f8fafc;
            border-radius: 12px;
            border: 2px dashed #cbd5e1;
            padding: 10px;
            flex-shrink: 0;
        }}

        .silhouette-box svg {{
            width: 100%;
            height: 100%;
            max-width: 130px;
            max-height: 130px;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.08));
        }}

        .hero-details {{
            flex: 1;
        }}

        .hero-title-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 6px;
        }}

        .hero-title {{
            font-size: 1.2rem;
            font-weight: 800;
            color: var(--text-title);
            letter-spacing: -0.01em;
        }}

        .hero-scale-badge {{
            font-size: 0.72rem;
            color: var(--primary);
            font-weight: 700;
            background: var(--primary-light);
            padding: 4px 10px;
            border-radius: 6px;
            border: 1px solid #bae6fd;
        }}

        .hero-description {{
            font-size: 0.82rem;
            color: var(--text-body);
            line-height: 1.45;
            margin-bottom: 12px;
        }}

        .hero-tags {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .hero-tag {{
            font-size: 0.72rem;
            background: #f1f5f9;
            color: var(--text-muted);
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: 500;
        }}

        /* Sección Inferior: 3 Renders en Fila Horizontal */
        .bottom-section {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            flex: 1;
        }}

        .section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .section-title {{
            font-size: 0.92rem;
            font-weight: 700;
            color: var(--text-title);
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .cards-row-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 18px;
        }}

        .render-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            transition: all 0.2s ease;
        }}

        .render-card:hover {{
            border-color: #cbd5e1;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            transform: translateY(-2px);
        }}

        .card-header-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 6px;
        }}

        .card-badge {{
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
            padding: 2px 8px;
            border-radius: 4px;
            display: inline-block;
        }}

        .badge-pop {{ background: #dcfce7; color: #15803d; }}
        .badge-kawaii {{ background: #ede9fe; color: #6d28d9; }}
        .badge-monster {{ background: #e0f2fe; color: #0369a1; }}

        .card-name {{
            font-size: 0.92rem;
            font-weight: 700;
            color: var(--text-title);
            margin-bottom: 4px;
        }}

        .card-desc {{
            font-size: 0.74rem;
            color: var(--text-muted);
            line-height: 1.35;
            margin-bottom: 12px;
            min-height: 34px;
        }}

        /* Contenedor de la Imagen: RENDER COMPLETO SIN RECORTES */
        .render-img-box {{
            width: 100%;
            height: 220px;
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12px;
            overflow: hidden;
            padding: 6px;
        }}

        .render-img-box img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            display: block;
            border-radius: 6px;
        }}

        .palette-row {{
            display: flex;
            gap: 6px;
            margin-bottom: 10px;
        }}

        .palette-chip {{
            flex: 1;
            height: 22px;
            border-radius: 4px;
            border: 1px solid rgba(0,0,0,0.12);
        }}

        .tips-list {{
            font-size: 0.72rem;
            color: #475569;
            padding-left: 16px;
            line-height: 1.4;
        }}

        .tips-list li {{
            margin-bottom: 3px;
        }}
    </style>
</head>
<body>
    <header>
        <div class="header-title">
            <h1>ESTACIÓN 05 — ACABADO & COLOR</h1>
            <p>Guía de Inspiración y Pintura de DigiToys 2.5D con Marcadores Posca</p>
        </div>
        <div class="header-badges">
            <span class="badge">Altura: 70 mm</span>
            <span class="badge">Espesor: 15 mm (Boleado)</span>
            <span class="badge highlight">Marcadores Acrílicos Posca</span>
        </div>
    </header>

    <div class="main-layout">
        <!-- Columna 1: Lista de Siluetas -->
        <aside class="sidebar-list">
            <div class="sidebar-title">12 Siluetas Oficiales</div>
            <div id="character-list"></div>
        </aside>

        <!-- Columna 2: Canvas Principal (Silueta Superior + 3 Renders Horizontales Debajo) -->
        <main class="main-content">
            <!-- Tarjeta Superior: Silueta + Ficha Rápida -->
            <div class="top-hero-card">
                <div class="silhouette-box" id="silhouette-display">
                    <!-- Inyectado por JS sin CORS -->
                </div>
                <div class="hero-details">
                    <div class="hero-title-row">
                        <div class="hero-title" id="current-name">01 Dino Bebé 1</div>
                        <div class="hero-scale-badge">Escala Real 1:1 (70 mm)</div>
                    </div>
                    <p class="hero-description" id="hero-desc">
                        Silueta base 2.5D para impresión 3D con bordes redondeados infantiles ($R=1.2\text{{ mm}}$). Planifica el diseño de la carita en tu <strong>Ficha de Trabajo Dual</strong> con lápices antes de pintar sobre la pieza física con marcadores Posca.
                    </p>
                    <div class="hero-tags" id="hero-tags">
                        <span class="hero-tag">📏 70 × 15 mm</span>
                        <span class="hero-tag">🎨 Base recomendada: Blanco / Filamento Neutro</span>
                        <span class="hero-tag">✨ Doble Boleado Suave</span>
                    </div>
                </div>
            </div>

            <!-- Sección Inferior: 3 Renders en Fila Horizontal -->
            <div class="bottom-section">
                <div class="section-header">
                    <div class="section-title">
                        <span>🎨</span> Propuestas de Acabado 2.5D (Renders de Muestra)
                    </div>
                </div>

                <div class="cards-row-grid" id="renders-container">
                    <!-- Inyectado dinámicamente por JS -->
                </div>
            </div>
        </main>
    </div>

    <script>
        const characters = {characters_json};
        let currentIdx = 0;

        const dinoBebeCardsHTML = `
            <!-- Tarjeta 1: Pop Color -->
            <div class="render-card">
                <div class="card-header-row">
                    <span class="card-badge badge-pop">ESTILO 01</span>
                    <span style="font-size: 0.68rem; color: #15803d; font-weight: 600;">1 Ojo Cartoon</span>
                </div>
                <div class="card-name">Color Pop / Menta & Amarillo</div>
                <div class="card-desc">Cuerpo menta, barriga amarilla plana, ojo grande lateral con doble brillo blanco y mejilla rosa.</div>
                <div class="render-img-box">
                    <img src="inspiracion/01_dino_bebe_25d_pop.jpg" alt="Dino Bebe 2.5D Pop Color">
                </div>
                <div class="palette-row">
                    <div class="palette-chip" style="background: #10b981;" title="Verde Menta (Base)"></div>
                    <div class="palette-chip" style="background: #fbbf24;" title="Amarillo Brillante"></div>
                    <div class="palette-chip" style="background: #f43f5e;" title="Rosa Mejillas"></div>
                    <div class="palette-chip" style="background: #0f172a;" title="Negro Trazo"></div>
                </div>
                <ul class="tips-list">
                    <li>Barriga pintada con doble pasada de amarillo Posca.</li>
                    <li>Ojo grande cartoon con dos puntos de luz blancos.</li>
                </ul>
            </div>

            <!-- Tarjeta 2: Kawaii Pastel -->
            <div class="render-card">
                <div class="card-header-row">
                    <span class="card-badge badge-kawaii">ESTILO 02</span>
                    <span style="font-size: 0.68rem; color: #6d28d9; font-weight: 600;">Ojo Manga / Estrella</span>
                </div>
                <div class="card-name">Pastel Kawaii / Lila & Melocotón</div>
                <div class="card-desc">Cuerpo lila suave, barriga melocotón cálido, ojo manga con destello de estrella y rubor dulce.</div>
                <div class="render-img-box">
                    <img src="inspiracion/01_dino_bebe_25d_kawaii.jpg" alt="Dino Bebe 2.5D Kawaii Pastel">
                </div>
                <div class="palette-row">
                    <div class="palette-chip" style="background: #c4b5fd;" title="Lila Pastel (Base)"></div>
                    <div class="palette-chip" style="background: #fdba74;" title="Melocotón Suave"></div>
                    <div class="palette-chip" style="background: #f472b6;" title="Rosa Pastel"></div>
                    <div class="palette-chip" style="background: #ffffff;" title="Blanco Destellos"></div>
                </div>
                <ul class="tips-list">
                    <li>Colores pastel relajantes ideales para los más pequeños.</li>
                    <li>Destellos de estrella en el ojo con plumón blanco fino.</li>
                </ul>
            </div>

            <!-- Tarjeta 3: Monster Texturado -->
            <div class="render-card">
                <div class="card-header-row">
                    <span class="card-badge badge-monster">ESTILO 03</span>
                    <span style="font-size: 0.68rem; color: #0369a1; font-weight: 600;">Monstruito / Colmillo</span>
                </div>
                <div class="card-name">Monstruo Travieso / Turquesa & Naranja</div>
                <div class="card-desc">Cuerpo turquesa, manchas circulares naranjas en el lomo y sonrisa traviesa con colmillito blanco.</div>
                <div class="render-img-box">
                    <img src="inspiracion/01_dino_bebe_25d_monster.jpg" alt="Dino Bebe 2.5D Monster">
                </div>
                <div class="palette-row">
                    <div class="palette-chip" style="background: #06b6d4;" title="Turquesa Eléctrico"></div>
                    <div class="palette-chip" style="background: #f97316;" title="Naranja Intenso"></div>
                    <div class="palette-chip" style="background: #0f172a;" title="Boca / Contorno"></div>
                    <div class="palette-chip" style="background: #ffffff;" title="Dientes Blancos"></div>
                </div>
                <ul class="tips-list">
                    <li>Manchas circulares de diferente diámetro en el lomo.</li>
                    <li>Dientecito triangular blanco en la esquina de la boca.</li>
                </ul>
            </div>
        `;

        function initApp() {{
            const listEl = document.getElementById("character-list");
            listEl.innerHTML = "";

            characters.forEach((char, idx) => {{
                const item = document.createElement("div");
                item.className = "char-item" + (idx === 0 ? " active" : "");
                item.onclick = () => selectCharacter(idx);
                item.innerHTML = `
                    <svg viewBox="${{char.viewBox}}">
                        <path d="${{char.d}}" fill="#64748b" />
                    </svg>
                    <div class="char-item-name">${{char.name}}</div>
                `;
                listEl.appendChild(item);
            }});

            renderSilhouette();
            renderRenders(0);
        }}

        function selectCharacter(idx) {{
            currentIdx = idx;
            document.querySelectorAll(".char-item").forEach((el, i) => {{
                el.classList.toggle("active", i === idx);
            }});
            const char = characters[idx];
            document.getElementById("current-name").textContent = char.name;
            
            renderSilhouette();
            renderRenders(idx);
        }}

        function renderRenders(idx) {{
            const container = document.getElementById("renders-container");
            if (idx === 0) {{
                container.innerHTML = dinoBebeCardsHTML;
            }} else {{
                const char = characters[idx];
                container.innerHTML = `
                    <div class="render-card">
                        <div class="card-header-row">
                            <span class="card-badge badge-pop">PROPUESTA 01</span>
                            <span style="font-size: 0.68rem; color: #15803d; font-weight: 600;">1 Ojo Cíclope</span>
                        </div>
                        <div class="card-name">Estilo Alien / Cíclope Pop</div>
                        <div class="card-desc">Un único ojo gigante central con iris brillante y pupila negra con doble reflejo.</div>
                        <div class="render-img-box" style="flex-direction: column; background: #f8fafc; border: 2px dashed #cbd5e1; gap: 8px;">
                            <div style="font-size: 2rem;">👁️</div>
                            <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600;">Próximamente Render 2.5D</div>
                        </div>
                        <div class="palette-row">
                            <div class="palette-chip" style="background: #0284c7;" title="Azul Eléctrico"></div>
                            <div class="palette-chip" style="background: #fbbf24;" title="Amarillo"></div>
                            <div class="palette-chip" style="background: #0f172a;" title="Negro Trazo"></div>
                            <div class="palette-chip" style="background: #ffffff;" title="Blanco Brillos"></div>
                        </div>
                        <ul class="tips-list">
                            <li>Dibuja un círculo grande con plumón negro en el centro.</li>
                            <li>Añade el iris de color y los puntos blancos de brillo.</li>
                        </ul>
                    </div>

                    <div class="render-card">
                        <div class="card-header-row">
                            <span class="card-badge badge-kawaii">PROPUESTA 02</span>
                            <span style="font-size: 0.68rem; color: #6d28d9; font-weight: 600;">2 Ojos Tiernos</span>
                        </div>
                        <div class="card-name">Estilo Amigable / 2 Ojos & Sonrisa</div>
                        <div class="card-desc">Dos ojitos juntos y separados con expresión tierna, pecas y barriga de color.</div>
                        <div class="render-img-box" style="flex-direction: column; background: #f8fafc; border: 2px dashed #cbd5e1; gap: 8px;">
                            <div style="font-size: 2rem;">👀</div>
                            <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600;">Próximamente Render 2.5D</div>
                        </div>
                        <div class="palette-row">
                            <div class="palette-chip" style="background: #a855f7;" title="Púrpura"></div>
                            <div class="palette-chip" style="background: #fda4af;" title="Rosa Pastel"></div>
                            <div class="palette-chip" style="background: #fef08a;" title="Amarillo Pastel"></div>
                            <div class="palette-chip" style="background: #ffffff;" title="Blanco"></div>
                        </div>
                        <ul class="tips-list">
                            <li>Dos círculos paralelos con puntos de luz y mejillas sonrosadas.</li>
                            <li>Boca con sonrisa suave en arco.</li>
                        </ul>
                    </div>

                    <div class="render-card">
                        <div class="card-header-row">
                            <span class="card-badge badge-monster">PROPUESTA 03</span>
                            <span style="font-size: 0.68rem; color: #0369a1; font-weight: 600;">Texturas / Monstruo</span>
                        </div>
                        <div class="card-name">Estilo Gráfico / Rayas o Manchas</div>
                        <div class="card-desc">Rayas atigradas gruesas o manchas geométricas combinadas con boca traviesa.</div>
                        <div class="render-img-box" style="flex-direction: column; background: #f8fafc; border: 2px dashed #cbd5e1; gap: 8px;">
                            <div style="font-size: 2rem;">⚡</div>
                            <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600;">Próximamente Render 2.5D</div>
                        </div>
                        <div class="palette-row">
                            <div class="palette-chip" style="background: #f97316;" title="Naranja"></div>
                            <div class="palette-chip" style="background: #10b981;" title="Verde"></div>
                            <div class="palette-chip" style="background: #0f172a;" title="Negro"></div>
                            <div class="palette-chip" style="background: #ffffff;" title="Dientes"></div>
                        </div>
                        <ul class="tips-list">
                            <li>Patrones geométricos con trazos gruesos y directos de Posca.</li>
                            <li>Boca con colmillitos afilados para darle personalidad.</li>
                        </ul>
                    </div>
                `;
            }}
        }}

        function renderSilhouette() {{
            if (!characters.length) return;
            const char = characters[currentIdx];
            const box = document.getElementById("silhouette-display");
            box.innerHTML = `
                <svg viewBox="${{char.viewBox}}">
                    <path d="${{char.d}}" fill="#1e293b" />
                </svg>
            `;
        }}

        window.onload = initApp;
    </script>
</body>
</html>
'''

with open('pack_digitoys_12/05_acabado_color/estacion_05_acabado_color.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("estacion_05_acabado_color.html rebuilt with 3 bottom renders layout successfully!")
