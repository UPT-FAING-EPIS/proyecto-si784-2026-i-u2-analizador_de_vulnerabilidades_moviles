# Frontend Dashboard (Streamlit Blueprint)

El frontend de un analizador móvil de AnzenCore no es un script plano de Streamlit. Usa una arquitectura MVC montada en el `session_state`.

## Inicialización (Bootstrap)
Al arrancar, inyecta las dependencias en la sesión y carga el CSS personalizado:

```python
import streamlit as st

def bootstrap():
    if "model" not in st.session_state:
        st.session_state.model = SupabaseModel()
        st.session_state.controller = DashboardController(st.session_state.model)
        st.session_state.view = DashboardView()
    if "nav_section" not in st.session_state:
        st.session_state.nav_section = "inicio"
```

## Pinging y Actualizaciones Parciales (@st.fragment)
Para evitar que toda la pantalla de Streamlit parpadee cuando necesitas actualizar el estado de los usuarios conectados o barras de progreso en vivo, AnzenCore usa fragmentos.

```python
@st.fragment(run_every=5)
def _ping_fragment(controller):
    if "user" not in st.session_state:
        return
    user_id = st.session_state.user["id"]
    controller.update_user_ping(user_id)
    st.session_state.online_users = controller.fetch_online_list()
```

## Control de Vistas y Layout
La clase `DashboardView` maneja el UI. El renderizado condicional se hace verificando si el usuario existe en sesión:

```python
def main():
    bootstrap()
    # 1. Login if not authenticated
    if "user" not in st.session_state:
        view.render_login(controller)
        return
        
    # 2. Render Sidebar
    view.render_sidebar(st.session_state.user)
    
    # 3. Main Dashboard Rendering
    view.render_dashboard(...)
    
    # 4. Background tasks
    _ping_fragment(controller)
```

## Prácticas Recomendadas para Mostrar Vulnerabilidades
1. Agrupar por Severidad (Crítico en rojo, Alto en naranja, etc.).
2. Mostrar los bloques de código detectados en bloques markdown (`st.code`).
3. Proporcionar recomendaciones de OWASP Mobile o CWE.
