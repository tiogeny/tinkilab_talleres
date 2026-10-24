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
            padding: 10px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-shrink: 0;
        }}

        .header-title h1 {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-title);
            letter-spacing: -0.02em;
        }}

        .header-title p {{
            font-size: 0.78rem;
            color: var(--text-muted);
        }}

        .header-badges {{
            display: flex;
            gap: 8px;
        }}

        .badge {{
            font-size: 0.72rem;
            font-weight: 600;
            padding: 3px 10px;
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
            grid-template-columns: 240px 1fr;
            overflow: hidden;
        }}

        /* Columna 1: Lista de Siluetas */
        .sidebar-list {{
            background-color: var(--bg-card);
            border-right: 1px solid var(--border);
            overflow-y: auto;
            padding: 12px;
        }}

        .sidebar-title {{
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 10px;
            padding-left: 4px;
        }}

        .char-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 10px;
            border-radius: 8px;
            cursor: pointer;
            border: 1px solid transparent;
            margin-bottom: 4px;
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
            width: 28px;
            height: 28px;
            flex-shrink: 0;
        }}

        .char-item.active svg path {{
            fill: var(--primary);
        }}

        .char-item-name {{
            font-size: 0.8rem;
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

        /* Columna 2: Canvas Principal */
        .main-content {{
            padding: 18px 24px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        /* Tarjeta Superior: Silueta Proporcional Grande (140 mm visible) + Información */
        .top-hero-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px 24px;
            display: flex;
            align-items: center;
            gap: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            flex-shrink: 0;
        }}

        .silhouette-box {{
            width: 140px;
            height: 140px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f8fafc;
            border-radius: 10px;
            border: 2px dashed #cbd5e1;
            padding: 10px;
            flex-shrink: 0;
            transition: all 0.2s ease;
        }}

        .silhouette-box svg {{
            width: 100%;
            height: 100%;
            max-width: 120px;
            max-height: 120px;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
        }}

        .hero-details {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            flex: 1;
        }}

        .hero-title-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .hero-title {{
            font-size: 1.25rem;
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

        .hero-instruction {{
            font-size: 0.82rem;
            color: var(--text-body);
            line-height: 1.4;
        }}

        .hero-features {{
            display: flex;
            gap: 12px;
            margin-top: 2px;
        }}

        .hero-feature-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.74rem;
            color: var(--text-muted);
            background: #f8fafc;
            padding: 4px 10px;
            border-radius: 6px;
            border: 1px solid var(--border);
        }}

        /* Sección Inferior: 3 Renders en Fila Horizontal */
        .bottom-section {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            flex: 1;
        }}

        .section-title {{
            font-size: 0.88rem;
            font-weight: 700;
            color: var(--text-title);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .cards-row-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            align-items: stretch;
        }}

        .render-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 14px;
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
            margin-bottom: 4px;
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
            font-size: 0.88rem;
            font-weight: 700;
            color: var(--text-title);
            margin-bottom: 4px;
        }}

        .card-desc {{
            font-size: 0.74rem;
            color: var(--text-muted);
            line-height: 1.35;
            margin-bottom: 10px;
            min-height: 32px;
        }}

        /* Contenedor de la Imagen: RENDER COMPLETO */
        .render-img-box {{
            width: 100%;
            height: 230px;
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 10px;
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
            margin-bottom: 8px;
        }}

        .palette-chip {{
            flex: 1;
            height: 20px;
            border-radius: 4px;
            border: 1px solid rgba(0,0,0,0.12);
        }}

        .tips-list {{
            font-size: 0.72rem;
            color: #475569;
            padding-left: 16px;
            line-height: 1.35;
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
            <p>Guía de Inspiración y Pintura de DigiToys 2.5D con Marcadores Posca</p>
        </div>
        <div class="header-badges">
            <span class="badge">Altura: 70 mm</span>
            <span class="badge">Espesor: 15 mm</span>
            <span class="badge highlight">Marcadores Acrílicos Posca</span>
        </div>
    </header>

    <div class="main-layout">
        <!-- Columna 1: Lista de Siluetas -->
        <aside class="sidebar-list">
            <div class="sidebar-title">12 Siluetas Oficiales</div>
            <div id="character-list"></div>
        </aside>

        <!-- Columna 2: Canvas Principal -->
        <main class="main-content">
            <!-- Tarjeta Superior: Silueta Proporcional Grande + Información Limpia -->
            <div class="top-hero-card">
                <div class="silhouette-box" id="silhouette-display">
                    <!-- Inyectado por JS -->
                </div>
                <div class="hero-details">
                    <div class="hero-title-row">
                        <div class="hero-title" id="current-name">01 Dino Bebé 1</div>
                        <div class="hero-scale-badge">Silueta Base 1:1 (70 mm)</div>
                    </div>
                    <div class="hero-instruction">
                        Esta es la silueta 3D original que tendrás en tus manos. Boceta primero la carita en tu <strong>Ficha de Diseño 2D</strong> y luego píntala en 3D inspirándote en cualquiera de las 3 opciones de abajo:
                    </div>
                    <div class="hero-features">
                        <span class="hero-feature-item">📍 <strong>Escala:</strong> 70 mm alto</span>
                        <span class="hero-feature-item">🧱 <strong>Espesor:</strong> 15 mm (base estable)</span>
                        <span class="hero-feature-item">🎨 <strong>Base:</strong> Filamento neutro / blanco</span>
                    </div>
                </div>
            </div>

            <!-- Sección Inferior: 3 Renders en Fila Horizontal -->
            <div class="bottom-section">
                <div class="section-title">
                    <span>🎨</span> 3 Opciones de Inspiración & Color (Pieza 2.5D Real)
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

        const characterRenders = {{
            "01_dino_bebe_1": [
                {{ badge: "ESTILO 01", type: "badge-pop", tag: "1 Ojo Cartoon", name: "Color Pop / Menta & Amarillo", desc: "Cuerpo menta, barriga amarilla plana, ojo grande lateral con doble brillo blanco y mejilla rosa.", img: "inspiracion/01_dino_bebe_25d_pop.jpg", palette: ["#10b981", "#fbbf24", "#f43f5e", "#0f172a"], tips: ["Barriga pintada con doble pasada de amarillo Posca.", "Ojo grande cartoon con dos puntos de luz blancos."] }},
                {{ badge: "ESTILO 02", type: "badge-kawaii", tag: "Ojo Manga / Estrella", name: "Pastel Kawaii / Lila & Melocotón", desc: "Cuerpo lila suave, barriga melocotón cálido, ojo manga con destello de estrella y rubor dulce.", img: "inspiracion/01_dino_bebe_25d_kawaii.jpg", palette: ["#c4b5fd", "#fdba74", "#f472b6", "#ffffff"], tips: ["Colores pastel relajantes ideales para los más pequeños.", "Destellos de estrella en el ojo con plumón blanco fino."] }},
                {{ badge: "ESTILO 03", type: "badge-monster", tag: "Monstruito / Colmillo", name: "Monstruo Travieso / Turquesa & Naranja", desc: "Cuerpo turquesa, manchas circulares naranjas en el lomo y sonrisa traviesa con colmillito blanco.", img: "inspiracion/01_dino_bebe_25d_monster.jpg", palette: ["#06b6d4", "#f97316", "#0f172a", "#ffffff"], tips: ["Manchas circulares de diferente diámetro en el lomo.", "Dientecito triangular blanco en la esquina de la boca."] }}
            ],
            "02_dino_bebe_2": [
                {{ badge: "ESTILO 01", type: "badge-pop", tag: "1 Cíclope Pop", name: "Rosa Coral & Amarillo", desc: "Cuerpo rosa coral, barriga amarilla y un gran ojo cíclope central con iris azul y reflejo blanco.", img: "inspiracion/02_dino_bebe_2_25d_pop.jpg", palette: ["#fb7185", "#facc15", "#0284c7", "#0f172a"], tips: ["Ojo central grande y expresivo en medio de la cabeza.", "Boca alegre en arco debajo del ojo."] }},
                {{ badge: "ESTILO 02", type: "badge-kawaii", tag: "2 Ojos Kawaii", name: "Menta Pastel & Lila", desc: "Cuerpo verde menta suave, barriga lila pastel, 2 ojos brillantes y mejillas sonrosadas.", img: "inspiracion/02_dino_bebe_2_25d_kawaii.jpg", palette: ["#6ee7b7", "#d8b4fe", "#fda4af", "#ffffff"], tips: ["Dos ojos paralelos con destellos dobles.", "Colores súper suaves y amigables."] }},
                {{ badge: "ESTILO 03", type: "badge-monster", tag: "Monstruo / Colmillo", name: "Naranja Eléctrico & Púrpura", desc: "Cuerpo naranja brillante con manchas circulares púrpuras en el lomo y sonrisa con colmillito.", icon: "⚡", palette: ["#f97316", "#a855f7", "#0f172a", "#ffffff"], tips: ["Manchas circulares en el lomo.", "Dientecito blanco triangular."] }}
            ],
            "03_fantasmita": [
                {{ badge: "ESTILO 01", type: "badge-pop", tag: "Clásico Fantasmal", name: "Blanco Crema & Cian", desc: "Cuerpo blanco crema con contorno cian suave, dos ojazos negros expresivos y boca abierta alegre en 'O'.", img: "inspiracion/03_fantasmita_25d_pop.jpg", palette: ["#f8fafc", "#38bdf8", "#0f172a", "#ffffff"], tips: ["Ojos grandes ovalados con brillo blanco brillante.", "Boca en forma de 'O' flotante."] }},
                {{ badge: "ESTILO 02", type: "badge-kawaii", tag: "1 Ojo Cósmico", name: "Lila Estelar & Amarillo", desc: "Cuerpo lila suave con un único ojo cósmico central y mejillas con destellos de estrella.", icon: "⭐", palette: ["#c084fc", "#fde047", "#fda4af", "#ffffff"], tips: ["Ojo central con pupila violeta y estrella blanca.", "Rubor cálido en los lados."] }},
                {{ badge: "ESTILO 03", type: "badge-monster", tag: "Espíritu Travieso", name: "Turquesa & Lengüita Rosa", desc: "Cuerpo turquesa con un ojo guiñado, lengua rosa traviesa afuera y puntitos de confeti flotantes.", icon: "👻", palette: ["#06b6d4", "#f43f5e", "#fde047", "#0f172a"], tips: ["Guiño feliz con pestañas marcadas.", "Lengüita rosa saliendo de la boca."] }}
            ],
            "04_frijolito": [
                {{ badge: "ESTILO 01", type: "badge-pop", tag: "2 Puntos / Tierno", name: "Amarillo Mostaza & Crema", desc: "Cuerpo amarillo cálido, pecho crema, dos ojos de punto simples y limpios, y sonrisa feliz con pecas.", img: "inspiracion/04_frijolito_25d_pop.jpg", palette: ["#f59e0b", "#fef3c7", "#f43f5e", "#0f172a"], tips: ["Puntos negros súper limpios para los ojos.", "Pecas y rubor suave en las mejillas."] }},
                {{ badge: "ESTILO 02", type: "badge-monster", tag: "1 Cíclope Alien", name: "Verde Lima & Rayas Tigre", desc: "Cuerpo verde lima con rayas atigradas oscuras y un ojo cíclope gigante con iris púrpura y doble brillo.", img: "inspiracion/04_frijolito_25d_monster.jpg", palette: ["#84cc16", "#15803d", "#a855f7", "#0f172a"], tips: ["Ojo gigante en el centro de la cabeza.", "Rayas horizontales en el cuerpo."] }},
                {{ badge: "ESTILO 03", type: "badge-kawaii", tag: "Fresa Kawaii", name: "Rosa Pastel & Lunares", desc: "Cuerpo rosa pastel con ojitos felices cerrados (^ ^) y pequeñas motas estilo semilla de fresa.", icon: "🍓", palette: ["#f472b6", "#fee2e2", "#dc2626", "#0f172a"], tips: ["Ojos curvados felices hacia arriba.", "Boca abierta sonriente."] }}
            ],
            "05_monstruo_cuernitos": [
                {{ badge: "ESTILO 01", type: "badge-pop", tag: "1 Cíclope Neón", name: "Azul Cobalto & Amarillo", desc: "Cuerpo azul cobalto, barriga amarillo neón, cuernitos blancos limpios y un gran ojo cíclope central.", img: "inspiracion/05_monstruo_cuernitos_25d_pop.jpg", palette: ["#1d4ed8", "#facc15", "#ffffff", "#0f172a"], tips: ["Cuernos en blanco limpio de alto contraste.", "Ojo central grande y amigable."] }},
                {{ badge: "ESTILO 02", type: "badge-kawaii", tag: "Cuernos Bastón", name: "Lila Dormilón & Caramelo", desc: "Cuerpo lila pastel, cuernitos con rayas de caramelo rojas y blancas, y ojos dormilones serenos.", img: "inspiracion/05_monstruo_cuernitos_25d_kawaii.jpg", palette: ["#c084fc", "#ef4444", "#ffffff", "#0f172a"], tips: ["Líneas rojas diagonales en los cuernos.", "Líneas de ojos cerrados descansando."] }},
                {{ badge: "ESTILO 03", type: "badge-monster", tag: "Ojos Desiguales", name: "Naranja & Colmillitos", desc: "Cuerpo naranja con manchas verde azuladas, dos ojos de distinto tamaño (uno grande, uno chico) y colmillitos.", icon: "👹", palette: ["#ea580c", "#0d9488", "#0f172a", "#ffffff"], tips: ["Un ojo grande y otro más pequeño para toque pícaro.", "Dos dientes triangulares blancos hacia arriba."] }}
            ]
        }};

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
            const char = characters[idx];
            const data = characterRenders[char.id];

            if (data && data.length === 3) {{
                let html = "";
                data.forEach(item => {{
                    let imgHtml = "";
                    if (item.img) {{
                        imgHtml = `<img src="${{item.img}}" alt="${{item.name}}">`;
                    }} else {{
                        imgHtml = `
                            <div style="font-size: 2.2rem;">${{item.icon || "✨"}}</div>
                            <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600;">Próximamente Render 2.5D</div>
                        `;
                    }}

                    let paletteHtml = "";
                    item.palette.forEach(color => {{
                        paletteHtml += `<div class="palette-chip" style="background: ${{color}};"></div>`;
                    }});

                    let tipsHtml = "";
                    item.tips.forEach(tip => {{
                        tipsHtml += `<li>${{tip}}</li>`;
                    }});

                    html += `
                        <div class="render-card">
                            <div class="card-header-row">
                                <span class="card-badge ${{item.type}}">${{item.badge}}</span>
                                <span style="font-size: 0.68rem; font-weight: 600;">${{item.tag}}</span>
                            </div>
                            <div class="card-name">${{item.name}}</div>
                            <div class="card-desc">${{item.desc}}</div>
                            <div class="render-img-box" ${{!item.img ? 'style="flex-direction: column; background: #f8fafc; border: 2px dashed #cbd5e1; gap: 8px;"' : ''}}>
                                ${{imgHtml}}
                            </div>
                            <div class="palette-row">
                                ${{paletteHtml}}
                            </div>
                            <ul class="tips-list">
                                ${{tipsHtml}}
                            </ul>
                        </div>
                    `;
                }});
                container.innerHTML = html;
            }} else {{
                container.innerHTML = `
                    <div class="render-card">
                        <div class="card-header-row">
                            <span class="card-badge badge-pop">PROPUESTA 01</span>
                            <span style="font-size: 0.68rem; color: #15803d; font-weight: 600;">1 Ojo Cíclope</span>
                        </div>
                        <div class="card-name">Estilo Alien / Cíclope Pop</div>
                        <div class="card-desc">Un único ojo gigante central con iris brillante y pupila negra con doble reflejo.</div>
                        <div class="render-img-box" style="flex-direction: column; background: #f8fafc; border: 2px dashed #cbd5e1; gap: 8px;">
                            <div style="font-size: 2.2rem;">👁️</div>
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
                        <div class="card-desc">Dos ojitos juntos con expresión tierna, pecas y barriga de color contrastante.</div>
                        <div class="render-img-box" style="flex-direction: column; background: #f8fafc; border: 2px dashed #cbd5e1; gap: 8px;">
                            <div style="font-size: 2.2rem;">👀</div>
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
                            <div style="font-size: 2.2rem;">⚡</div>
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

print("estacion_05_acabado_color.html updated with dynamic renders for 01-05!")
