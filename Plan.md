# Plan de Reestructuracion AnzenCore

## Objetivo

Reestructurar AnzenCore para pasar de un prototipo funcional a un proyecto publicable con practicas DevSecOps: infraestructura como codigo, analisis de seguridad, pruebas automatizadas, versionamiento y despliegue continuo.

## Prompt Maestro Para Reestructuracion

Usa el siguiente prompt para guiar la reestructuracion del proyecto segun la rubrica. Este prompt deja fuera, por ahora, la elaboracion final de los documentos FD01, FD02, FD03 y FD04, porque esos informes se prepararan al cierre del proyecto cuando la arquitectura, workflows, pruebas, despliegue y evidencias ya esten implementados.

```text
Actua como arquitecto de software, DevSecOps engineer y desarrollador senior.

Necesito reestructurar el proyecto "AnzenCore", un Analizador de Vulnerabilidades Moviles.

Contexto del proyecto:
- Nombre: AnzenCore.
- Tipo: Analizador de vulnerabilidades moviles.
- Funcionalidad principal: analizar APKs subidos mediante ingenieria inversa.
- Arquitectura de software objetivo: MVC.
- Dashboard actual: Streamlit.
- Agente movil: APK/Kivy.
- Base de datos: PostgreSQL administrado por Supabase.
- Despliegue oficial objetivo: Azure Container Apps administrado con Terraform.
- Repositorio: GitHub.

Objetivo general:
Reestructurar el proyecto para cumplir una rubrica academica/profesional enfocada en DevSecOps, calidad, documentacion, despliegue, versionamiento, seguridad e infraestructura como codigo.

Alcance actual:
No generar aun los informes FD01, FD02, FD03 y FD04. Solo preparar el proyecto, la estructura, los workflows, la arquitectura, los artefactos tecnicos y las bases para que esos documentos puedan elaborarse al final con evidencia real.

Rubrica que debe guiar la reestructuracion:
1. README actualizado con requisitos, procedimientos, parametros y pasos de despliegue.
2. GitHub Wikis con caracteristicas del producto, futuras versiones, roadmap, fechas de liberacion y funcionalidades principales.
3. GitHub Projects con tareas relacionadas a ramas.
4. GitHub Actions para desarrollo seguro:
   - SonarQube o SonarCloud.
   - Semgrep.
   - Snyk.
   - Analisis de vulnerabilidades, bugs, dependencias e infraestructura.
5. Releases y Packages en GitHub.
6. Evidencia de contribucion al proyecto.
7. Publicacion del sistema para consumo en nube o marketplace, distinto de GitHub.
8. Preparacion para exposicion:
   - Presentacion Marp.
   - Video publicado en YouTube.
   - Claridad de enfoque.
   - Capacidad de absolver preguntas.

Requisitos tecnicos obligatorios:
- Mantener la base de datos PostgreSQL en Supabase.
- Mantener arquitectura MVC en la aplicacion.
- Priorizar como flujo principal el analisis de APK subido por el usuario.
- Separar responsabilidades entre dashboard, agente movil, backend/API, infraestructura, pruebas y documentacion.
- Evitar que el APK escriba directamente en Supabase si se implementa API backend.
- Implementar pruebas:
  - Unitarias.
  - Integracion.
  - Mutantes.
  - Interfaz.
  - BDD con escenarios en Gherkin.
- Implementar workflows de GitHub para:
  - Analisis estatico.
  - Seguridad.
  - Pruebas.
  - Versionamiento.
  - Releases.
  - Despliegue.
- Implementar Terraform para infraestructura y analisis economico posterior.
- Preparar la base para diagramas por reverse engineering al final:
  - Clases.
  - Base de datos.
  - Componentes.
  - Despliegue.
  - Arquitectura.
  - Infraestructura.

Estructura objetivo sugerida:
AnzenCore/
  app/
    dashboard/
      app.py
      src/
        models/
        views/
        controllers/
        services/
        config/
    api/
      main.py
      routes/
      controllers/
      services/
      models/
      schemas/
      config/
  mobile/
    agent/
      main.py
      buildozer.spec
      requirements.txt
  assets/
    AnzenCore_Agent.apk
  infra/
    terraform/
      environments/
        dev/
        prod/
      modules/
  tests/
    unit/
    integration/
    bdd/
    interface/
    mutation/
  docs/
    wiki/
    roadmap/
    diagrams/
    marp/
  .github/
    workflows/
      ci.yml
      security.yml
      deploy.yml
      release.yml
  README.md
  Plan.md

Entregables esperados en esta reestructuracion:
1. Estructura de carpetas limpia y escalable.
2. Codigo organizado bajo MVC.
3. Dashboard funcionando.
4. Agente movil organizado.
5. API backend preparada o implementada para recibir reportes del movil.
6. Conexion segura con Supabase/PostgreSQL.
7. Scripts o migraciones SQL para tablas principales.
8. README con:
   - Descripcion del proyecto.
   - Requisitos.
   - Variables de entorno/secrets.
   - Instalacion local.
   - Ejecucion local.
   - Pruebas.
   - Build del APK.
   - Despliegue.
9. Workflows de GitHub Actions:
   - ci.yml para pruebas.
   - security.yml para Sonar, Semgrep y Snyk.
   - deploy.yml para despliegue.
   - release.yml para versionamiento y releases.
10. Configuracion base de Terraform.
11. Base para GitHub Wiki:
   - Caracteristicas del producto.
   - Roadmap.
   - Futuras versiones.
   - Fechas estimadas.
12. Base para GitHub Projects:
   - Issues en formato "Como... Quiero... Para...".
   - Criterios de aceptacion.
   - Ramas asociadas.
13. Base para pruebas BDD:
   - Features en Gherkin con "Dado... Cuando... Entonces...".
14. Preparacion para generar diagramas al final mediante reverse engineering.

Restricciones:
- No eliminar funcionalidades existentes sin reemplazo.
- No usar Streamlit Cloud como despliegue oficial.
- Mantener Streamlit solo como framework del dashboard.
- El despliegue final debe hacerse con Terraform.
- No exponer claves de Supabase en el repositorio.
- No dejar secretos dentro del APK si se puede usar una API backend.
- Mantener compatibilidad con pruebas locales antes del despliegue.
- Documentar cualquier decision tecnica importante.

Orden de trabajo recomendado:
1. Analizar estructura actual.
2. Crear estructura objetivo.
3. Mover dashboard a MVC.
4. Separar agente movil.
5. Crear o preparar API backend.
6. Definir esquema Supabase/PostgreSQL.
7. Agregar pruebas base.
8. Agregar workflows CI.
9. Agregar herramientas de seguridad.
10. Agregar Terraform.
11. Agregar README y docs base.
12. Preparar releases y packages.
13. Verificar despliegue publico en Azure Container Apps.
14. Preparar evidencias para FD01-FD04 al final.

Resultado esperado:
Un proyecto AnzenCore reestructurado, mantenible, publicable y alineado a la rubrica, preparado para completar posteriormente los informes FD01, FD02, FD03 y FD04 en formato Markdown y PDF con evidencias reales del repositorio, infraestructura, pruebas, despliegue, issues, roadmap, diagramas y analisis economico.
```

## Diagnostico Actual

El proyecto actual funciona como demo, pero mezcla responsabilidades:

```text
app.py / src       -> dashboard Streamlit
agent/            -> agente movil Kivy/APK
assets/           -> APK compilado descargable
Supabase directo  -> base de datos y API REST
```

Riesgos principales:

- El APK envia datos directamente a Supabase.
- La clave publica de Supabase queda embebida en el APK.
- No hay una API intermedia para validar reportes.
- No hay estructura formal de pruebas.
- No hay workflows de CI/CD.
- Terraform no esta integrado.
- No hay separacion clara entre dashboard, backend, mobile, infraestructura y tests.

