# AnzenCore Architecture Blueprint

La arquitectura de AnzenCore está dividida en microservicios, pensada para aislar la lógica pesada de análisis del dashboard interactivo y lograr escalabilidad horizontal e integración continua *stateless*.

## Componentes del Stack

1. **Backend / API REST (FastAPI - Python 3.12)**
   - Puerto por defecto: 8000
   - Ejecuta análisis asíncronos y expone endpoints estáticos y proxies para consumidores externos.
   - Componentes clave: `routes/`, `services/` (donde vive `ApkAnalyzer` y `FolderAnalyzer`), `schemas/`.
   - Autenticación: Capa stateless o JWT.

2. **Frontend / Dashboard (Streamlit - Python 3.12)**
   - Puerto por defecto: 8501
   - Actúa como la UI interactiva para los usuarios (desarrolladores/auditores).
   - Patrón **MVC (Model-View-Controller)** dentro de Streamlit:
     - `models/`: Interactúa con la base de datos Supabase.
     - `controllers/`: Reglas de negocio del dashboard, llamadas al Backend API y manejo de sesiones.
     - `views/`: Dibuja los componentes y widgets en Streamlit.

3. **Base de Datos (Supabase / PostgreSQL)**
   - Almacena el registro de usuarios, historial de reportes (JSONs procesados de análisis), escaneos históricos.
   - Variables de entorno críticas: `SUPABASE_URL`, `SUPABASE_KEY`.

4. **Despliegue y Orquestación (Docker + Azure Container Apps)**
   - Cada servicio (API y Dashboard) tiene su propio `Dockerfile` (`Dockerfile.api`, `Dockerfile.dashboard`).
   - Escalamiento: El Dashboard y la API escalan automáticamente basados en tráfico HTTP (Custom Scale Rules en Terraform).

## Diagrama de Interacción
1. Usuario interactúa con Streamlit (`app.py` / `DashboardView`).
2. Streamlit invoca métodos en `DashboardController`.
3. El Controller consulta `SupabaseModel` (para reportes históricos) o hace peticiones HTTP REST a `FastAPI` (para procesar nuevos APKs).
4. `FastAPI` utiliza los analizadores (`ApkAnalyzer`), procesa y retorna el JSON al Dashboard.
5. El Dashboard almacena el resultado exitoso en Supabase.
