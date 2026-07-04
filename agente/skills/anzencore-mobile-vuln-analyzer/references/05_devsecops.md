# DevSecOps e Infraestructura (AnzenCore Blueprint)

La seguridad y confiabilidad del analizador dependen de su infraestructura. AnzenCore utiliza Azure Container Apps mediante Terraform y un pipeline riguroso de CI/CD.

## 1. Contenedores (Docker)
Los servicios se empaquetan por separado:
- **API (`Dockerfile.api`)**: Ejecuta `uvicorn` (FastAPI).
- **Dashboard (`Dockerfile.dashboard`)**: Ejecuta `streamlit`.
- **Variables de Entorno Cruciales**: `SUPABASE_URL`, `SUPABASE_KEY` (inyectadas al contenedor en runtime).

## 2. Infraestructura como Código (Terraform)
La infraestructura base, descrita en `infra/main.tf`, despliega en Azure:
- **Azure Container Registry (ACR)**: Almacena las imágenes Docker de la API y el Dashboard.
- **Log Analytics Workspace**: Centraliza los logs de los contenedores.
- **Azure Container Apps Environment**: Orquestador serverless donde viven los contenedores.
- **Container Apps**:
  - `anzencore-api`: Expone puerto 8000. Escala basado en peticiones HTTP concurrentes.
  - `anzencore-dashboard`: Expone puerto 8501. Configurado con un tráfico del 100% apuntando a la última revisión. Conoce a la API usando la FQDN interna/externa de la Container App de la API.

### Secreto de Infraestructura
En Terraform, los secrets de Supabase y Registry se manejan nativamente dentro del bloque `secret {}` del `azurerm_container_app`, evitando exponerlos en texto plano en las variables de entorno de la app directamente.

## 3. CI/CD & DevSecOps (Conceptos)
Cualquier clon del analizador debe implementar:
- **Pytest con Mutmut**: Para asegurar que las reglas del `ApkAnalyzer` realmente atrapan vulnerabilidades y los tests no sean frágiles.
- **SonarQube / Snyk**: El código de la herramienta de seguridad debe ser seguro en sí mismo (ej. escaneo del código Python por GitHub Actions).