## Decision de Producto

La funcionalidad principal de AnzenCore sera:

```text
Analizar APKs subidos por el usuario mediante ingenieria inversa para identificar vulnerabilidades moviles.
```

El flujo principal del sistema sera:

```text
Usuario autenticado
  -> sube archivo APK
  -> sistema valida el archivo
  -> motor de analisis aplica ingenieria inversa
  -> sistema detecta vulnerabilidades
  -> sistema guarda resultados
  -> dashboard muestra hallazgos
  -> usuario exporta reporte
```

El agente movil queda como componente complementario o evolucion futura:

```text
Agente movil opcional
  -> diagnostico basico del dispositivo
  -> envio de reportes a API
```

No sera el flujo principal de evaluacion del producto.

## Requerimientos Funcionales

Los siguientes requerimientos funcionales se derivan del analisis del codigo actual del dashboard Streamlit, la capa MVC existente, Supabase y el agente movil Kivy/APK.

### RF-01: Registro de usuarios

El sistema debe permitir que un usuario cree una cuenta desde el dashboard ingresando usuario y contrasena.

Detalle:

- El sistema debe validar que usuario y contrasena no esten vacios.
- El sistema debe verificar si el usuario ya existe.
- El sistema debe registrar el usuario en la tabla `usuarios`.
- El sistema debe mostrar un mensaje de exito o error.

Estado actual:

```text
Implementado parcialmente.
```

Mejoras requeridas:

- Hashear contrasenas.
- Validar formato y longitud.
- Evitar mensajes ambiguos ante errores de base de datos.

### RF-02: Inicio de sesion

El sistema debe permitir que un usuario registrado inicie sesion desde el dashboard.

Detalle:

- El usuario ingresa usuario y contrasena.
- El sistema valida credenciales contra Supabase.
- Si las credenciales son correctas, se crea una sesion en Streamlit.
- Si son incorrectas, se muestra un mensaje de error.

Estado actual:

```text
Implementado.
```

Mejoras requeridas:

- Usar autenticacion segura.
- Evitar contrasenas en texto plano.

### RF-03: Cierre de sesion

El sistema debe permitir cerrar la sesion activa desde el dashboard.

Detalle:

- El usuario autenticado debe ver un boton para cerrar sesion.
- Al cerrar sesion, el sistema debe limpiar la sesion local.
- El sistema debe regresar a la pantalla de login.

Estado actual:

```text
Implementado.
```

### RF-04: Visualizacion de usuario autenticado

El sistema debe mostrar los datos basicos del usuario autenticado en el dashboard.

Detalle:

- Mostrar nombre de usuario.
- Mostrar ID de usuario.
- El ID debe servir para asociar reportes enviados por el agente movil.

Estado actual:

```text
Implementado.
```

### RF-05: Actualizacion de estado online

El sistema debe actualizar periodicamente el estado de actividad del usuario autenticado.

Detalle:

- El sistema debe actualizar `last_ping` del usuario.
- El dashboard debe refrescarse automaticamente.
- El sistema debe considerar online a usuarios con actividad reciente.

Estado actual:

```text
Implementado parcialmente.
```

Mejoras requeridas:

- Revisar uso de `now()` en Supabase.
- Usar timestamps consistentes.
- Definir claramente el umbral de usuario online.

### RF-06: Listado de usuarios online

El sistema debe mostrar usuarios conectados o recientemente activos.

Detalle:

- Consultar tabla `usuarios`.
- Filtrar usuarios con `last_ping` reciente.
- Mostrar nombres de usuarios online en el dashboard.

Estado actual:

```text
Implementado.
```

### RF-07: Descarga del agente movil APK

El sistema debe permitir descargar el APK del agente movil desde el dashboard.

Detalle:

- El dashboard debe verificar que el archivo APK exista.
- El dashboard debe verificar que el APK no este vacio.
- El usuario debe poder descargar el APK desde la interfaz.

Estado actual:

```text
Implementado.
```

### RF-08: Escaneo manual desde dashboard

El sistema debe permitir ejecutar un escaneo manual desde el dashboard.

Detalle:

- El usuario puede ingresar un objetivo como URL o IP.
- Si se ingresa objetivo, el sistema genera resultados asociados a ese objetivo.
- Si no se ingresa objetivo, el sistema ejecuta un escaneo local/simulado.
- Los resultados se muestran en el dashboard.

Estado actual:

```text
Implementado como simulacion/local.
```

Mejoras requeridas:

- Diferenciar claramente escaneo real de simulacion.
- Persistir resultados si corresponde.
- Validar objetivo.

### RF-09: Visualizacion del historial de vulnerabilidades

El sistema debe mostrar el historial de vulnerabilidades registradas.

Detalle:

- Consultar la tabla `vulnerabilidades`.
- Mostrar columnas principales:
  - dispositivo
  - vulnerabilidad
  - nivel
  - fecha
- Ordenar resultados por fecha descendente.
- Mostrar mensaje cuando no existan reportes.

Estado actual:

```text
Implementado.
```

### RF-10: Registro de vulnerabilidades desde agente movil

El agente movil debe enviar vulnerabilidades detectadas al sistema.

Detalle:

- El usuario debe ingresar el ID de usuario del dashboard en el APK.
- El agente debe generar resultados del analisis movil.
- El agente debe enviar los datos a Supabase o, en la arquitectura objetivo, a la API backend.
- El sistema debe asociar el reporte con `user_id`.
- El dashboard debe mostrar los reportes enviados.

Estado actual:

```text
Implementado parcialmente.
```

Mejoras requeridas:

- Enviar a API backend en vez de Supabase directo.
- Validar `user_id`.
- Mostrar errores HTTP reales.
- Evitar claves de Supabase dentro del APK.

### RF-11: Validacion de errores del agente movil

El agente movil debe informar si el envio de reportes falla.

Detalle:

- Debe mostrar error de conexion.
- Debe mostrar error HTTP si Supabase/API rechaza el reporte.
- Debe confirmar cuantos reportes fueron enviados correctamente.

Estado actual:

```text
Implementado en codigo fuente, pendiente de recompilar APK.
```

### RF-12: Almacenamiento de reportes en Supabase/PostgreSQL

El sistema debe persistir los reportes de vulnerabilidades en la base de datos.

Detalle:

- Usar tabla `vulnerabilidades`.
- Cada reporte debe tener:
  - user_id
  - dispositivo
  - vulnerabilidad
  - nivel
  - descripcion
  - fecha

Estado actual:

```text
Implementado en Supabase.
```

### RF-13: Clasificacion de vulnerabilidades por nivel

El sistema debe clasificar las vulnerabilidades segun nivel de severidad.

Detalle:

- Niveles actuales:
  - Critico
  - Alto
  - Medio
  - Bajo
- El dashboard debe mostrar el nivel de cada vulnerabilidad.

Estado actual:

```text
Implementado.
```

Mejoras requeridas:

- Normalizar valores de severidad.
- Evitar problemas de codificacion en textos con tildes.

### RF-14: Refresco automatico del dashboard

El dashboard debe actualizar periodicamente la informacion visible.

Detalle:

- Refrescar cada cierto intervalo.
- Actualizar usuarios online.
- Actualizar historial de vulnerabilidades.

Estado actual:

```text
Implementado con streamlit-autorefresh.
```

### RF-15: Publicacion del sistema para usuarios externos

El sistema debe estar disponible publicamente para que terceros puedan probarlo.

Detalle:

- El dashboard debe estar publicado en la nube.
- Los usuarios deben acceder por URL publica.
- La aplicacion publicada debe usar secrets configurados en el ambiente cloud.

Estado actual:

```text
Implementado temporalmente mediante Streamlit Cloud. Para la entrega final debe migrarse a Azure Container Apps con Terraform.
```

