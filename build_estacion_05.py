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
            grid-template-columns: 270px 1fr 410px;
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

        /* Columna 2: Canvas Central y Guía de Expresiones */
        .center-canvas {{
            padding: 20px 24px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 18px;
        }}

        .silhouette-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px 24px;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }}

        .silhouette-header {{
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
        }}

        .silhouette-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-title);
        }}

        .silhouette-scale {{
            font-size: 0.72rem;
            color: var(--primary);
            font-weight: 600;
            background: var(--primary-light);
            padding: 3px 8px;
            border-radius: 6px;
        }}

        .silhouette-box {{
            width: 210px;
            height: 210px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f8fafc;
            border-radius: 12px;
            border: 2px dashed #cbd5e1;
            padding: 14px;
        }}

        .silhouette-box svg {{
            width: 100%;
            height: 100%;
            max-width: 180px;
            max-height: 180px;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.08));
        }}

        /* Biblioteca de Expresiones Faciales */
        .features-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 14px;
            width: 100%;
        }}

        .feature-block {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px 16px;
        }}

        .feature-block-title {{
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--text-title);
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .feature-items-row {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
        }}

        .feature-box {{
            background: #f8fafc;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 8px 4px;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 62px;
            transition: transform 0.1s ease;
        }}

        .feature-box:hover {{
            background: #ffffff;
            border-color: #cbd5e1;
            transform: translateY(-2px);
        }}

        .feature-box svg {{
            width: 32px;
            height: 32px;
        }}

        .feature-box-label {{
            font-size: 0.65rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-top: 5px;
        }}

        /* Columna 3: 3 Opciones de Inspiración 2.5D */
        .sidebar-inspiration {{
            background-color: var(--bg-card);
            border-left: 1px solid var(--border);
            overflow-y: auto;
            padding: 18px 20px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .inspiration-title {{
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--text-title);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .card-style {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px;
            transition: border-color 0.15s ease;
        }}

        .card-style:hover {{
            border-color: #cbd5e1;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        }}

        .card-badge {{
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
            padding: 2px 8px;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 6px;
        }}

        .badge-pop {{ background: #dcfce7; color: #15803d; }}
        .badge-kawaii {{ background: #ede9fe; color: #6d28d9; }}
        .badge-monster {{ background: #e0f2fe; color: #0369a1; }}

        .card-name {{
            font-size: 0.88rem;
            font-weight: 700;
            color: var(--text-title);
            margin-bottom: 3px;
        }}

        .card-desc {{
            font-size: 0.72rem;
            color: var(--text-muted);
            line-height: 1.35;
            margin-bottom: 10px;
        }}

        .card-preview-img {{
            width: 100%;
            height: 165px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 10px;
            border: 1px solid var(--border);
            background: #f8fafc;
            display: block;
        }}

        .palette-row {{
            display: flex;
            gap: 6px;
            margin-bottom: 8px;
        }}

        .palette-chip {{
            flex: 1;
            height: 20px;
            border-radius: 4px;
            border: 1px solid rgba(0,0,0,0.1);
        }}

        .tips-list {{
            font-size: 0.68rem;
            color: #475569;
            padding-left: 14px;
        }}

        .tips-list li {{
            margin-bottom: 2px;
        }}
    </style>
</head>
<body>
    <header>
        <div class="header-title">
            <h1>ESTACIÓN 05 — ACABADO & COLOR</h1>
            <p>Catálogo de Expresiones Faciales y Guía de Pintura de DigiToys 2.5D</p>
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

        <!-- Columna 2: Canvas Central y Guía de Expresiones -->
        <main class="center-canvas">
            <!-- Tarjeta de Silueta Oficial -->
            <div class="silhouette-card">
                <div class="silhouette-header">
                    <div class="silhouette-title" id="current-name">01 Dino Bebé 1</div>
                    <div class="silhouette-scale">Escala 1:1 (70 mm)</div>
                </div>

                <div class="silhouette-box" id="silhouette-display">
                    <!-- Inyectado por JS sin CORS -->
                </div>
            </div>

            <!-- Biblioteca de Expresiones Faciales Fáciles para 7 cm -->
            <div class="features-grid">
                <!-- Ojos -->
                <div class="feature-block">
                    <div class="feature-block-title">
                        <span>👀</span> Ideas de Ojos (Simples & Lindos)
                    </div>
                    <div class="feature-items-row">
                        <div class="feature-box" title="Círculo negro grande con 2 puntos de luz blancos">
                            <svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="14" fill="#0f172a"/><circle cx="16" cy="15" r="4.5" fill="#ffffff"/><circle cx="24" cy="23" r="2.5" fill="#ffffff"/></svg>
                            <span class="feature-box-label">Cartoon</span>
                        </div>
                        <div class="feature-box" title="1 solo ojo central gigante para monstruos o marcianos">
                            <svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="16" fill="#f8fafc" stroke="#0f172a" stroke-width="2.5"/><circle cx="20" cy="20" r="8" fill="#0284c7"/><circle cx="20" cy="20" r="4" fill="#0f172a"/><circle cx="18" cy="18" r="2" fill="#ffffff"/></svg>
                            <span class="feature-box-label">1 Cíclope</span>
                        </div>
                        <div class="feature-box" title="Arco curvado feliz con pestañita">
                            <svg viewBox="0 0 40 40"><path d="M8,24 Q20,10 32,24" stroke="#0f172a" stroke-width="4" fill="none" stroke-linecap="round"/><line x1="12" y1="16" x2="8" y2="12" stroke="#0f172a" stroke-width="3" stroke-linecap="round"/><line x1="28" y1="16" x2="32" y2="12" stroke="#0f172a" stroke-width="3" stroke-linecap="round"/></svg>
                            <span class="feature-box-label">Guiño</span>
                        </div>
                        <div class="feature-box" title="Puntos limpios súper tiernos">
                            <svg viewBox="0 0 40 40"><circle cx="13" cy="20" r="5" fill="#0f172a"/><circle cx="27" cy="20" r="5" fill="#0f172a"/></svg>
                            <span class="feature-box-label">2 Puntos</span>
                        </div>
                    </div>
                </div>

                <!-- Bocas -->
                <div class="feature-block">
                    <div class="feature-block-title">
                        <span>👄</span> Ideas de Bocas (Trazo Fácil Posca)
                    </div>
                    <div class="feature-items-row">
                        <div class="feature-box" title="Sonrisa amplia feliz">
                            <svg viewBox="0 0 40 40"><path d="M8,18 Q20,32 32,18" stroke="#0f172a" stroke-width="3.5" fill="none" stroke-linecap="round"/></svg>
                            <span class="feature-box-label">Sonrisa</span>
                        </div>
                        <div class="feature-box" title="Sonrisa pícara con colmillo blanco">
                            <svg viewBox="0 0 40 40"><path d="M8,18 Q20,30 32,18" stroke="#0f172a" stroke-width="3.5" fill="none" stroke-linecap="round"/><polygon points="23,20 28,20 25.5,27" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/></svg>
                            <span class="feature-box-label">Colmillito</span>
                        </div>
                        <div class="feature-box" title="Boca sorpresa abierta 'O'">
                            <svg viewBox="0 0 40 40"><ellipse cx="20" cy="21" rx="8" ry="11" fill="#e11d48" stroke="#0f172a" stroke-width="2.5"/><ellipse cx="20" cy="26" rx="5" ry="4" fill="#fda4af"/></svg>
                            <span class="feature-box-label">Sorpresa</span>
                        </div>
                        <div class="feature-box" title="Boca monstruo zig-zag o robot">
                            <svg viewBox="0 0 40 40"><path d="M8,20 L14,25 L20,16 L26,25 L32,18" stroke="#0f172a" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
                            <span class="feature-box-label">Zig-Zag</span>
                        </div>
                    </div>
                </div>

                <!-- Texturas & Patrones -->
                <div class="feature-block" style="grid-column: span 2;">
                    <div class="feature-block-title">
                        <span>🎨</span> Detalles y Contraste de Color
                    </div>
                    <div class="feature-items-row" style="grid-template-columns: repeat(4, 1fr);">
                        <div class="feature-box" title="Pecas o manchas circulares de color">
                            <svg viewBox="0 0 40 40"><circle cx="12" cy="14" r="3.5" fill="#f97316"/><circle cx="28" cy="13" r="4.5" fill="#f97316"/><circle cx="17" cy="27" r="3" fill="#f97316"/><circle cx="29" cy="26" r="3.5" fill="#f97316"/></svg>
                            <span class="feature-box-label">Pecas / Manchas</span>
                        </div>
                        <div class="feature-box" title="Rayas atigradas gruesas y fáciles">
                            <svg viewBox="0 0 40 40"><path d="M10,13 Q20,9 30,13" stroke="#0284c7" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M8,20 Q20,16 32,20" stroke="#0284c7" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M11,27 Q20,23 29,27" stroke="#0284c7" stroke-width="3" fill="none" stroke-linecap="round"/></svg>
                            <span class="feature-box-label">Rayas Tigre</span>
                        </div>
                        <div class="feature-box" title="Zona del pecho en contraste claro">
                            <svg viewBox="0 0 40 40"><ellipse cx="20" cy="20" rx="15" ry="12" fill="#fef08a" stroke="#ca8a04" stroke-width="2"/></svg>
                            <span class="feature-box-label">Barriga Color</span>
                        </div>
                        <div class="feature-box" title="Mejillas sonrosadas Kawaii">
                            <svg viewBox="0 0 40 40"><ellipse cx="11" cy="20" rx="7" ry="5" fill="#fda4af" opacity="0.85"/><ellipse cx="29" cy="20" rx="7" ry="5" fill="#fda4af" opacity="0.85"/></svg>
                            <span class="feature-box-label">Mejillas Rubor</span>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <!-- Columna 3: 3 Opciones de Inspiración 2.5D -->
        <aside class="sidebar-inspiration">
            <div class="inspiration-title" id="inspiration-header">Inspiración 2.5D: 01 Dino Bebé 1</div>
            <div id="inspiration-cards-container">
                <!-- Se inyecta dinámicamente mediante renderInspirationCards(idx) sin destruir estado -->
            </div>
        </aside>
    </div>

    <script>
        const characters = {characters_json};
        let currentIdx = 0;

        const dinoBebeCardsHTML = `
            <!-- Tarjeta 1: Pop Color -->
            <div class="card-style">
                <span class="card-badge badge-pop">ESTILO 01</span>
                <div class="card-name">Color Pop / Menta & Amarillo</div>
                <div class="card-desc">Base verde menta, barriga amarilla plana, ojos cartoon expresivos y mejillas rosas.</div>
                <img src="inspiracion/01_dino_bebe_25d_pop.jpg" alt="Estilo Pop 2.5D" class="card-preview-img">
                <div class="palette-row">
                    <div class="palette-chip" style="background: #10b981;" title="Verde Menta (Base)"></div>
                    <div class="palette-chip" style="background: #fbbf24;" title="Amarillo Brillante"></div>
                    <div class="palette-chip" style="background: #f43f5e;" title="Rosa Mejillas"></div>
                    <div class="palette-chip" style="background: #0f172a;" title="Negro Trazo"></div>
                </div>
                <ul class="tips-list">
                    <li>Barriga pintada con doble pasada de amarillo Posca.</li>
                    <li>Ojo grande con doble punto de luz blanco.</li>
                </ul>
            </div>

            <!-- Tarjeta 2: Kawaii Pastel -->
            <div class="card-style" style="margin-top: 14px;">
                <span class="card-badge badge-kawaii">ESTILO 02</span>
                <div class="card-name">Pastel Kawaii / Lila & Melocotón</div>
                <div class="card-desc">Base lila suave, barriga melocotón cálido, ojito manga con estrellas y mejillas sonrosadas.</div>
                <img src="inspiracion/01_dino_bebe_25d_kawaii.jpg" alt="Estilo Kawaii 2.5D" class="card-preview-img">
                <div class="palette-row">
                    <div class="palette-chip" style="background: #c4b5fd;" title="Lila Pastel (Base)"></div>
                    <div class="palette-chip" style="background: #fdba74;" title="Melocotón Suave"></div>
                    <div class="palette-chip" style="background: #f472b6;" title="Rosa Pastel"></div>
                    <div class="palette-chip" style="background: #ffffff;" title="Blanco Destellos"></div>
                </div>
                <ul class="tips-list">
                    <li>Tonos suaves ideales para niños pequeños.</li>
                    <li>Brillos de estrellas en los ojos con plumón blanco fino.</li>
                </ul>
            </div>

            <!-- Tarjeta 3: Monster Dino -->
            <div class="card-style" style="margin-top: 14px;">
                <span class="card-badge badge-monster">ESTILO 03</span>
                <div class="card-name">Monstruo Travieso / Turquesa & Naranja</div>
                <div class="card-desc">Base turquesa eléctrica, manchas geométricas naranjas y sonrisa pícara con colmillito.</div>
                <img src="inspiracion/01_dino_bebe_25d_monster.jpg" alt="Estilo Monster 2.5D" class="card-preview-img">
                <div class="palette-row">
                    <div class="palette-chip" style="background: #06b6d4;" title="Turquesa Eléctrico"></div>
                    <div class="palette-chip" style="background: #f97316;" title="Naranja Intenso"></div>
                    <div class="palette-chip" style="background: #0f172a;" title="Boca / Contorno"></div>
                    <div class="palette-chip" style="background: #ffffff;" title="Dientes Blancos"></div>
                </div>
                <ul class="tips-list">
                    <li>Manchas circulares de diferente diámetro sobre el lomo.</li>
                    <li>Dientecito blanco triangular en la esquina de la boca.</li>
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
            renderInspiration(0);
        }}

        function selectCharacter(idx) {{
            currentIdx = idx;
            document.querySelectorAll(".char-item").forEach((el, i) => {{
                el.classList.toggle("active", i === idx);
            }});
            const char = characters[idx];
            document.getElementById("current-name").textContent = char.name;
            document.getElementById("inspiration-header").textContent = `Inspiración 2.5D: ${{char.name}}`;
            
            renderSilhouette();
            renderInspiration(idx);
        }}

        function renderInspiration(idx) {{
            const container = document.getElementById("inspiration-cards-container");
            if (idx === 0) {{
                container.innerHTML = dinoBebeCardsHTML;
            }} else {{
                const char = characters[idx];
                container.innerHTML = `
                    <div class="card-style" style="text-align: center; padding: 28px 16px;">
                        <span class="card-badge badge-pop">PALETA SUGERIDA</span>
                        <div class="card-name" style="margin-top: 10px; font-size: 1rem;">${{char.name}}</div>
                        <p class="card-desc" style="margin-top: 8px;">
                            ¡Explora expresiones únicas! Puedes dibujarlo con <strong>1 ojo gigante cíclope</strong> o con <strong>2 ojos tiernos</strong> según su personalidad.
                        </p>
                        <div class="palette-row" style="margin-top: 16px;">
                            <div class="palette-chip" style="background: #0284c7;" title="Azul"></div>
                            <div class="palette-chip" style="background: #fbbf24;" title="Amarillo"></div>
                            <div class="palette-chip" style="background: #10b981;" title="Verde"></div>
                            <div class="palette-chip" style="background: #f43f5e;" title="Rojo"></div>
                            <div class="palette-chip" style="background: #0f172a;" title="Negro"></div>
                        </div>
                        <div style="margin-top: 24px; font-size: 0.75rem; color: var(--text-muted); background: #f8fafc; padding: 14px; border-radius: 8px; border: 1px solid var(--border); line-height: 1.45;">
                            💡 <strong>Tip de Pintado Posca:</strong><br>
                            Usa la guía central de ojos y bocas. Primero dibuja la forma principal con plumón negro, deja secar 1 minuto y añade los brillos blancos.
                        </div>
                        <button onclick="selectCharacter(0)" style="margin-top: 20px; background: var(--primary-light); color: var(--primary); border: 1px solid #bae6fd; padding: 8px 14px; border-radius: 6px; font-weight: 600; font-size: 0.75rem; cursor: pointer;">
                            ⬅ Ver ejemplos 2.5D de Dino Bebé 1
                        </button>
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

print("estacion_05_acabado_color.html generated successfully!")
