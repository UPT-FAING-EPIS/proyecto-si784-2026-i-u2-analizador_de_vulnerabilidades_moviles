import os

import pandas as pd
import streamlit as st


class AnzenView:
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
            u = st.text_input("Usuario", key="l_u")
            p = st.text_input("Contrasena", type="password", key="l_p")
            btn = st.button("Iniciar sesion")
        with tab2:
            ru = st.text_input("Nuevo usuario", key="r_u")
            rp = st.text_input("Nueva contrasena", type="password", key="r_p")
            rbtn = st.button("Crear cuenta")
        return u, p, btn, ru, rp, rbtn

    def render_dashboard(self, user, online_users, reports):
        st.title("AnzenCore Live Dashboard")

        c1, c2, c3 = st.columns([1, 1, 1.5])
        c1.metric("Online", len(online_users))
        c2.info(f"Sesion: {user['username']}")

        with c3:
            st.write("**Agente movil**")
            apk_path = "assets/AnzenCore_Agent.apk"
            if os.path.exists(apk_path) and os.path.getsize(apk_path) > 0:
                self.render_apk_download(apk_path, "AnzenCore.apk")
            else:
                st.error("APK no disponible en /assets")

        st.subheader("Monitor en tiempo real")
        user_list = [f"`{u['username']}`" for u in online_users]
        st.write(" ".join(user_list) if user_list else "Solo tu estas online.")

        st.divider()
        st.subheader("Historial de vulnerabilidades")
        combined_reports = reports.copy() if reports else []
        if st.session_state.get("scan_results"):
            combined_reports = combined_reports + st.session_state.scan_results

        col_hist, col_btn = st.columns([3, 1])
        with col_hist:
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
        with col_btn:
            st.write("")
            target = st.text_input(
                "Objetivo a escanear (URL, IP, etc.)",
                key="scan_target",
                placeholder="Ejemplo: https://ejemplo.com o 192.168.1.1",
            )
            if st.button("Escanear", key="scan_btn", use_container_width=True):
                if target:
                    st.session_state.scan_results = (
                        st.session_state.controller.scan_vulnerabilities(target)
                    )
                else:
                    st.info("Escaneando dispositivo local...")
                    st.session_state.scan_results = (
                        st.session_state.controller.scan_vulnerabilities()
                    )
                st.rerun()