### RF-16: Gestion de APK publicado

El sistema debe entregar a los usuarios la version vigente del APK.

Detalle:

- El APK compilado debe estar en `assets`.
- El dashboard debe descargar la version actual.
- Las releases deben adjuntar el APK versionado.

Estado actual:

```text
Implementado parcialmente.
```

Mejoras requeridas:

- Automatizar build/release del APK.
- Registrar version de APK.

### RF-17: API backend para recepcion de reportes

El sistema debe exponer una API backend para recibir reportes desde el agente movil.

Detalle:

- Endpoint `POST /reports`.
- Validar payload.
- Validar usuario.
- Insertar en Supabase.
- Retornar respuesta clara al APK.

Estado actual:

```text
Pendiente.
```

Justificacion:

- Evita exponer Supabase directamente en el APK.
- Permite validar datos antes de persistirlos.
- Mejora seguridad y trazabilidad.

### RF-18: Consulta de salud del sistema

El sistema debe exponer un mecanismo para verificar disponibilidad.

Detalle:

- Endpoint sugerido: `GET /health`.
- Debe validar disponibilidad de API.
- Opcionalmente validar conexion con Supabase.

Estado actual:

```text
Pendiente.
```

### RF-19: Gestion de configuracion por ambiente

El sistema debe permitir configuraciones separadas para local, pruebas y produccion.

Detalle:

- Local: `.streamlit/secrets.toml`.
- Produccion: Azure Container Apps secrets o Azure Key Vault.
- CI/CD: GitHub Secrets.
- API: variables de entorno.

Estado actual:

```text
Implementado parcialmente.
```

### RF-20: Trazabilidad de reportes

El sistema debe permitir asociar cada vulnerabilidad con un usuario y un dispositivo.

Detalle:

- Cada reporte debe incluir `user_id`.
- Cada reporte debe incluir identificador o descripcion del dispositivo.
- El dashboard debe mostrar el origen del reporte.

Estado actual:

```text
Implementado parcialmente.
```

### RF-21: Integracion con sistemas externos

El sistema debe poder integrarse con otros sistemas mediante interfaces estandarizadas.

Detalle:

- Exponer una API documentada para consultar reportes de vulnerabilidades.
- Permitir registrar reportes desde clientes externos autorizados.
- Entregar respuestas en formato JSON.
- Documentar contratos de entrada y salida.
- Permitir autenticacion por token para integraciones.
- Preparar OpenAPI/Swagger si se implementa FastAPI.
- Permitir exportar reportes para consumo externo.

Estado actual:

```text
Pendiente.
```

Justificacion:

- Facilita integracion con plataformas SIEM, dashboards externos, sistemas academicos, herramientas DevSecOps o APIs empresariales.
- Evita que otros sistemas dependan directamente de la estructura interna de Supabase.
- Permite que AnzenCore sea consumido como servicio.

## Arquitectura Recomendada

```text
APK movil
  -> API backend
  -> Supabase/PostgreSQL

Dashboard Streamlit
  -> API backend o Supabase

GitHub Actions
  -> pruebas
  -> analisis estatico
  -> seguridad
  -> build
  -> despliegue

Terraform
  -> infraestructura cloud
```

## Integrabilidad del Sistema

AnzenCore debe disenarse como un sistema integrable con otras plataformas. La integracion no debe depender de acceso directo a la base de datos, sino de contratos estables mediante API.

### Principios

```text
- API first.
- Respuestas JSON.
- Contratos documentados.
- Autenticacion por token.
- Versionamiento de API.
- Bajo acoplamiento con Supabase.
- Documentacion OpenAPI/Swagger.
```

### API de Integracion Sugerida

```text
GET /health
GET /reports
GET /reports/{report_id}
GET /users/{user_id}/reports
POST /reports
GET /devices
GET /metrics/summary
```

### Casos de Integracion

```text
SIEM:
- Consumir reportes de vulnerabilidades.
- Correlacionar eventos de seguridad.

Dashboard externo:
- Consultar metricas y reportes.
- Mostrar tendencias.

Herramientas DevSecOps:
- Enviar resultados a pipelines.
- Cruzar hallazgos con releases.

Sistema academico:
- Consultar evidencias.
- Asociar reportes a usuarios o grupos.

Aplicaciones moviles:
- Enviar reportes al backend.
- Consultar estado de envio.
```

### Requisitos Tecnicos Para Integracion

```text
- FastAPI debe generar documentacion OpenAPI automaticamente.
- Cada endpoint debe tener request/response schema.
- La API debe manejar errores con codigos HTTP claros.
- La API debe versionarse, por ejemplo `/api/v1`.
- Los tokens de integracion deben guardarse como secrets.
- No se debe exponer SUPABASE_KEY a clientes externos.
```

### Ejemplo de Payload de Reporte

```json
{
  "user_id": "uuid-del-usuario",
  "device_id": "android-device-id",
  "dispositivo": "Android arm64-v8a",
  "vulnerabilidad": "USB Debugging",
  "nivel": "Medio",
  "descripcion": "Modo desarrollador activo"
}
```

### Resultado Esperado

```text
AnzenCore podra funcionar como dashboard y tambien como servicio integrable para que otros sistemas consulten o registren informacion de vulnerabilidades moviles de forma controlada.
```

### RF-22: Escaneo de APK mediante ingenieria inversa

El sistema debe permitir cargar un archivo APK y ejecutar un analisis de ingenieria inversa para identificar vulnerabilidades.

Este requerimiento es la funcionalidad principal del producto.

Detalle:

- El dashboard debe incluir un boton o seccion principal para escanear un APK.
- El usuario debe poder subir un archivo `.apk`.
- El sistema debe validar que el archivo tenga formato permitido.
- El sistema debe ejecutar un proceso de analisis estatico e ingenieria inversa.
- El sistema debe extraer metadatos del APK.
- El sistema debe identificar posibles vulnerabilidades.
- El sistema debe registrar el resultado del escaneo en la base de datos.
- El sistema debe mostrar los hallazgos en el dashboard.

Analisis sugeridos:

```text
- Permisos peligrosos solicitados por el APK.
- Uso de HTTP no cifrado.
- URLs o endpoints hardcodeados.
- Secrets, tokens o API keys embebidas.
- Certificados inseguros.
- Configuracion debug habilitada.
- Min SDK vulnerable.
- Componentes exportados.
- Activities, services o receivers expuestos.
- Uso de almacenamiento inseguro.
- Librerias o dependencias sospechosas.
```

Herramientas candidatas:

```text
apktool
jadx
MobSF
androguard
semgrep sobre codigo decompilado
```

Estado actual:

```text
Pendiente.
```

Prioridad:

```text
Critica.
```

Justificacion:

- Esta sera una funcionalidad principal del producto.
- Permite analizar APKs externos sin depender solo del agente instalado en el movil.
- Aporta valor directo como analizador de vulnerabilidades moviles.

### RF-23: Historial de escaneos de APK

El sistema debe mantener un historial de los APKs analizados y sus resultados.

Detalle:

- Registrar cada escaneo ejecutado.
- Asociar el escaneo con el usuario autenticado.
- Guardar nombre del archivo APK.
- Guardar fecha del escaneo.
- Guardar estado del escaneo:
  - pendiente
  - procesando
  - completado
  - fallido
- Guardar cantidad de vulnerabilidades encontradas.
- Permitir consultar escaneos anteriores.
- Permitir abrir el detalle de cada escaneo.

Tabla sugerida:

```text
apk_scans
```

Campos sugeridos:

```text
id
user_id
file_name
file_hash
package_name
app_name
version_name
version_code
status
created_at
finished_at
summary
```

Estado actual:

```text
Pendiente.
```

### RF-24: Detalle de hallazgos por APK analizado

