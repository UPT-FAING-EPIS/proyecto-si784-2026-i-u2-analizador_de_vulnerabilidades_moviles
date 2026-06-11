import os

import streamlit as st


class DashboardSettings:
    page_title = "AnzenCore"
    page_icon = "shield"
    layout = "wide"
    apk_path = "assets/AnzenCore_Agent.apk"
    apk_filename = "AnzenCore.apk"
    refresh_interval_ms = 5000


def get_supabase_settings():
    return {
        "url": st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", "")),
        "key": st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", "")),
    }
