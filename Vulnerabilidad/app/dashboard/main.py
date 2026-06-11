import streamlit as st
from streamlit_autorefresh import st_autorefresh

from app.dashboard.config.settings import DashboardSettings
from app.dashboard.controllers.dashboard_controller import DashboardController
from app.dashboard.models.supabase_model import SupabaseModel
from app.dashboard.views.dashboard_view import DashboardView


st.set_page_config(
    page_title=DashboardSettings.page_title,
    page_icon=DashboardSettings.page_icon,
    layout=DashboardSettings.layout,
)


def bootstrap():
    if "model" not in st.session_state:
        st.session_state.model = SupabaseModel()
        st.session_state.controller = DashboardController(st.session_state.model)
        st.session_state.view = DashboardView()


def main():
    bootstrap()
    controller = st.session_state.controller
    view = st.session_state.view

    if "user" not in st.session_state:
        username, password, login_button, new_username, new_password, signup_button = (
            view.render_login()
        )
        if login_button:
            user = controller.login(username, password)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Credenciales incorrectas.")

        if signup_button:
            ok, message = controller.signup(new_username, new_password)
            if ok:
                st.success(message)
            else:
                st.error(message)
        return

    st_autorefresh(
        interval=DashboardSettings.refresh_interval_ms,
        key="refresh_dashboard",
    )
    controller.update_user_ping(st.session_state.user["id"])

    online_users = controller.fetch_online_list()
    reports = controller.fetch_all_reports()
    apk_scans = controller.fetch_apk_scans()

    if view.render_sidebar(st.session_state.user):
        del st.session_state.user
        st.rerun()

    view.render_dashboard(
        st.session_state.user,
        online_users,
        reports,
        apk_scans,
        controller,
    )


if __name__ == "__main__":
    main()