El sistema debe almacenar y mostrar los hallazgos encontrados durante el analisis de un APK.

Detalle:

- Cada hallazgo debe pertenecer a un escaneo.
- Cada hallazgo debe tener severidad.
- Cada hallazgo debe tener descripcion.
- Cada hallazgo debe indicar evidencia tecnica si existe.
- Cada hallazgo debe sugerir una recomendacion.

Tabla sugerida:

```text
apk_findings
```

Campos sugeridos:

```text
id
scan_id
tipo
titulo
severidad
descripcion
evidencia
recomendacion
created_at
```

Estado actual:

```text
Pendiente.
```

### RF-25: Exportacion de reportes

El sistema debe permitir exportar reportes de analisis para uso externo o evidencia academica/profesional.

Detalle:

- Exportar reporte por escaneo.
- Exportar historial de escaneos.
- Exportar hallazgos por severidad.
- Permitir formato PDF.
- Permitir formato CSV o Excel.
- Opcionalmente permitir formato JSON para integraciones.

Contenido minimo del reporte:

```text
- Nombre del APK.
- Hash del APK.
- Fecha de analisis.
- Usuario que ejecuto el analisis.
- Resumen de vulnerabilidades.
- Hallazgos detallados.
- Severidad.
- Evidencia.
- Recomendaciones.
```

Estado actual:

```text
Pendiente.
```

### RF-26: Escaneo principal desde dashboard

El dashboard debe presentar como flujo principal el escaneo de APK por ingenieria inversa.

Detalle:

- La pantalla principal debe priorizar la opcion "Escanear APK".
- El usuario debe poder iniciar el analisis desde un boton visible.
- El historial de escaneos debe estar disponible desde el dashboard.
- La exportacion de reportes debe estar disponible desde el resultado o historial.

Estado actual:

```text
Pendiente.
```

## Estructura Propuesta

```text
AnzenCore/
  app/
    dashboard/
      app.py
      src/
        controllers.py
        models.py
        views.py
    api/
      main.py
      routes/
      services/
      schemas/
      settings.py
  mobile/
    agent/
      main.py
      buildozer.spec
      requirements.txt
  assets/
    AnzenCore_Agent.apk
  infra/
    terraform/
      environments/
        dev/
        prod/
      modules/
  tests/
    unit/
    integration/
    bdd/
    interface/
    mutation/
  .github/
    workflows/
      ci.yml
      security.yml
      deploy.yml
  docs/
  requirements.txt
  README.md
  Plan.md
```

## Componentes

## Guia de Configuracion Paso a Paso

Durante la implementacion se debe documentar cada configuracion necesaria. No se deben dejar pasos implicitos ni claves dentro del codigo.

### 1. Supabase

Objetivo:

- Configurar PostgreSQL, tablas, API keys y acceso seguro.

Pasos:

```text
1. Entrar a Supabase.
2. Crear o abrir el proyecto AnzenCore.
3. Copiar Project URL.
4. Copiar anon/public key.
5. Crear/verificar tabla `usuarios`.
6. Crear/verificar tabla `vulnerabilidades`.
7. Configurar politicas RLS si aplica.
8. Probar lectura desde dashboard.
9. Probar insercion de vulnerabilidad.
```

Secrets requeridos:

```text
SUPABASE_URL
SUPABASE_KEY
```

Donde configurarlos:

```text
Local:
.streamlit/secrets.toml

Produccion:
Azure Container Apps secrets o Azure Key Vault

GitHub Actions:
Repository Settings -> Secrets and variables -> Actions
```

Formato local:

```toml
SUPABASE_URL = "https://tu-proyecto.supabase.co"
SUPABASE_KEY = "tu_anon_key"
```

### 2. Azure Container Apps con Terraform

Objetivo:

- Publicar el dashboard Streamlit y la API FastAPI en Azure usando Terraform como unico mecanismo oficial de despliegue.

Pasos:

```text
1. Subir el proyecto a GitHub.
2. Crear cuenta/suscripcion de Azure.
3. Crear credenciales de despliegue para GitHub Actions.
4. Guardar credenciales Azure en GitHub Secrets.
5. Crear Dockerfile para dashboard Streamlit.
6. Crear Dockerfile para API FastAPI.
7. Crear Terraform para Resource Group, Azure Container Registry, Log Analytics, Container Apps Environment y Container Apps.
8. Ejecutar terraform plan desde GitHub Actions.
9. Ejecutar terraform apply desde rama main.
10. Publicar dashboard y API en Azure Container Apps.
11. Probar login, dashboard, API y descarga del APK desde la URL publica de Azure.
```

Secrets requeridos:

```text
SUPABASE_URL
SUPABASE_KEY
AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
```

Evidencia:

```text
- URL publica de Azure Container Apps.
- Captura del dashboard.
- Captura de Terraform plan/apply.
- Captura de Azure Container Apps.
- Captura de configuracion de secrets sin mostrar valores.
```

### 3. GitHub Secrets

Objetivo:

- Centralizar claves necesarias para CI/CD, seguridad y despliegue.

Pasos:

```text
1. Ir al repositorio en GitHub.
2. Entrar a Settings.
3. Entrar a Secrets and variables.
4. Entrar a Actions.
5. Crear cada secret requerido.
6. Verificar que los workflows los usen con secrets.NOMBRE.
```

Secrets minimos:

```text
SUPABASE_URL
SUPABASE_KEY
SONAR_TOKEN
SNYK_TOKEN
SEMGREP_APP_TOKEN
```

Secrets opcionales para despliegue:

```text
CLOUD_PROVIDER_TOKEN
AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
```

Regla:

```text
Nunca imprimir secrets en logs.
Nunca guardar secrets en el repositorio.
Nunca poner secrets en el APK si se puede usar API backend.
```

### 4. SonarQube / SonarCloud

Objetivo:

- Analizar bugs, vulnerabilidades, code smells, duplicacion y cobertura.

Pasos:

```text
1. Crear cuenta en SonarCloud o usar servidor SonarQube.
2. Vincular el repositorio de GitHub.
3. Crear proyecto AnzenCore.
4. Generar SONAR_TOKEN.
5. Guardar SONAR_TOKEN en GitHub Secrets.
6. Agregar archivo sonar-project.properties si aplica.
7. Configurar workflow security.yml.
8. Ejecutar analisis.
9. Verificar Quality Gate.
```

Archivo sugerido:

```text
sonar-project.properties
```

Contenido base:

```properties
sonar.projectKey=anzencore
sonar.projectName=AnzenCore
sonar.sources=.
sonar.tests=tests
sonar.python.coverage.reportPaths=coverage.xml
sonar.exclusions=**/__pycache__/**,**/.venv/**,**/.buildozer/**,assets/**
```

### 5. Semgrep

Objetivo:

- Detectar patrones inseguros en codigo, YAML, workflows y Terraform.

Pasos:

```text
1. Crear cuenta en Semgrep.
2. Vincular repositorio GitHub.
3. Generar SEMGREP_APP_TOKEN si se usara Semgrep App.
4. Guardar SEMGREP_APP_TOKEN en GitHub Secrets.
5. Crear workflow security.yml.
6. Ejecutar semgrep en pull requests.
7. Revisar findings.
```

Configuracion recomendada:

```text
Ruleset:
- p/default
- p/security-audit
- p/python
- p/owasp-top-ten
```

### 6. Snyk

Objetivo:

- Detectar vulnerabilidades en dependencias e infraestructura como codigo.

Pasos:

```text
1. Crear cuenta en Snyk.
2. Vincular repositorio GitHub.
3. Generar SNYK_TOKEN.
4. Guardar SNYK_TOKEN en GitHub Secrets.
5. Configurar workflow security.yml.
6. Ejecutar `snyk test`.
7. Ejecutar `snyk iac test infra/terraform`.
8. Revisar vulnerabilidades.
```

