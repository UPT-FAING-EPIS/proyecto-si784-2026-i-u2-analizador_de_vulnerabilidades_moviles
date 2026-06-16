import os

import pandas as pd
import streamlit as st

from app.dashboard.config.settings import DashboardSettings
from app.dashboard.config.styles import severity_icon

# ── Definición del menú de navegación ─────────────────────────────────────────
NAV_ITEMS = [
    {"key": "inicio",     "icon": "🏠", "label": "Inicio"},
    {"key": "escanear",   "icon": "📤", "label": "Escanear APK"},
    {"key": "historial",  "icon": "📋", "label": "Historial APK"},
    {"key": "comunidad",  "icon": "🌐", "label": "Comunidad"},
    {"key": "agente",     "icon": "🤖", "label": "Agente Móvil"},
    {"key": "manual",     "icon": "🔎", "label": "Escaneo Manual"},
    {"key": "repo_calidad", "icon": "📦", "label": "Calidad Repo"},
]


from app.dashboard.config.kb import APK_FINDING_KB, APK_ARTIFACT_KB


class DashboardView:
    # ── APK download ──────────────────────────────────────────────────────────
    def render_apk_download(self, apk_path, filename):
        with open(apk_path, "rb") as apk_file:
            st.download_button(
                label="⬇️  Descargar AnzenCore APK",
                data=apk_file,
                file_name=filename,
                mime="application/vnd.android.package-archive",
                use_container_width=True,
            )

    # ── Login ─────────────────────────────────────────────────────────────────
    def render_login(self):
        st.markdown(
            """
            <div class="login-card">
                <div class="login-logo">🛡️</div>
                <div class="login-title">AnzenCore</div>
                <div class="login-subtitle">Plataforma de seguridad móvil</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        _, col, _ = st.columns([1, 3, 1])
        with col:
            tab1, tab2 = st.tabs(["🔑  Iniciar sesión", "✨  Crear cuenta"])
            with tab1:
                username = st.text_input("Usuario", key="l_u", placeholder="Tu usuario")
                password = st.text_input(
                    "Contraseña", type="password", key="l_p", placeholder="••••••••"
                )
                login_button = st.button(
                    "Iniciar sesión", use_container_width=True, key="login_btn"
                )
            with tab2:
                new_username = st.text_input(
                    "Nuevo usuario", key="r_u", placeholder="Elige un usuario"
                )
                new_password = st.text_input(
                    "Nueva contraseña", type="password", key="r_p", placeholder="••••••••"
                )
                signup_button = st.button(
                    "Crear cuenta", use_container_width=True, key="signup_btn"
                )

        return username, password, login_button, new_username, new_password, signup_button

    # ── Sidebar con navegación ────────────────────────────────────────────────
    def render_sidebar(self, user):
        active = st.session_state.get("nav_section", "inicio")

        with st.sidebar:
            # Branding
            st.markdown(
                f"""
                <div style="text-align:center; padding: 1rem 0 .5rem;">
                    <div style="font-size:2.5rem;">🛡️</div>
                    <div style="font-size:1.1rem; font-weight:700; color:#00d4ff; margin:.3rem 0 .1rem;">
                        AnzenCore
                    </div>
                    <div style="font-size:.75rem; color:#64748b; letter-spacing:.06em; text-transform:uppercase;">
                        Security Dashboard
                    </div>
                </div>
                <hr style="margin:.75rem 0;"/>
                """,
                unsafe_allow_html=True,
            )

            # Info de usuario (compacta, arriba)
            st.markdown(
                f"""
                <div style="background:rgba(0,212,255,.06); border:1px solid rgba(0,212,255,.18);
                            border-radius:10px; padding:.6rem .9rem; margin-bottom:.75rem;">
                    <div style="font-size:.65rem; color:#64748b; text-transform:uppercase;
                                letter-spacing:.08em; margin-bottom:.2rem;">Usuario activo</div>
                    <div style="font-weight:700; color:#e2e8f0; font-size:.9rem;">
                        👤 {user['username']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Menú de navegación
            st.markdown(
                '<div class="nav-section-label">Navegación</div>',
                unsafe_allow_html=True,
            )
            for item in NAV_ITEMS:
                is_active = active == item["key"]
                css_class = "nav-btn-active" if is_active else "nav-btn"
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                if st.button(
                    f"{item['icon']}  {item['label']}",
                    key=f"nav_{item['key']}",
                    use_container_width=True,
                ):
                    st.session_state.nav_section = item["key"]
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            # Separador y botón de cierre de sesión (siempre visible)
            st.markdown("<hr/>", unsafe_allow_html=True)
            st.markdown(
                """
                <style>
                div[data-testid="stSidebar"] div[data-testid="stButton"]:last-of-type > button {
                    background: rgba(255,71,87,.12) !important;
                    border: 1px solid rgba(255,71,87,.5) !important;
                    color: #ff4757 !important;
                    font-weight: 600 !important;
                    width: 100% !important;
                }
                div[data-testid="stSidebar"] div[data-testid="stButton"]:last-of-type > button:hover {
                    background: rgba(255,71,87,.25) !important;
                    box-shadow: 0 0 16px rgba(255,71,87,.3) !important;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            logout = st.button(
                "🚪  Cerrar sesión",
                use_container_width=True,
                key="logout_btn",
            )

            st.markdown(
                """
                <div style="font-size:.68rem; color:#64748b; text-align:center; margin-top:.6rem;">
                    AnzenCore v1.0 · Seguridad Móvil
                </div>
                """,
                unsafe_allow_html=True,
            )

        return logout

    # ── Router principal ──────────────────────────────────────────────────────
    def render_dashboard(self, user, reports, apk_scans, controller):
        section = st.session_state.get("nav_section", "inicio")
        nav_meta = next((n for n in NAV_ITEMS if n["key"] == section), NAV_ITEMS[0])

        # Breadcrumb de sección
        st.markdown(
            f"""
            <div class="page-header">
                🛡️ AnzenCore &nbsp;›&nbsp; <span>{nav_meta['icon']} {nav_meta['label']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if section == "inicio":
            self._render_inicio(user, reports, apk_scans)
        elif section == "escanear":
            self.render_apk_scanner(user, controller)
        elif section == "historial":
            self.render_apk_scan_history(user, apk_scans, controller)
        elif section == "comunidad":
            self.render_comunidad()
        elif section == "agente":
            self.render_vulnerability_history(reports)
        elif section == "manual":
            self.render_manual_scan(controller)
        elif section == "repo_calidad":
            self.render_repo_quality(controller)

    # ── Inicio / Overview ─────────────────────────────────────────────────────
    def _render_inicio(self, user, reports, apk_scans):
        st.markdown(
            f"""
            <div style="margin-bottom:1.5rem;">
                <h1 style="margin:0;">Bienvenido, {user['username']} 👋</h1>
                <div style="color:#64748b; font-size:.9rem; margin-top:.25rem;">
                    Resumen de actividad de seguridad
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📱 APKs analizados", len(apk_scans) if apk_scans else 0)

        # Total de hallazgos = suma de findings_count en todos los escaneos del usuario
        total_findings = sum(s.get("findings_count", 0) for s in apk_scans) if apk_scans else 0
        c2.metric("🔍 Hallazgos totales", total_findings)

        # Usuarios online (desde session_state, actualizado por el fragment)
        online_users = st.session_state.get("online_users", [])
        c3.metric("🌐 Online ahora", len(online_users))

        # Reportes del agente móvil
        agent_reports = len(reports) if reports else 0
        scan_results = len(st.session_state.get("scan_results", []))
        c4.metric("🤖 Reportes del agente", agent_reports + scan_results)

        st.divider()

        # Descarga APK agente
        col_apk, col_info = st.columns([1, 2])
        with col_apk:
            st.markdown("### 📲 Agente móvil")
            apk_path = DashboardSettings.apk_path
            if os.path.exists(apk_path) and os.path.getsize(apk_path) > 0:
                self.render_apk_download(apk_path, DashboardSettings.apk_filename)
            else:
                st.error("APK no disponible en /assets")

        with col_info:
            st.markdown("### 📊 Últimos escaneos")
            if apk_scans:
                df = pd.DataFrame(apk_scans[:5])
                display_cols = [c for c in ["file_name", "status", "severity_max", "created_at"] if c in df.columns]
                st.dataframe(
                    df[display_cols].rename(columns={
                        "file_name": "APK", "status": "Estado",
                        "severity_max": "Severidad", "created_at": "Fecha",
                    }),
                    use_container_width=True, hide_index=True,
                )
            else:
                st.markdown(
                    """
                    <div style="text-align:center; padding:1.5rem; background:rgba(17,24,39,.6);
                                border:1px dashed rgba(0,212,255,.2); border-radius:12px; color:#64748b;">
                        <div style="font-size:1.5rem;">📭</div>
                        <div style="margin-top:.4rem;">Sin escaneos aún. Ve a <b>Escanear APK</b>.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ── APK scanner ───────────────────────────────────────────────────────────
    def render_apk_scanner(self, user, controller):
        st.markdown("## 📤 Escanear APK")
        st.markdown(
            "<div style='color:#64748b; font-size:.88rem; margin-bottom:1rem;'>"
            "Sube un archivo APK para analizarlo por ingeniería inversa y detectar vulnerabilidades."
            "</div>",
            unsafe_allow_html=True,
        )
        col_upload, col_btn = st.columns([3, 1])
        with col_upload:
            uploaded_file = st.file_uploader(
                "Selecciona un archivo APK",
                type=["apk"],
                label_visibility="collapsed",
            )
        with col_btn:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            scan_btn = st.button("🔍  Analizar", use_container_width=True)

        if scan_btn:
            with st.spinner("⚙️  Analizando APK por ingeniería inversa..."):
                ok, result = controller.create_apk_scan(user["id"], uploaded_file)
            if ok:
                st.success(f"✅ {result['message']}")
                st.markdown("### 📊 Resultados del análisis")
                
                scan_id = result["scan_id"]
                apk_scans = controller.fetch_apk_scans(user["id"])
                selected_scan = next((s for s in apk_scans if s.get("id") == scan_id), None)
                
                if selected_scan:
                    findings = controller.fetch_apk_findings(scan_id)
                    artifacts = controller.fetch_apk_artifacts(scan_id)
                    self.render_scan_detail(user, selected_scan, findings, artifacts, controller)
            else:
                st.error(f"❌ {result}")

    # ── APK scan history ──────────────────────────────────────────────────────
    def render_apk_scan_history(self, user, apk_scans, controller):
        st.markdown("## 📋 Historial de escaneos APK")

        if not apk_scans:
            st.markdown(
                """
                <div style="text-align:center; padding:2rem; background:rgba(17,24,39,.6);
                            border:1px dashed rgba(0,212,255,.2); border-radius:12px; color:#64748b;">
                    <div style="font-size:2rem; margin-bottom:.5rem;">📭</div>
                    <div>Todavía no hay APKs analizados.</div>
                    <div style="font-size:.8rem; margin-top:.25rem;">Sube un APK en <b>Escanear APK</b>.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        df = pd.DataFrame(apk_scans)

        if "severity_max" in df.columns:
            severity_counts = df["severity_max"].fillna("Info").value_counts().to_dict()
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("🔴 Críticos", severity_counts.get("Critico", 0))
            c2.metric("🟠 Altos", severity_counts.get("Alto", 0))
            c3.metric("🟡 Medios", severity_counts.get("Medio", 0))
            c4.metric(
                "🟢 Bajos / Info",
                severity_counts.get("Bajo", 0) + severity_counts.get("Info", 0),
            )

        display_columns = [
            col for col in
            ["file_name", "package_name", "app_name", "status", "severity_max", "findings_count", "created_at"]
            if col in df.columns
        ]
        history_df = df[display_columns].copy().rename(
            columns={
                "file_name": "APK", "package_name": "Paquete", "app_name": "App",
                "status": "Estado", "severity_max": "Severidad",
                "findings_count": "Hallazgos", "created_at": "Fecha",
            }
        )
        st.dataframe(history_df, use_container_width=True, hide_index=True)

        scan_options = {
            (
                f"{severity_icon(row.get('severity_max', ''))}  "
                f"{row.get('file_name', 'APK')}  ·  "
                f"{row.get('findings_count', 0)} hallazgos  ·  "
                f"{str(row.get('created_at', ''))[:16]}"
            ): row["id"]
            for row in apk_scans
            if row.get("id")
        }
        if not scan_options:
            return

        selected_label = st.selectbox("🔎  Ver detalle de escaneo", options=list(scan_options.keys()))
        selected_scan_id = scan_options[selected_label]
        selected_scan = next(scan for scan in apk_scans if scan.get("id") == selected_scan_id)
        findings = controller.fetch_apk_findings(selected_scan_id)
        artifacts = controller.fetch_apk_artifacts(selected_scan_id)
        self.render_scan_detail(user, selected_scan, findings, artifacts, controller)

    # ── Scan detail ───────────────────────────────────────────────────────────
    def render_scan_detail(self, user, scan, findings, artifacts, controller):
        severity_order = {"Critico": 0, "Alto": 1, "Medio": 2, "Bajo": 3, "Info": 4}
        tab_findings, tab_artifacts, tab_exports = st.tabs(
            ["🔍  Hallazgos", "🗂️  Artefactos", "📤  Exportar"]
        )

        with tab_findings:
            if not findings:
                st.info("Este escaneo no tiene hallazgos registrados.")
            else:
                findings = sorted(findings, key=lambda i: severity_order.get(i.get("severity"), 99))
                for finding in findings:
                    severity = finding.get("severity", "Info")
                    icon = severity_icon(severity)
                    with st.expander(
                        f"{icon}  [{severity}]  {finding.get('title', 'Hallazgo')}  —  {finding.get('finding_type', 'general')}"
                    ):
                        st.markdown(f"**📝 Explicación:**\n{finding.get('description', 'Sin descripción.')}")
                        
                        # Obtener implicación basada en el tipo de hallazgo
                        f_type = finding.get("finding_type", "")
                        kb_info = APK_FINDING_KB.get(f_type, {})
                        implicacion = kb_info.get("implicacion")
                        if implicacion:
                            st.markdown(f"**⚠️ Lo que implica (Riesgo):**\n{implicacion}")
                            
                        if finding.get("evidence"):
                            st.markdown("**🔍 Evidencia / Código vulnerable:**")
                            st.markdown(finding["evidence"])
                            
                        cols = st.columns(2)
                        if finding.get("source_file"):
                            cols[0].caption(f"📄 Fuente: `{finding['source_file']}`")
                        refs = [v for v in [finding.get("cwe"), finding.get("owasp_mobile")] if v]
                        if refs:
                            cols[1].caption("🔗 " + "  /  ".join(refs))
                            
                        # Mostrar recomendación prioritariamente del hallazgo o de la KB
                        rec = finding.get("recommendation") or kb_info.get("recommendation")
                        if rec:
                            st.info(f"💡 **Recomendación:** {rec}")

        with tab_artifacts:
            if not artifacts:
                st.info("Este escaneo no tiene artefactos registrados.")
            else:
                artifact_df = pd.DataFrame(artifacts)
                display_cols = [c for c in ["artifact_type", "artifact_value", "source_file"] if c in artifact_df.columns]
                st.dataframe(
                    artifact_df[display_cols].rename(columns={
                        "artifact_type": "Tipo", "artifact_value": "Valor", "source_file": "Fuente"
                    }),
                    use_container_width=True, hide_index=True,
                )

                st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
                st.markdown("### 💡 Guía de análisis de artefactos")
                # Obtener tipos únicos presentes en este escaneo
                unique_types = sorted(list({a.get("artifact_type") for a in artifacts if a.get("artifact_type")}))
                for a_type in unique_types:
                    kb_info = APK_ARTIFACT_KB.get(a_type)
                    if kb_info:
                        with st.expander(f"📁  {kb_info['titulo']} ({a_type})"):
                            st.markdown(f"**📝 Explicación:**\n{kb_info['descripcion']}")
                            st.info(f"💡 **Recomendación:** {kb_info['recommendation']}")

        with tab_exports:
            st.markdown("**Exporta el resultado del escaneo seleccionado**")
            pdf_name, pdf_data = controller.build_report_export(scan, findings, artifacts, "pdf", user["id"])
            st.download_button("📕  Descargar PDF", data=pdf_data, file_name=pdf_name, mime="application/pdf", use_container_width=True)

    # ── Comunidad ─────────────────────────────────────────────────────────────
    def render_comunidad(self):
        online_users = st.session_state.get("online_users", [])
        total = len(online_users)

        st.markdown(
            f"""
            <div style="margin-bottom:1.5rem;">
                <h1 style="margin:0;">Comunidad</h1>
                <div style="color:#64748b; font-size:.9rem; margin-top:.25rem;">
                    Usuarios activos en los últimos 30 segundos
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Métrica principal
        col_m, col_info = st.columns([1, 3])
        col_m.metric("🌐 Usuarios online", total)
        with col_info:
            st.markdown(
                """
                <div style="background:rgba(0,255,136,.05); border:1px solid rgba(0,255,136,.15);
                            border-radius:10px; padding:.75rem 1.1rem; font-size:.85rem; color:#64748b;
                            display:flex; align-items:center; gap:.6rem; height:100%;">
                    <span class="online-dot"></span>
                    La lista se actualiza automáticamente cada 30 segundos sin recargar la página.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.divider()

        if not online_users:
            st.markdown(
                """
                <div style="text-align:center; padding:3rem 2rem; background:rgba(17,24,39,.6);
                            border:1px dashed rgba(0,255,136,.2); border-radius:14px; color:#64748b;">
                    <div style="font-size:2.5rem; margin-bottom:.75rem;">🌐</div>
                    <div style="font-size:1rem; font-weight:600; color:#e2e8f0;">
                        Solo tú estás conectado ahora mismo
                    </div>
                    <div style="font-size:.85rem; margin-top:.4rem;">
                        Cuando otros usuarios inicien sesión aparecerán aquí.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        # Grid de tarjetas de usuarios
        cols_per_row = 3
        rows = [online_users[i:i + cols_per_row] for i in range(0, len(online_users), cols_per_row)]

        for row in rows:
            cols = st.columns(cols_per_row)
            for idx, u in enumerate(row):
                with cols[idx]:
                    # Iniciales del usuario para el avatar
                    initials = u["username"][:2].upper()
                    st.markdown(
                        f"""
                        <div style="
                            background: linear-gradient(135deg, rgba(17,24,39,.95), rgba(26,34,53,.95));
                            border: 1px solid rgba(0,255,136,.25);
                            border-radius: 14px;
                            padding: 1.25rem 1rem;
                            text-align: center;
                            transition: transform .2s, border-color .2s;
                            margin-bottom: .5rem;
                        ">
                            <div style="
                                width: 52px; height: 52px;
                                background: linear-gradient(135deg, #00d4ff22, #00ff8822);
                                border: 2px solid rgba(0,255,136,.4);
                                border-radius: 50%;
                                display: flex; align-items: center; justify-content: center;
                                font-size: 1.1rem; font-weight: 700;
                                color: #00ff88;
                                margin: 0 auto .75rem;
                                font-family: 'JetBrains Mono', monospace;
                            ">{initials}</div>
                            <div style="font-weight:700; font-size:.95rem; color:#e2e8f0; margin-bottom:.4rem;">
                                {u['username']}
                            </div>
                            <div style="
                                display: inline-flex; align-items: center; gap: .35rem;
                                background: rgba(0,255,136,.08);
                                border: 1px solid rgba(0,255,136,.2);
                                border-radius: 20px;
                                padding: .2rem .65rem;
                                font-size: .72rem; color: #00ff88; font-weight: 600;
                            ">
                                <span class="online-dot" style="width:6px;height:6px;"></span>
                                Activo
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    # ── Online users (usado por el fragment en main.py) ───────────────────────
    def render_online_users(self, online_users):
        st.markdown(
            '<div class="nav-section-label" style="padding:.4rem .2rem .6rem;">🌐 Usuarios online ahora</div>',
            unsafe_allow_html=True,
        )
        if not online_users:
            st.markdown(
                '<span class="online-dot"></span><span style="color:#64748b; font-size:.82rem;"> Solo tú estás online.</span>',
                unsafe_allow_html=True,
            )
            return
        for u in online_users:
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:.5rem; padding:.35rem .5rem;
                            border-radius:7px; margin:.15rem 0; background:rgba(0,255,136,.05);
                            border:1px solid rgba(0,255,136,.15);">
                    <span class="online-dot"></span>
                    <span style="font-size:.82rem; font-weight:500;">{u['username']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Vulnerability history ─────────────────────────────────────────────────
    def render_vulnerability_history(self, reports):
        st.markdown("## 🤖 Historial del agente móvil")
        st.markdown(
            "<div style='color:#64748b; font-size:.88rem; margin-bottom:1rem;'>"
            "Reportes de seguridad de dispositivos y análisis de red auxiliar."
            "</div>",
            unsafe_allow_html=True,
        )
        combined_reports = reports.copy() if reports else []
        
        # Evitar duplicados basados en vulnerabilidad, dispositivo y fecha
        saved_keys = set()
        for r in combined_reports:
            saved_keys.add((r.get("vulnerabilidad"), r.get("dispositivo"), r.get("fecha")))
            
        if st.session_state.get("scan_results"):
            for sr in st.session_state.scan_results:
                key = (sr.get("vulnerabilidad"), sr.get("dispositivo"), sr.get("fecha"))
                if key not in saved_keys:
                    combined_reports.append(sr)

        if combined_reports:
            severity_order = {"Critico": 0, "Crítico": 0, "Alto": 1, "Medio": 2, "Bajo": 3, "Info": 4}
            # Ordenar por severidad (más crítico primero) y luego por fecha (más reciente primero)
            combined_reports = sorted(
                combined_reports,
                key=lambda r: (severity_order.get(r.get("nivel", "Info"), 99), r.get("fecha", "")),
                reverse=False
            )

            # Mostrar tabla resumen de métricas/vista general
            df = pd.DataFrame(combined_reports)
            display_cols = [c for c in ["dispositivo", "vulnerabilidad", "nivel", "fecha"] if c in df.columns]
            
            st.markdown("### 📊 Vista general de hallazgos")
            st.dataframe(
                df[display_cols].rename(columns={
                    "dispositivo": "Dispositivo / IP",
                    "vulnerabilidad": "Vulnerabilidad",
                    "nivel": "Severidad",
                    "fecha": "Fecha"
                }),
                use_container_width=True,
                hide_index=True
            )

            st.markdown("### 🔍 Detalle técnico y remediación")
            for vuln in combined_reports:
                nivel = vuln.get("nivel", "Info")
                icon = severity_icon(nivel)
                raw_fecha = vuln.get("fecha", "")
                fecha_str = str(raw_fecha)[:16].replace("T", " ") if raw_fecha else "Fecha no registrada"
                
                with st.expander(
                    f"{icon}  [{nivel}]  {vuln.get('vulnerabilidad', 'Vulnerabilidad')}  ·  "
                    f"📱 {vuln.get('dispositivo', 'Dispositivo')}  ·  📅 {fecha_str}"
                ):
                    st.markdown(f"**📝 Explicación:**\n{vuln.get('descripcion', 'Sin descripción.')}")
                    
                    implicacion = vuln.get("implicacion")
                    if implicacion:
                        st.markdown(f"**⚠️ Lo que implica (Riesgo):**\n{implicacion}")
                        
                    rec = vuln.get("recommendation")
                    if rec:
                        st.info(f"💡 **Recomendación:** {rec}")
                        
                    refs = [v for v in [vuln.get("cwe"), vuln.get("owasp")] if v]
                    if refs:
                        st.caption("🔗 " + "  /  ".join(refs))
        else:
            st.markdown(
                """
                <div style="text-align:center; padding:2rem; background:rgba(17,24,39,.6);
                            border:1px dashed rgba(0,212,255,.2); border-radius:12px; color:#64748b;">
                    <div style="font-size:2rem; margin-bottom:.5rem;">📡</div>
                    <div>Esperando reportes del agente móvil o escaneos manuales...</div>
                    <div style="font-size:.8rem; margin-top:.25rem;">
                        Realiza un escaneo manual o instala el APK en tu dispositivo para comenzar a recibir datos.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Manual scan ───────────────────────────────────────────────────────────
    def render_manual_scan(self, controller):
        st.markdown("## 🔎 Escaneo manual auxiliar")
        st.markdown(
            "<div style='color:#64748b; font-size:.88rem; margin-bottom:1rem;'>"
            "Escanea una URL, IP o el dispositivo local en busca de vulnerabilidades de red."
            "</div>",
            unsafe_allow_html=True,
        )
        col_input, col_btn = st.columns([3, 1])
        with col_input:
            target = st.text_input(
                "Objetivo",
                key="scan_target",
                placeholder="https://ejemplo.com · 192.168.1.1 · (vacío = local)",
                label_visibility="collapsed",
            )
        with col_btn:
            scan_btn = st.button("⚡  Escanear", key="scan_btn", use_container_width=True)

        if scan_btn:
            with st.spinner("🔍  Escaneando..."):
                user_id = st.session_state.user["id"]
                st.session_state.scan_results = controller.scan_vulnerabilities(
                    user_id, target if target else None
                )
            st.rerun()

    # ── Calidad de repositorio (GitHub) ──────────────────────────────────────
    def render_repo_quality(self, controller):
        st.markdown("## 📦 Calidad de Repositorio (GitHub)")
        st.markdown(
            "<div style='color:#64748b; font-size:.88rem; margin-bottom:1rem;'>"
            "Analiza un repositorio público de GitHub consumiendo el servicio externo "
            "de análisis de calidad."
            "</div>",
            unsafe_allow_html=True,
        )

        col_input, col_btn = st.columns([3, 1])
        with col_input:
            repo_url = st.text_input(
                "Repositorio de GitHub",
                key="repo_github_url",
                placeholder="https://github.com/usuario/repo",
                label_visibility="collapsed",
            )
        with col_btn:
            analizar_btn = st.button("🔍  Analizar", key="repo_github_btn", use_container_width=True)

        if analizar_btn:
            if not repo_url:
                st.warning("Ingresa la URL de un repositorio de GitHub.")
            else:
                with st.spinner("⚙️  Analizando repositorio..."):
                    ok, result = controller.analizar_repo_github(repo_url)
                if ok:
                    st.session_state.repo_quality_result = result
                else:
                    st.session_state.repo_quality_result = None
                    st.error(f"❌ {result}")

        result = st.session_state.get("repo_quality_result")
        if result:
            st.success(f"✅ Análisis completado: {result.get('proyecto') or repo_url}")
            c1, c2, c3 = st.columns(3)
            c1.metric("📏 Líneas de código", result.get("lineas_codigo", "-"))
            c2.metric("🧩 Complejidad", result.get("complejidad", "-"))
            c3.metric("🐞 Code smells", result.get("code_smells", "-"))
