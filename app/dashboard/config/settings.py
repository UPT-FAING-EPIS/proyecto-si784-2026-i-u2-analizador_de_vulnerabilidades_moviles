import os

import streamlit as st


class DashboardSettings:
    page_title = "AnzenCore"
    page_icon = "shield"
    layout = "wide"
    apk_path = "assets/AnzenCore_Agent.apk"
    apk_filename = "AnzenCore.apk"
    # Intervalo de ping/online-users en segundos (st.fragment run_every)
    # No causa parpadeo de página completa — solo refresca el bloque del monitor.
    ping_interval_s = 30
    # URL del servicio externo de analisis de calidad (anestatico)
    anzen_external_url = os.getenv(
        "ANZEN_EXTERNAL_URL", "https://anestatico.onrender.com/api/analysis/external/github"
    )


def get_supabase_settings():
    return {
        "url": st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", "")),
        "key": st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", "")),
    }