Analisis requeridos:

```text
Dependencias Python:
snyk test

Infraestructura Terraform:
snyk iac test infra/terraform
```

### 7. Terraform

Objetivo:

- Definir infraestructura como codigo y preparar analisis economico.

Pasos:

```text
1. Elegir proveedor cloud.
2. Crear credenciales del proveedor.
3. Guardar credenciales en GitHub Secrets.
4. Crear estructura infra/terraform.
5. Crear ambientes dev y prod.
6. Ejecutar terraform fmt.
7. Ejecutar terraform init.
8. Ejecutar terraform validate.
9. Ejecutar terraform plan.
10. Configurar workflow terraform.yml.
11. Agregar Snyk IaC o herramienta equivalente.
12. Preparar Infracost o tabla de costos para FD01.
```

Secrets segun Azure:

```text
AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
```

Comandos base:

```bash
terraform fmt -recursive
terraform init
terraform validate
terraform plan
```

### 8. API Backend

Objetivo:

- Recibir reportes del APK sin exponer Supabase directamente.

Pasos:

```text
1. Crear proyecto FastAPI.
2. Crear endpoint GET /health.
3. Crear endpoint POST /reports.
4. Validar campos requeridos.
5. Validar user_id.
6. Insertar reporte en Supabase.
7. Probar con curl/Postman.
8. Actualizar APK para enviar a la API.
9. Desplegar API.
10. Guardar API_URL como secret/config.
```

Secrets/config requeridos:

```text
SUPABASE_URL
SUPABASE_KEY
API_URL
API_TOKEN opcional
```

### 9. APK Movil

Objetivo:

- Compilar y publicar una version del agente que envie reportes correctamente.

Pasos:

```text
1. Actualizar mobile/agent/main.py.
2. Configurar URL de API o endpoint.
3. Evitar escribir directo en Supabase si ya existe API.
4. Compilar con Buildozer en WSL/Linux.
5. Copiar APK a assets/AnzenCore_Agent.apk.
6. Probar instalacion en movil.
7. Probar envio de vulnerabilidades.
8. Publicar APK en GitHub Release.
9. Verificar descarga desde dashboard.
```

Comandos base:

```bash
cd mobile/agent
python -m buildozer android debug
cp bin/*.apk ../../assets/AnzenCore_Agent.apk
```

### 10. GitHub Releases y Packages

Objetivo:

- Publicar versiones formales del sistema.

Pasos:

```text
1. Definir version semantica.
2. Crear tag.
3. Ejecutar workflow release.yml.
4. Publicar changelog.
5. Adjuntar APK.
6. Adjuntar evidencias si aplica.
```

Formato:

```text
v1.0.0
v1.1.0
v1.1.1
```

### 11. GitHub Wiki y Roadmap

Objetivo:

- Documentar producto y futuras versiones.

Pasos:

```text
1. Activar Wiki en GitHub.
2. Crear pagina Home.
3. Crear pagina Caracteristicas.
4. Crear pagina Instalacion.
5. Crear pagina Arquitectura.
6. Crear pagina Roadmap.
7. Crear pagina Futuras versiones.
8. Definir fechas tentativas de liberacion.
```

Contenido minimo:

```text
- Descripcion del producto.
- Caracteristicas actuales.
- Caracteristicas futuras.
- Roadmap.
- Fechas de releases.
- Guia de despliegue.
```

### Dashboard

Tecnologia sugerida:

```text
Streamlit
```

Responsabilidades:

- Login de usuarios.
- Visualizacion del dashboard.
- Historial de vulnerabilidades.
- Descarga del APK.
- Consulta de datos desde API o Supabase.

### API Backend

Tecnologia sugerida:

```text
FastAPI
```

Responsabilidades:

- Recibir reportes del APK movil.
- Validar `user_id`.
- Validar payloads.
- Registrar vulnerabilidades.
- Centralizar reglas de negocio.
- Evitar que el APK escriba directo en Supabase.
- Recibir archivos APK para analisis si el procesamiento se delega al backend.
- Orquestar el analisis de ingenieria inversa.

Endpoints sugeridos:

```text
POST /reports
GET /reports
GET /users/{user_id}/reports
POST /auth/login
POST /auth/signup
POST /apk-scans
GET /apk-scans
GET /apk-scans/{scan_id}
GET /apk-scans/{scan_id}/findings
GET /apk-scans/{scan_id}/export
GET /health
```

### Motor de Analisis de APK

Tecnologia sugerida:

```text
Python + herramientas de reverse engineering
```

Responsabilidades:

- Recibir un APK.
- Calcular hash del archivo.
- Extraer AndroidManifest.
- Extraer metadatos del paquete.
- Decompilar o inspeccionar recursos.
- Ejecutar reglas de deteccion.
- Generar hallazgos.
- Guardar resultados en Supabase/PostgreSQL.
- Entregar reporte al dashboard.

Herramientas candidatas:

```text
apktool
jadx
androguard
MobSF
semgrep sobre codigo decompilado
```

Flujo sugerido:

```text
Usuario sube APK
  -> Dashboard/API recibe archivo
  -> Motor calcula hash y extrae metadatos
  -> Motor aplica reglas de analisis
  -> Guarda escaneo en `apk_scans`
  -> Guarda hallazgos en `apk_findings`
  -> Dashboard muestra resultado
  -> Usuario exporta reporte
```

### Agente Movil

Tecnologia actual:

```text
Kivy + Buildozer
```

Responsabilidades:

- Analizar el movil.
- Mostrar estado del escaneo.
- Enviar resultados a la API backend.
- Mostrar errores reales de conexion o validacion.

Flujo recomendado:

```text
Agente movil -> API backend -> Supabase/PostgreSQL
```

No recomendado:

```text
Agente movil -> Supabase directo
```

### Base de Datos

Opcion actual:

```text
Supabase PostgreSQL
```

Tablas minimas:

```sql
usuarios
vulnerabilidades
```

Tabla `usuarios`:

```text
id
username
password
last_ping
created_at
```

Tabla `vulnerabilidades`:

```text
id
user_id
dispositivo
vulnerabilidad
nivel
descripcion
fecha
```

Tabla `apk_scans`:

```text
id
user_id
file_name
file_hash
package_name
app_name
version_name
version_code
status
created_at
finished_at
summary
```

Tabla `apk_findings`:

```text
id
scan_id
tipo
titulo
severidad
descripcion
evidencia
recomendacion
created_at
```

Mejora recomendada:

- Usar hashing de contrasenas.
- Evaluar Supabase Auth.
- Configurar RLS.
- Crear migraciones SQL versionadas.

## Terraform

Terraform debe usarse como unico mecanismo oficial para definir y desplegar la infraestructura de produccion.

Objetivos:

- Definir infraestructura como codigo.
- Permitir ambientes `dev` y `prod`.
- Facilitar despliegue reproducible.
- Generar evidencia para la rubrica.
- Preparar el analisis economico requerido en FD01 al final.

Proveedor objetivo:

```text
Azure
```

Servicio objetivo:

```text
Azure Container Apps
```

Terraform administrara:

- Resource group/proyecto.
- Azure Container Registry.
- Log Analytics Workspace.
- Azure Container Apps Environment.
- Container App para dashboard Streamlit.
- Container App para API FastAPI.
- Secrets de ejecucion o integracion con Key Vault.
- Storage para APK/assets.
- Networking.
- Logs y monitoreo.

Estructura recomendada:

```text
infra/
  terraform/
    environments/
      dev/
        main.tf
        variables.tf
        outputs.tf
        terraform.tfvars.example
      prod/
        main.tf
        variables.tf
        outputs.tf
        terraform.tfvars.example
    modules/
      container_registry/
      container_app_environment/
      dashboard_app/
      api_app/
      storage/
      secrets/
      monitoring/
```

