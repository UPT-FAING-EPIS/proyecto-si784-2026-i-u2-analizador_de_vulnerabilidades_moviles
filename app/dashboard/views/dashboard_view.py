import os

import pandas as pd
import streamlit as st

from app.dashboard.config.settings import DashboardSettings


class DashboardView:
    def render_apk_download(self, apk_path, filename):
        with open(apk_path, "rb") as apk_file:
            st.download_button(
                label="Descargar AnzenCore APK",
                data=apk_file,
                file_name=filename,
                mime="application/vnd.android.package-archive",
                use_container_width=True,
            )

    def render_login(self):
        st.title("AnzenCore Access")
        tab1, tab2 = st.tabs(["Ingreso", "Registro"])
        with tab1:
            username = st.text_input("Usuario", key="l_u")
            password = st.text_input("Contrasena", type="password", key="l_p")
            login_button = st.button("Iniciar sesion")
        with tab2:
            new_username = st.text_input("Nuevo usuario", key="r_u")
            new_password = st.text_input("Nueva contrasena", type="password", key="r_p")
            signup_button = st.button("Crear cuenta")
        return username, password, login_button, new_username, new_password, signup_button

    def render_sidebar(self, user):
        st.sidebar.title(f"Usuario: {user['username']}")
        st.sidebar.info(f"ID: `{user['id']}`")
        return st.sidebar.button("Cerrar sesion")

    def render_dashboard(self, user, online_users, reports, apk_scans, controller):
        st.title("AnzenCore Live Dashboard")

        c1, c2, c3 = st.columns([1, 1, 1.5])
        c1.metric("Online", len(online_users))
        c2.info(f"Sesion: {user['username']}")

        with c3:
            st.write("**Agente movil**")
            apk_path = DashboardSettings.apk_path
            if os.path.exists(apk_path) and os.path.getsize(apk_path) > 0:
                self.render_apk_download(apk_path, DashboardSettings.apk_filename)
            else:
                st.error("APK no disponible en /assets")

        st.divider()
        self.render_apk_scanner(user, controller)
        st.divider()
        self.render_apk_scan_history(user, apk_scans, controller)
        st.divider()
        self.render_online_users(online_users)
        st.divider()
        self.render_vulnerability_history(reports)
        st.divider()
        self.render_manual_scan(controller)

    def render_apk_scanner(self, user, controller):
        st.subheader("Escanear APK por ingenieria inversa")
        uploaded_file = st.file_uploader("Selecciona un APK", type=["apk"])
        if st.button("Analizar APK", use_container_width=True):
            with st.spinner("Analizando APK..."):
                ok, message = controller.create_apk_scan(user["id"], uploaded_file)
            if ok:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    def render_apk_scan_history(self, user, apk_scans, controller):
        st.subheader("Historial de escaneos APK")
        if not apk_scans:
            st.info("Todavia no hay APKs analizados.")
            return

        df = pd.DataFrame(apk_scans)
        if "severity_max" in df.columns:
            severity_counts = df["severity_max"].fillna("Info").value_counts().to_dict()
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Criticos", severity_counts.get("Critico", 0))
            c2.metric("Altos", severity_counts.get("Alto", 0))
            c3.metric("Medios", severity_counts.get("Medio", 0))
            c4.metric("Bajos/Info", severity_counts.get("Bajo", 0) + severity_counts.get("Info", 0))

        display_columns = [
            col
            for col in [
                "file_name",
                "package_name",
                "app_name",
                "status",
                "severity_max",
                "findings_count",
                "created_at",
            ]
            if col in df.columns
        ]
        history_df = df[display_columns].copy()
        history_df = history_df.rename(
            columns={
                "file_name": "APK",
                "package_name": "Paquete",
                "app_name": "App",
                "status": "Estado",
                "severity_max": "Severidad",
                "findings_count": "Hallazgos",
                "created_at": "Fecha",
            }
        )
        st.dataframe(history_df, use_container_width=True)

        scan_options = {
            f"{row.get('file_name', 'APK')} | {row.get('created_at', '')} | {row.get('findings_count', 0)} hallazgos": row[
                "id"
            ]
            for row in apk_scans
            if row.get("id")
        }
        if not scan_options:
            return

        selected_label = st.selectbox(
            "Ver detalle de escaneo",
            options=list(scan_options.keys()),
        )
        selected_scan_id = scan_options[selected_label]
        selected_scan = next(
            scan for scan in apk_scans if scan.get("id") == selected_scan_id
        )
        findings = controller.fetch_apk_findings(selected_scan_id)
        artifacts = controller.fetch_apk_artifacts(selected_scan_id)
        self.render_scan_detail(user, selected_scan, findings, artifacts, controller)

    def render_scan_detail(self, user, scan, findings, artifacts, controller):
        tab_findings, tab_artifacts, tab_exports = st.tabs(
            ["Hallazgos", "Artefactos", "Exportar"]
        )

        with tab_findings:
            if not findings:
                st.info("Este escaneo no tiene hallazgos registrados.")
            else:
                severity_order = {
                    "Critico": 0,
                    "Alto": 1,
                    "Medio": 2,
                    "Bajo": 3,
                    "Info": 4,
                }
                findings = sorted(
                    findings,
                    key=lambda item: severity_order.get(item.get("severity"), 99),
                )
                for finding in findings:
                    severity = finding.get("severity", "Info")
                    title = finding.get("title", "Hallazgo")
                    finding_type = finding.get("finding_type", "general")
                    with st.expander(f"[{severity}] {title} - {finding_type}"):
                        st.write(finding.get("description", "Sin descripcion."))
                        if finding.get("evidence"):
                            st.code(finding["evidence"])
                        if finding.get("source_file"):
                            st.caption(f"Fuente: {finding['source_file']}")
                        if finding.get("cwe") or finding.get("owasp_mobile"):
                            st.caption(
                                " / ".join(
                                    value
                                    for value in [
                                        finding.get("cwe"),
                                        finding.get("owasp_mobile"),
                                    ]
                                    if value
                                )
                            )
                        if finding.get("recommendation"):
                            st.info(finding["recommendation"])

        with tab_artifacts:
            if not artifacts:
                st.info("Este escaneo no tiene artefactos registrados.")
            else:
                artifact_df = pd.DataFrame(artifacts)
                display_columns = [
                    col
                    for col in ["artifact_type", "artifact_value", "source_file"]
                    if col in artifact_df.columns
                ]
                artifact_df = artifact_df[display_columns].rename(
                    columns={
                        "artifact_type": "Tipo",
                        "artifact_value": "Valor",
                        "source_file": "Fuente",
                    }
                )
                st.dataframe(artifact_df, use_container_width=True)

        with tab_exports:
            st.write("Exporta el resultado del escaneo seleccionado.")
            c1, c2 = st.columns(2)
            with c1:
                csv_name, csv_data = controller.build_report_export(
                    scan,
                    findings,
                    artifacts,
                    "csv",
                    user["id"],
                )
                st.download_button(
                    "Descargar CSV",
                    data=csv_data,
                    file_name=csv_name,
                    mime="text/csv",
                    use_container_width=True,
                )
            with c2:
                json_name, json_data = controller.build_report_export(
                    scan,
                    findings,
                    artifacts,
                    "json",
                    user["id"],
                )
                st.download_button(
                    "Descargar JSON",
                    data=json_data,
                    file_name=json_name,
                    mime="application/json",
                    use_container_width=True,
                )

    def render_online_users(self, online_users):
        st.subheader("Monitor en tiempo real")
        user_list = [f"`{u['username']}`" for u in online_users]
        st.write(" ".join(user_list) if user_list else "Solo tu estas online.")

    def render_vulnerability_history(self, reports):
        st.subheader("Historial de vulnerabilidades del agente")
        combined_reports = reports.copy() if reports else []
        if st.session_state.get("scan_results"):
            combined_reports = combined_reports + st.session_state.scan_results

        if combined_reports:
            df = pd.DataFrame(combined_reports)
            display_columns = [
                col
                for col in ["dispositivo", "vulnerabilidad", "nivel", "fecha"]
                if col in df.columns
            ]
            st.dataframe(df[display_columns], use_container_width=True)
        else:
            st.info("Esperando reportes del agente movil...")

    def render_manual_scan(self, controller):
        st.subheader("Escaneo manual auxiliar")
        target = st.text_input(
            "Objetivo a escanear (URL, IP, etc.)",
            key="scan_target",
            placeholder="Ejemplo: https://ejemplo.com o 192.168.1.1",
        )
        if st.button("Escanear", key="scan_btn", use_container_width=True):
            if target:
                st.session_state.scan_results = controller.scan_vulnerabilities(target)
            else:
                st.info("Escaneando dispositivo local...")
                st.session_state.scan_results = controller.scan_vulnerabilities()
            st.rerun()