Recursos sugeridos:

```text
Aplicacion:
- Azure Container App para dashboard Streamlit.
- Azure Container App para API FastAPI.
- Azure Container Registry para imagenes Docker.
- Log Analytics para logs.

Base de datos:
- Supabase PostgreSQL como servicio externo documentado.

Secretos:
- Variables de Supabase.
- Tokens de API.
- Claves de despliegue.
- Azure Container Apps secrets o Key Vault.

Storage:
- APK compilado.
- Evidencias.
- Reportes.

Monitoreo:
- Logs de app.
- Metricas.
- Alertas basicas.
```

Automatizacion Terraform en GitHub Actions:

```text
terraform.yml
- Ejecutar terraform fmt.
- Ejecutar terraform validate.
- Ejecutar terraform plan en pull_request.
- Ejecutar terraform apply solo en main y con aprobacion.
- Guardar plan como artifact.
- Ejecutar Snyk IaC o Checkov para seguridad IaC.
```

Ejemplo base de `terraform.yml`:

```yaml
name: Terraform

on:
  pull_request:
    paths:
      - "infra/terraform/**"
  push:
    branches: [main]
    paths:
      - "infra/terraform/**"

jobs:
  terraform:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: infra/terraform/environments/prod
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3

      - name: Terraform fmt
        run: terraform fmt -check -recursive ../../

      - name: Terraform init
        run: terraform init

      - name: Terraform validate
        run: terraform validate

      - name: Terraform plan
        run: terraform plan -out=tfplan

      - name: Upload plan
        uses: actions/upload-artifact@v4
        with:
          name: terraform-plan
          path: infra/terraform/environments/prod/tfplan
```

Analisis economico con Terraform:

Al final, para FD01, se debe usar la infraestructura declarada para estimar costos.

Herramientas sugeridas:

```text
Infracost
Calculadora cloud del proveedor
Terraform plan
```

Evidencias a generar:

```text
- Tabla de recursos.
- Costo mensual estimado.
- Costo anual estimado.
- Comparacion dev vs prod.
- Justificacion de recursos elegidos.
- Capturas o reportes exportados.
```

## Analisis Estatico y Seguridad

Herramientas requeridas:

```text
SonarQube / SonarCloud
Semgrep
Snyk
```

Responsabilidades:

- Detectar bugs.
- Detectar vulnerabilidades.
- Detectar code smells.
- Detectar dependencias vulnerables.
- Analizar infraestructura como codigo.
- Bloquear PRs con problemas criticos.

## Pruebas

### Unitarias

Herramienta:

```text
pytest
```

Objetivo:

- Probar funciones aisladas.
- Controladores.
- Validaciones.
- Servicios.

### Integracion

Herramienta:

```text
pytest
```

Objetivo:

- Probar conexion entre API, dashboard y base.
- Probar insercion y lectura de reportes.
- Probar login/registro.

### BDD

Herramienta sugerida:

```text
behave
```

Objetivo:

- Documentar escenarios de usuario.
- Validar flujos completos.

Ejemplos:

```text
Dado un usuario registrado
Cuando el agente movil envia un reporte
Entonces el dashboard muestra la vulnerabilidad
```

### Interfaz

Herramienta sugerida:

```text
Playwright
```

Objetivo:

- Probar login.
- Probar dashboard.
- Probar descarga del APK.
- Probar visualizacion de reportes.

### Mutantes

Herramienta sugerida:

```text
mutmut
```

Objetivo:

- Medir calidad real de las pruebas.
- Detectar pruebas debiles.

## GitHub Workflows

Los workflows deben estar en:

```text
.github/workflows/
```

La automatizacion debe cubrir seguridad, calidad, pruebas, infraestructura, versionamiento y despliegue.

### ci.yml

Responsabilidades:

- Instalar dependencias.
- Ejecutar lint.
- Ejecutar pruebas unitarias.
- Ejecutar pruebas de integracion.
- Generar cobertura.

Pasos sugeridos:

```text
checkout
setup-python
install dependencies
pytest unit
pytest integration
coverage report
upload coverage
```

### security.yml

Responsabilidades:

- Ejecutar Sonar.
- Ejecutar Semgrep.
- Ejecutar Snyk.
- Escanear dependencias.
- Escanear IaC.
- Detectar secrets.
- Bloquear cambios con vulnerabilidades criticas.

Pasos sugeridos:

```text
checkout
semgrep ci
snyk test
snyk iac test
sonar scan
```

Automatizaciones requeridas:

```text
SonarCloud / SonarQube:
- Ejecutar analisis de bugs, vulnerabilidades, duplicacion y code smells.
- Usar token en GitHub Secrets: SONAR_TOKEN.
- Publicar Quality Gate.
- Fallar el workflow si el Quality Gate falla.

Semgrep:
- Ejecutar reglas default de seguridad.
- Analizar Python, YAML, Terraform y workflows.
- Generar reporte SARIF si se integra con GitHub Security.
- Fallar en findings de severidad alta o critica.

Snyk:
- Analizar dependencias Python.
- Analizar IaC con `snyk iac test`.
- Usar token en GitHub Secrets: SNYK_TOKEN.
- Fallar si hay vulnerabilidades criticas.
```

Secrets requeridos:

```text
SONAR_TOKEN
SNYK_TOKEN
SEMGREP_APP_TOKEN
SUPABASE_URL
SUPABASE_KEY
```

Ejemplo base de `security.yml`:

```yaml
name: Security

on:
  pull_request:
  push:
    branches: [main, develop]

jobs:
  semgrep:
    name: Semgrep
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: semgrep/semgrep-action@v1
        env:
          SEMGREP_APP_TOKEN: ${{ secrets.SEMGREP_APP_TOKEN }}

  snyk:
    name: Snyk
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - uses: snyk/actions/python@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          command: test
      - name: Snyk IaC
        run: snyk iac test infra/terraform
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

  sonar:
    name: Sonar
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest --cov=. --cov-report=xml
      - uses: SonarSource/sonarqube-scan-action@v5
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
      - uses: SonarSource/sonarqube-quality-gate-action@v1
        timeout-minutes: 5
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### deploy.yml

Responsabilidades:

- Construir version.
- Ejecutar pruebas finales.
- Construir imagen o preparar paquete.
- Aplicar Terraform.
- Desplegar dashboard/API.
- Publicar APK actualizado.

Pasos sugeridos:

```text
checkout
run tests
build artifacts
terraform plan
terraform apply
deploy app
create release tag
```

## Versionamiento

Estrategia sugerida:

```text
main        -> produccion
develop     -> integracion
feature/*   -> nuevas funcionalidades
fix/*       -> correcciones
release/*   -> preparacion de version
```

Convencion de versiones:

```text
v1.0.0
v1.1.0
v1.1.1
```

Recomendado:

- Tags por release.
- Changelog.
- Releases en GitHub.
- APK adjunto como artifact/release.

## Fases de Implementacion

La reestructuracion se ejecutara por fases para evitar romper el sistema publicado y para generar evidencia progresiva para la rubrica.

Cada fase debe cerrarse con:

```text
- Cambios implementados.
- Pruebas ejecutadas.
- Evidencias generadas.
- Issues/ramas actualizadas.
- Pendientes documentados.
```

### Estado de avance actual

```text
Fase 1 - Reestructuracion base: implementada.
Fase 2 - MVC y Supabase: implementada parcialmente y funcional.
Fase 3 - API backend: base implementada con GET /health y POST /reports.
Fase 5 - Escaneo APK: motor inicial implementado en dashboard.
Fase 6 - Historial/exportacion: historial, detalle, CSV y JSON implementados.
Fase 7 - Pruebas automatizadas: pytest, integracion, BDD e interfaz base agregados.
Fase 8 - GitHub Actions CI: workflow ci.yml agregado.
Fase 9 - Seguridad: workflow security.yml con Sonar, Semgrep y Snyk agregado.
Fase 10 - Terraform: base Azure Container Apps agregada.
Fase 11 - Despliegue: Dockerfiles y workflow base agregados; pendiente configurar secrets y publicar en Azure.
Fase 12 - Releases: workflow release.yml agregado.
Fase 13 - Documentacion: README, wiki base y roadmap agregados.
```

Pendientes inmediatos:

```text
1. Inicializar/subir repositorio GitHub si aun no existe.
2. Configurar GitHub Secrets.
3. Crear proyecto SonarCloud/Snyk/Semgrep y pegar tokens.
4. Instalar Terraform local o ejecutar validacion desde GitHub Actions.
5. Ajustar imagenes Docker finales en Terraform cuando ACR y despliegue esten listos.
6. Ejecutar mutmut en WSL o GitHub Actions, porque Windows nativo no es soportado.
```

### Fase 0: Preparacion y Control del Proyecto

Objetivo:

- Preparar el repositorio para trabajar de forma ordenada con ramas, issues, proyectos y documentacion base.

Tareas:

- Crear rama `develop`.
- Definir estrategia de ramas:
  - `main`
  - `develop`
  - `feature/*`
  - `fix/*`
  - `release/*`
- Crear GitHub Project.
- Crear labels:
  - `feature`
  - `bug`
  - `security`
  - `documentation`
  - `infra`
  - `testing`
  - `mobile`
  - `dashboard`
  - `api`
- Crear milestones por fase.
- Crear issues iniciales en formato:
  - Como...
  - Quiero...
  - Para...
- Actualizar README inicial.

Entregables:

- GitHub Project creado.
- Issues iniciales creados.
- Rama `develop`.
- README base.

Criterio de listo:

- El tablero de proyecto refleja las fases.
- Cada tarea importante tiene issue y rama asociada.

Rubrica relacionada:

- GitHub Projects.
- Contribucion al proyecto.
- README.

### Fase 1: Reestructuracion Base del Proyecto

Objetivo:

- Separar dashboard, mobile, assets, tests e infraestructura.

Tareas:

- Crear estructura nueva.
- Mover Streamlit a `app/dashboard`.
- Mover agente a `mobile/agent`.
- Mantener APK compilado en `assets`.
- Actualizar imports.
- Verificar que Streamlit siga funcionando.

Entregables:

- Estructura nueva del proyecto.
- Dashboard movido sin perder funcionalidad.
- Agente movil separado.
- Assets organizados.

Criterio de listo:

- La app local ejecuta correctamente.
- El link publico sigue siendo recuperable despues del despliegue.

Rubrica relacionada:

- README.
- Publicacion para consumo en nube.
- Base para FD04 al final.

### Fase 2: Modelo MVC y Capa de Datos Supabase

Objetivo:

- Ordenar el codigo bajo arquitectura MVC y dejar Supabase/PostgreSQL como fuente de datos estable.

Tareas:

- Separar modelos, vistas y controladores.
- Crear servicios para operaciones de negocio.
- Centralizar configuracion de Supabase.
- Evitar secrets en codigo.
- Revisar tabla `usuarios`.
- Revisar tabla `vulnerabilidades`.
- Crear script SQL o documentacion de esquema.
- Mejorar manejo de errores de Supabase.
- Preparar migraciones SQL versionadas si aplica.

Entregables:

- MVC claro.
- Configuracion por secrets.
- Esquema de base documentado.
- Acceso a Supabase probado.

Criterio de listo:

- Login funciona.
- Registro funciona.
- Dashboard lista vulnerabilidades.
- No hay secrets hardcodeados en dashboard.

Rubrica relacionada:

- README.
- FD04 al final.
- Seguridad.

### Fase 3: Crear API Backend

Objetivo:

- Evitar que el APK escriba directo en Supabase.

Tareas:

- Crear API con FastAPI.
- Crear endpoint `POST /reports`.
- Validar `user_id`.
- Insertar vulnerabilidades desde backend.
- Probar con payload del APK.

Entregables:

- API FastAPI inicial.
- Endpoint `POST /reports`.
- Endpoint `GET /health`.
- Validaciones de payload.
- Conexion API -> Supabase.

Criterio de listo:

- Un POST de prueba crea una vulnerabilidad visible en dashboard.
- La API responde correctamente en local.
- Los errores son claros.

Rubrica relacionada:

- Seguridad.
- Pruebas de integracion.
- Despliegue.

### Fase 4: Actualizar APK

Objetivo:

- Enviar reportes a la API backend.

Tareas:

- Cambiar URL del APK.
- Remover escritura directa a Supabase.
- Mostrar errores HTTP reales.
- Recompilar APK.
- Reemplazar `assets/AnzenCore_Agent.apk`.
- Probar en movil real.

Entregables:

- APK actualizado.
- APK publicado en `assets`.
- Manual de build del APK.
- Evidencia de prueba en movil.

Criterio de listo:

- El movil envia reportes.
- El dashboard muestra reportes reales.
- El APK muestra errores HTTP reales.

Rubrica relacionada:

- Publicacion.
- Releases.
- README.

### Fase 5: Escaneo de APK por Ingenieria Inversa

Objetivo:

- Implementar la funcionalidad principal para subir un APK, aplicar ingenieria inversa y detectar vulnerabilidades.

Tareas:

- Crear interfaz de carga de APK en el dashboard.
- Crear endpoint `POST /apk-scans`.
- Validar extension y tamano del archivo.
- Calcular hash del APK.
- Extraer metadatos basicos.
- Analizar AndroidManifest.
- Detectar permisos peligrosos.
- Detectar componentes exportados.
- Detectar URLs, HTTP o posibles secrets embebidos.
- Guardar registro en `apk_scans`.
- Guardar hallazgos en `apk_findings`.
- Mostrar resultado en dashboard.
- Manejar estados del escaneo:
  - pendiente
  - procesando
  - completado
  - fallido

Entregables:

- Boton/seccion "Escanear APK".
- Carga de archivo APK.
- Motor inicial de analisis.
- Tablas `apk_scans` y `apk_findings`.
- Vista de resultado del analisis.

Criterio de listo:

- Un usuario puede subir un APK.
- El sistema ejecuta analisis.
- El sistema muestra hallazgos.
- El resultado queda guardado en historial.

Rubrica relacionada:

- Funcionalidad principal del producto.
- Pruebas de integracion.
- FD03 al final.
- FD04 al final.

### Fase 6: Historial y Exportacion de Reportes

Objetivo:

- Permitir consultar escaneos anteriores y exportar reportes.

Tareas:

- Crear vista de historial de escaneos.
- Crear detalle de escaneo.
- Crear filtros por fecha, severidad y usuario.
- Crear exportacion PDF.
- Crear exportacion CSV/Excel.
- Crear exportacion JSON para integraciones.
- Adjuntar reportes como evidencia.

Entregables:

- Historial de escaneos.
- Detalle por escaneo.
- Exportacion PDF.
- Exportacion CSV/Excel o JSON.

Criterio de listo:

- El usuario puede consultar escaneos anteriores.
- El usuario puede exportar resultados.
- Los reportes incluyen hallazgos y recomendaciones.

Rubrica relacionada:

- Exportacion de evidencias.
- Integrabilidad.
- Documentacion.

### Fase 7: Pruebas Automatizadas

Objetivo:

- Crear base de calidad para CI/CD.

Tareas:

- Agregar pytest.
- Agregar pruebas unitarias.
- Agregar pruebas de integracion.
- Agregar BDD con behave.
- Agregar interfaz con Playwright.
- Agregar mutmut.

Entregables:

- Suite de pruebas unitarias.
- Suite de pruebas de integracion.
- Escenarios BDD.
- Pruebas de interfaz.
- Pruebas mutantes.
- Reporte de cobertura.

Criterio de listo:

- `pytest` ejecuta correctamente.
- BDD tiene escenarios principales.
- Playwright valida login/dashboard.
- Mutmut genera reporte.

Rubrica relacionada:

- Pruebas unitarias.
- Pruebas integracion.
- Pruebas mutantes.
- Pruebas interfaz.
- BDD.
- FD03 al final.

### Fase 8: GitHub Actions CI

Objetivo:

- Automatizar pruebas y validaciones basicas en cada push y pull request.

Tareas:

- Crear `.github/workflows/ci.yml`.
- Instalar dependencias.
- Ejecutar pruebas unitarias.
- Ejecutar pruebas de integracion.
- Ejecutar cobertura.
- Guardar reporte como artifact.

Entregables:

- Workflow `ci.yml`.
- Badge de CI en README.
- Reporte de cobertura.

Criterio de listo:

- Pull requests ejecutan CI automaticamente.
- El workflow falla si las pruebas fallan.

Rubrica relacionada:

- GitHub Actions.
- Contribucion.

### Fase 9: Seguridad y Analisis Estatico

Objetivo:

- Integrar Sonar, Semgrep y Snyk.

Tareas:

- Configurar SonarCloud o SonarQube.
- Crear workflow de Semgrep.
- Crear workflow de Snyk.
- Configurar tokens en GitHub Secrets.
- Definir reglas de bloqueo.

Entregables:

- Workflow `security.yml`.
- SonarCloud/SonarQube configurado.
- Semgrep configurado.
- Snyk configurado.
- Reportes visibles en GitHub.

Criterio de listo:

- El workflow corre en PR.
- Sonar genera Quality Gate.
- Semgrep analiza codigo.
- Snyk analiza dependencias e IaC.
- Hallazgos criticos bloquean cambios.

Rubrica relacionada:

- Actions para desarrollo seguro.
- Sin vulnerabilidades ni bugs criticos.

### Fase 10: Terraform e Infraestructura

Objetivo:

- Declarar infraestructura como codigo.

Tareas:

- Definir proveedor cloud.
- Crear modulos Terraform.
- Crear ambientes dev/prod.
- Agregar `terraform fmt`.
- Agregar `terraform validate`.
- Agregar `terraform plan` en PR.
- Agregar `terraform apply` en deploy controlado.

Entregables:

- Estructura `infra/terraform`.
- Modulos o ambientes dev/prod.
- Workflow `terraform.yml`.
- `terraform fmt`.
- `terraform validate`.
- `terraform plan`.
- Base para analisis economico.

Criterio de listo:

- Terraform valida correctamente.
- El plan se genera en PR.
- Los costos pueden estimarse al final.

Rubrica relacionada:

- Terraform.
- Analisis economico FD01 al final.
- Infraestructura FD04 al final.

### Fase 11: Despliegue

Objetivo:

- Publicar la aplicacion para consumo en nube, distinto de GitHub.

Tareas:

- Crear workflow de deploy.
- Crear Dockerfile para dashboard Streamlit.
- Crear Dockerfile para API FastAPI.
- Construir imagenes Docker en GitHub Actions.
- Publicar imagenes en Azure Container Registry.
- Configurar despliegue de dashboard en Azure Container Apps.
- Configurar despliegue de API en Azure Container Apps.
- Configurar secrets de produccion.
- Ejecutar `terraform plan`.
- Ejecutar `terraform apply` desde rama `main`.
- Validar URL publica de Azure Container Apps.

Entregables:

- App publica funcionando.
- API publica o ambiente controlado.
- Variables/secrets configurados.
- Imagenes publicadas en Azure Container Registry.
- Infraestructura creada por Terraform.
- Evidencia de despliegue.

Criterio de listo:

- El sistema se consume desde una URL publica.
- No depende de ejecucion local.
- No depende de Streamlit Cloud.
- El despliegue se reproduce con Terraform.

Rubrica relacionada:

- Publicacion para consumo en nube.
- README.
- Deploy.

### Fase 12: Versionamiento, Releases y Packages

Objetivo:

- Publicar versiones controladas del sistema y del APK.

Tareas:

- Crear workflow `release.yml`.
- Crear tags `vX.Y.Z`.
- Publicar GitHub Releases.
- Adjuntar APK como artifact.
- Publicar APK como artifact.
- Crear tags y releases.
- Documentar proceso.

Entregables:

- Release en GitHub.
- APK adjunto.
- Changelog.
- Version documentada.

Criterio de listo:

- Existe al menos una release formal.
- El APK actualizado se puede descargar desde release y dashboard.

Rubrica relacionada:

- Releases y packages.
- Versionamiento.

### Fase 13: Wikis, Roadmap y Documentacion

Objetivo:

- Crear documentacion navegable para producto, versiones y uso.

Tareas:

- Actualizar README completo.
- Preparar contenido para GitHub Wiki.
- Crear roadmap.
- Definir futuras versiones.
- Definir fechas tentativas de liberacion.
- Documentar procedimientos:
  - local
  - build APK
  - pruebas
  - despliegue
  - secrets

Entregables:

- README actualizado.
- Wiki creada.
- Roadmap documentado.
- Futuras versiones documentadas.

Criterio de listo:

- Una persona externa puede ejecutar y entender el proyecto leyendo la documentacion.

Rubrica relacionada:

- README.
- GitHub Wikis.
- Roadmap.

### Fase 14: Preparacion de Evidencias Finales

Objetivo:

- Preparar evidencia para los documentos FD01, FD02, FD03 y FD04, sin redactarlos todavia.

Tareas:

- Exportar reportes de Sonar.
- Exportar reportes Semgrep/Snyk.
- Guardar capturas de workflows.
- Guardar capturas de GitHub Projects.
- Guardar evidencias de releases.
- Guardar evidencias de despliegue publico.
- Generar diagramas preliminares por reverse engineering.
- Preparar base para Marp.

Entregables:

- Carpeta de evidencias.
- Diagramas preliminares.
- Reportes exportados.
- Guion base de exposicion.

Criterio de listo:

- Hay evidencia suficiente para redactar FD01-FD04 al final.

Rubrica relacionada:

- FD01.
- FD02.
- FD03.
- FD04.
- Exposicion.

## Prioridad Recomendada

Orden sugerido:

```text
0. Preparacion y control del proyecto
1. Reestructuracion base del proyecto
2. Modelo MVC y capa de datos Supabase
3. Crear API backend
4. Actualizar APK para enviar a API
5. Escaneo de APK por ingenieria inversa
6. Historial y exportacion de reportes
7. Pruebas automatizadas
8. GitHub Actions CI
9. Seguridad con Sonar, Semgrep y Snyk
10. Terraform e infraestructura
11. Despliegue
12. Versionamiento, releases y packages
13. Wikis, roadmap y documentacion
14. Preparacion de evidencias finales
```

## Decision Tecnica Recomendada

Mantener por ahora:

```text
Dashboard: Streamlit
Base: Supabase PostgreSQL
Mobile: Kivy APK
```

Agregar:

```text
Backend: FastAPI
CI/CD: GitHub Actions
Seguridad: Sonar + Semgrep + Snyk
IaC: Terraform
Pruebas: pytest + behave + Playwright + mutmut
```

## Resultado Esperado

Al finalizar la reestructuracion, AnzenCore deberia tener:

- Proyecto organizado por capas.
- Dashboard publicado.
- API backend validando reportes.
- APK enviando datos de forma controlada.
- Base de datos con esquema claro.
- Workflows de CI/CD.
- Analisis estatico y seguridad automatizados.
- Pruebas automatizadas.
- Infraestructura definida con Terraform.
- Versionamiento y despliegue reproducible.
