<center>

[comment]: <img src="./media/media/image1.png" style="width:1.088in;height:1.46256in" alt="escudo.png" />

![./media/media/image1.png](./media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERIA**

**Escuela Profesional de Ingeniería de Sistemas**

**Proyecto *AnzenCore – Plataforma de Análisis de Seguridad para Aplicaciones Móviles***

Curso: *Calidad y Pruebas de Software*

Docente: *Patrick José Cuadros Quiroga*

Integrantes:

***Arocutipa [Apellido], Gianfranco ([Código])***

***Perez Peralta, Fabrizio ([Código])***

**Tacna – Perú**

***2026***

**  
**
</center>
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

Sistema *AnzenCore*

Informe de Factibilidad

Versión *1.0*

|CONTROL DE VERSIONES||||||
| :-: | :- | :- | :- | :- | :- |
|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo|
|1\.0|GAR / FPP|PJCQ|PJCQ|18/06/2026|Versión Original|

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

# **INDICE GENERAL**

[1. Descripción del Proyecto](#_Toc52661346)

[2. Riesgos](#_Toc52661347)

[3. Análisis de la Situación actual](#_Toc52661348)

[4. Estudio de Factibilidad](#_Toc52661349)

[4.1 Factibilidad Técnica](#_Toc52661350)

[4.2 Factibilidad económica](#_Toc52661351)

[4.3 Factibilidad Operativa](#_Toc52661352)

[4.4 Factibilidad Legal](#_Toc52661353)

[4.5 Factibilidad Social](#_Toc52661354)

[4.6 Factibilidad Ambiental](#_Toc52661355)

[5. Análisis Financiero](#_Toc52661356)

[6. Conclusiones](#_Toc52661357)


<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

**<u>Informe de Factibilidad</u>**

1. <span id="_Toc52661346" class="anchor"></span>**Descripción del Proyecto**

    1.1. Nombre del proyecto

    **AnzenCore – Plataforma de Análisis de Seguridad para Aplicaciones Móviles**

    1.2. Duración del proyecto

    **2 a 3 meses** (Abril 2026 – Junio 2026)

    1.3. Descripción

    AnzenCore es una plataforma web de análisis estático de seguridad orientada a aplicaciones móviles Android. El sistema permite a los equipos de desarrollo detectar, de manera automatizada y temprana, vulnerabilidades de seguridad embebidas en archivos APK y en repositorios de código fuente Java/Kotlin.

    El proyecto surge de la necesidad real de los desarrolladores de software de contar con una herramienta accesible, en español y sin costo, capaz de identificar malas prácticas de seguridad tales como: credenciales hardcodeadas en el código, uso de protocolos de comunicación inseguros (HTTP), algoritmos criptográficos débiles o rotos (MD5, SHA-1, DES), configuraciones inseguras de WebView, generadores de números aleatorios no criptográficos, entre otras.

    AnzenCore ofrece tres componentes principales:

    - **Dashboard web interactivo** (Streamlit): Panel de control con autenticación de usuarios, carga de archivos APK, visualización de hallazgos por severidad (Crítico, Alto, Medio, Bajo, Info), historial de escaneos, comparativa de archivos y exportación de reportes PDF.
    - **API REST** (FastAPI): Interfaz programática que permite a equipos externos integrar el motor de análisis en sus flujos de CI/CD, con endpoints para APK, código fuente, URLs y repositorios GitHub.
    - **Agente móvil Android**: Aplicación instalable en dispositivos Android para el escaneo de vulnerabilidades locales del dispositivo.

    1.4. Objetivos

        1.4.1 Objetivo General

        Desarrollar una plataforma integral de análisis estático de seguridad que permita detectar vulnerabilidades en aplicaciones móviles Android (APK) y repositorios de código fuente, proporcionando reportes detallados con recomendaciones de mitigación, mediante una interfaz web accesible y una API REST para integraciones externas.

        1.4.2 Objetivos Específicos

        - **OE1**: Implementar un motor de análisis estático en Python capaz de detectar al menos 8 tipos de vulnerabilidades de seguridad (secretos hardcodeados, HTTP inseguro, criptografía débil, WebView inseguro, Random inseguro, IPs hardcodeadas, librerías nativas y bases de datos empaquetadas) en archivos APK y código fuente comprimido (ZIP).

        - **OE2**: Desarrollar una interfaz web (dashboard Streamlit) con autenticación de usuarios, carga de archivos APK, visualización de hallazgos con clasificación por severidad y OWASP Mobile Top 10, historial de escaneos y exportación de reportes en formato PDF.

        - **OE3**: Diseñar e implementar una API REST (FastAPI) con endpoints para analizar APKs, código fuente, URLs y repositorios GitHub, incluyendo un endpoint de carga de carpetas locales que retorne métricas de calidad por archivo (`code_smells.files`).

        - **OE4**: Integrar un sistema de almacenamiento persistente con Supabase (PostgreSQL) para gestionar usuarios, historial de escaneos, hallazgos de seguridad y artefactos extraídos de los APK.

        - **OE5**: Desplegar el sistema en Azure Container Apps mediante infraestructura como código (Terraform) con pipeline de CI/CD automatizado en GitHub Actions, incluyendo análisis de seguridad del propio código con Sonar, Semgrep y Snyk.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

2. <span id="_Toc52661347" class="anchor"></span>**Riesgos**

    | N° | Riesgo | Probabilidad | Impacto | Mitigación |
    |---|---|---|---|---|
    | R1 | Indisponibilidad del servicio externo de análisis de calidad (anestatico.onrender.com) | Media | Alto | Implementar manejo de errores graceful y mostrar métricas locales cuando el servicio externo falle. |
    | R2 | Limitaciones del plan gratuito de Supabase (500 MB almacenamiento, 2 conexiones simultáneas) | Media | Medio | Implementar paginación, limpieza de escaneos antiguos y monitoreo de uso de almacenamiento. |
    | R3 | Archivos APK ofuscados o cifrados que reduzcan la efectividad del análisis estático | Alta | Medio | Documentar las limitaciones del análisis estático; recomendar el uso complementario de análisis dinámico para APKs ofuscados. |
    | R4 | Costos inesperados en Azure Container Apps al superar el tier gratuito | Baja | Alto | Configurar alertas de presupuesto en Azure y aprovechar los créditos estudiantiles disponibles. |
    | R5 | Falsos positivos en la detección de secretos hardcodeados que generen desconfianza en la herramienta | Media | Medio | Refinar los patrones de detección con listas de exclusión y umbrales de longitud mínima. |
    | R6 | Cambios de versión en las dependencias (FastAPI, Streamlit) que rompan la compatibilidad | Baja | Medio | Fijar versiones exactas en `requirements.txt` y ejecutar tests de regresión en CI/CD. |
    | R7 | Dificultades en el despliegue de Azure Container Apps por falta de experiencia en cloud | Media | Medio | Documentar el proceso paso a paso y usar Terraform para reproducibilidad del entorno. |

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

3. <span id="_Toc52661348" class="anchor"></span>**Análisis de la Situación actual**

    3.1. Planteamiento del problema

    El ecosistema de aplicaciones móviles Android ha crecido exponencialmente en los últimos años, y con ello el número de aplicaciones con vulnerabilidades de seguridad explotables. Según el informe OWASP Mobile Top 10, las vulnerabilidades más frecuentes incluyen almacenamiento inseguro de datos, comunicaciones inseguras y código con secretos hardcodeados, todas detectables mediante análisis estático.

    En el contexto peruano y latinoamericano, los equipos de desarrollo de aplicaciones móviles —especialmente PyMEs y estudiantes universitarios— carecen de acceso a herramientas de análisis de seguridad que sean:
    - **Accesibles económicamente**: Las soluciones comerciales (AppScan, Checkmarx, MobSF Cloud) tienen costos de licencia elevados (desde $500/año).
    - **En español**: La mayoría de herramientas open-source carecen de documentación y reportes en español.
    - **Fáciles de operar**: Herramientas como MobSF requieren instalación local compleja y conocimientos avanzados de seguridad.
    - **Integrables en pipelines**: Pocas herramientas ofrecen una API REST lista para integración en CI/CD.

    AnzenCore resuelve esta problemática al ofrecer una plataforma web gratuita, en español, con una interfaz intuitiva y una API REST documentada, que permite detectar las vulnerabilidades más comunes en APKs y código fuente Java/Kotlin sin requerir instalación local ni conocimientos avanzados en ciberseguridad.

    3.2. Consideraciones de hardware y software

    **Hardware disponible para el desarrollo:**

    | Recurso | Especificación | Propósito |
    |---|---|---|
    | Laptop del equipo (×2) | Intel Core i5/i7, 8-16 GB RAM, 256+ GB SSD | Desarrollo y pruebas locales |
    | Servidor Azure Container Apps | 0.5–1 vCPU, 1–2 GB RAM (auto-scaling) | Despliegue del dashboard y la API |
    | Azure Container Registry | Plan Básico (gratuito con créditos estudiantiles) | Almacenamiento de imágenes Docker |

    **Software seleccionado para el desarrollo:**

    | Categoría | Tecnología | Versión | Licencia | Justificación |
    |---|---|---|---|---|
    | Lenguaje de programación | Python | 3.12 | PSF | Amplio ecosistema de librerías de seguridad y análisis |
    | Framework API | FastAPI | 0.100+ | MIT | Alto rendimiento, tipado, OpenAPI automático |
    | Dashboard web | Streamlit | 1.30+ | Apache 2.0 | Desarrollo rápido de interfaces web en Python |
    | Base de datos | Supabase (PostgreSQL 15) | — | Apache 2.0 | BaaS con autenticación y API REST, plan gratuito |
    | Contenerización | Docker | 24+ | Apache 2.0 | Portabilidad y reproducibilidad del entorno |
    | Infraestructura como código | Terraform | 1.7+ | BSL 1.1 | Despliegue reproducible en Azure |
    | CI/CD | GitHub Actions | — | MIT | Automatización de builds, tests y despliegue |
    | Análisis de seguridad del código | Sonar, Semgrep, Snyk | — | Varios | Calidad y seguridad del propio código de AnzenCore |
    | Control de versiones | Git + GitHub | — | MIT / — | Gestión del código fuente y colaboración |

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

4. <span id="_Toc52661349" class="anchor"></span>**Estudio de Factibilidad**

    El estudio de factibilidad fue preparado por los integrantes del equipo (Gianfranco Arocutipa y Fabrizio Perez Peralta) durante la fase de planificación del proyecto en el curso de Calidad y Pruebas de Software. Los resultados fueron revisados y aprobados por el docente Patrick José Cuadros Quiroga.

    El análisis concluye que el proyecto es viable en todas sus dimensiones: técnica, económica, operativa, legal, social y ambiental.

    4.1. <span id="_Toc52661350" class="anchor"></span>Factibilidad Técnica

    El estudio de viabilidad técnica evalúa los recursos tecnológicos disponibles y su aplicabilidad a las necesidades del proyecto.

    **Evaluación del equipo de desarrollo:**

    El equipo posee competencias técnicas directamente aplicables al proyecto:
    - Programación en Python (nivel avanzado): desarrollo de servicios web con FastAPI y Streamlit.
    - Conocimiento de bases de datos PostgreSQL y uso de Supabase como BaaS.
    - Experiencia con Docker y despliegue de contenedores en entornos cloud.
    - Familiaridad con conceptos de seguridad en aplicaciones móviles (OWASP Mobile Top 10).
    - Uso de GitHub Actions para automatización de pipelines CI/CD.

    **Evaluación de tecnologías:**

    Todas las tecnologías seleccionadas son de código abierto, ampliamente documentadas y con comunidades activas. Python 3.12 con FastAPI permite el desarrollo de APIs de alto rendimiento de manera rápida. Streamlit habilita la creación de dashboards interactivos sin necesidad de conocimientos de frontend (HTML/CSS/JS). Supabase provee almacenamiento PostgreSQL, autenticación y API REST en un plan gratuito adecuado para el alcance del proyecto.

    El motor de análisis estático fue desarrollado íntegramente en Python, utilizando únicamente la biblioteca estándar (módulo `zipfile`, `re`) sin dependencias externas, lo que garantiza su portabilidad y facilidad de mantenimiento.

    **Infraestructura:**

    Azure Container Apps en su tier de consumo ofrece ejecución gratuita hasta 180,000 vCPU-segundos y 360,000 GB-segundos por mes, suficiente para el volumen de uso esperado en un entorno académico. Los créditos estudiantiles de Azure cubren los costos adicionales si se superan los límites gratuitos.

    **Conclusión de Factibilidad Técnica:** El proyecto es técnicamente viable. El equipo cuenta con los conocimientos y herramientas necesarias para su desarrollo e implantación.

    4.2. <span id="_Toc52661351" class="anchor"></span>Factibilidad Económica

    El propósito de este estudio es determinar los beneficios y costos económicos del proyecto.

    Dado que AnzenCore es un proyecto académico que utiliza exclusivamente herramientas open-source e infraestructura en sus niveles gratuitos, la inversión se concentra en el recurso humano (horas de desarrollo del equipo).

        4.2.1. Costos Generales

        | Ítem | Unidad | Cantidad | Costo Unit. (S/.) | Total (S/.) |
        |---|---|---|---|---|
        | Material de impresión (documentación) | Paquete | 1 | 25.00 | 25.00 |
        | Servicio de internet (hogar) | Mes | 3 | 80.00 | 240.00 |
        | Energía eléctrica adicional | Mes | 3 | 30.00 | 90.00 |
        | Útiles de escritorio | Global | 1 | 20.00 | 20.00 |
        | **TOTAL COSTOS GENERALES** | | | | **375.00** |

        4.2.2. Costos operativos durante el desarrollo

        | Ítem | Detalle | Total (S/.) |
        |---|---|---|
        | Comunicación (videollamadas, reuniones virtuales) | Google Meet, Discord – gratuito | 0.00 |
        | Gestión del proyecto | GitHub Projects – gratuito | 0.00 |
        | Almacenamiento de código | GitHub Free – gratuito | 0.00 |
        | **TOTAL COSTOS OPERATIVOS** | | **0.00** |

        4.2.3. Costos del ambiente (infraestructura)

        | Servicio | Plan utilizado | Costo mensual | Total 3 meses (S/.) |
        |---|---|---|---|
        | Supabase (base de datos PostgreSQL) | Free Tier (500 MB, 2 conexiones) | $0.00 | 0.00 |
        | Azure Container Apps (Dashboard + API) | Consumption Plan (créditos estudiantiles) | $0.00 | 0.00 |
        | Azure Container Registry | Basic (créditos estudiantiles) | $0.00 | 0.00 |
        | GitHub Actions CI/CD | Free Tier (2,000 min/mes) | $0.00 | 0.00 |
        | Render.com (servicio análisis externo) | Free Tier | $0.00 | 0.00 |
        | **TOTAL COSTOS DE AMBIENTE** | | | **0.00** |

        4.2.4. Costos de personal

        | Integrante | Rol | Horas/mes | Meses | Tarifa (S/./hora) | Total (S/.) |
        |---|---|---|---|---|---|
        | Gianfranco Arocutipa | Desarrollador Backend / DevOps | 50 | 3 | 25.00 | 3,750.00 |
        | Fabrizio Perez Peralta | Desarrollador Backend / Frontend | 50 | 3 | 25.00 | 3,750.00 |
        | **TOTAL COSTOS DE PERSONAL** | | | | | **7,500.00** |

        > *Nota: La tarifa de S/. 25/hora representa el costo de oportunidad estimado para estudiantes universitarios de Ingeniería de Sistemas en Tacna.*

        4.2.5. Costos totales del desarrollo del sistema

        | Categoría | Total (S/.) |
        |---|---|
        | Costos Generales | 375.00 |
        | Costos Operativos | 0.00 |
        | Costos de Ambiente / Infraestructura | 0.00 |
        | Costos de Personal | 7,500.00 |
        | **COSTO TOTAL DEL PROYECTO** | **7,875.00** |

        El costo efectivo en dinero real desembolsado es de **S/. 375.00** (costos generales), ya que la infraestructura es gratuita y los costos de personal representan el tiempo de dedicación de los estudiantes como parte de su formación académica.

    4.3. <span id="_Toc52661352" class="anchor"></span>Factibilidad Operativa

    **Beneficios del sistema:**

    AnzenCore aporta los siguientes beneficios operativos a sus usuarios:
    - **Detección automatizada de vulnerabilidades**: Lo que manualmente requeriría días de revisión de código, AnzenCore lo realiza en segundos.
    - **Reportes accionables**: Cada hallazgo incluye descripción técnica, evidencia de código y recomendación de mitigación con ejemplos de código seguro.
    - **Clasificación estándar**: Los hallazgos se alinean con OWASP Mobile Top 10 y CWE, permitiendo priorización objetiva.
    - **Historial de escaneos**: Permite rastrear la evolución de la seguridad de una aplicación a lo largo del tiempo.
    - **Exportación de reportes**: Generación de reportes PDF para entrega a clientes o revisión por parte de equipos de QA.

    **Capacidad de mantenimiento:**

    El sistema es mantenible gracias a:
    - Arquitectura en capas (controladores, servicios, modelos) que facilita la incorporación de nuevos detectores de vulnerabilidades.
    - Tests automatizados (unitarios, de integración y BDD con Behave) que previenen regresiones.
    - Pipeline CI/CD que automatiza el despliegue ante cada cambio aprobado.
    - Documentación técnica en el repositorio GitHub.

    **Interesados (Stakeholders):**

    | Rol | Descripción |
    |---|---|
    | Equipo de desarrollo | Gianfranco Arocutipa, Fabrizio Perez Peralta |
    | Docente / Supervisor | Patrick José Cuadros Quiroga |
    | Usuarios finales | Desarrolladores Android, equipos de QA, estudiantes de Ingeniería de Sistemas |
    | Equipo integrador externo | Equipos que consumen la API REST para integrar AnzenCore en sus pipelines |

    4.4. <span id="_Toc52661353" class="anchor"></span>Factibilidad Legal

    AnzenCore cumple con el marco legal peruano e internacional aplicable:

    - **Licencias de software**: Todas las librerías utilizadas (FastAPI – MIT, Streamlit – Apache 2.0, Pydantic – MIT, Supabase-py – MIT) son de código abierto con licencias permisivas que permiten su uso, modificación y distribución sin restricciones comerciales.
    - **Protección de datos personales**: El sistema almacena únicamente datos de autenticación (usuario y contraseña hasheada con PBKDF2-HMAC-SHA256) y resultados de análisis técnicos. No procesa ni almacena datos personales de usuarios finales de las aplicaciones analizadas. Cumple con la **Ley N° 29733 – Ley de Protección de Datos Personales del Perú** y su reglamento (D.S. N° 003-2013-JUS).
    - **Uso ético del análisis de APKs**: El análisis estático de APKs es legal cuando se realiza sobre aplicaciones propias o con autorización expresa del propietario. AnzenCore incluye en su documentación un aviso de uso responsable.
    - **Propiedad intelectual**: El código fuente de AnzenCore es desarrollado íntegramente por el equipo; no reproduce código propietario de terceros. El proyecto puede ser registrado como obra intelectual ante INDECOPI de ser necesario.
    - **Sin conflictos con regulaciones de seguridad**: La herramienta es defensiva (análisis de vulnerabilidades propias), no ofensiva, por lo que no entra en conflicto con la **Ley N° 30096 – Ley de Delitos Informáticos**.

    4.5. <span id="_Toc52661354" class="anchor"></span>Factibilidad Social

    AnzenCore tiene un impacto social positivo en múltiples dimensiones:

    - **Democratización de la seguridad**: Al ser gratuito y en español, pone al alcance de PyMEs y estudiantes peruanos herramientas de seguridad que antes solo estaban disponibles para grandes empresas.
    - **Formación en seguridad**: Los reportes incluyen explicaciones didácticas de cada vulnerabilidad y ejemplos de código seguro, promoviendo la cultura de desarrollo seguro (DevSecOps) en equipos locales.
    - **Reducción de riesgo para usuarios finales**: Al ayudar a los desarrolladores a corregir vulnerabilidades antes del lanzamiento, se protege indirectamente a los usuarios de las aplicaciones analizadas de ataques como robo de credenciales o intercepción de comunicaciones.
    - **Contribución académica**: El proyecto sirve como referencia y base para investigaciones futuras en análisis estático de seguridad en la Universidad Privada de Tacna.
    - **Ética profesional**: El sistema promueve la responsabilidad profesional en el desarrollo de software, alineándose con el código de ética del Colegio de Ingenieros del Perú (CIP).

    4.6. <span id="_Toc52661355" class="anchor"></span>Factibilidad Ambiental

    El impacto ambiental de AnzenCore es mínimo y predominantemente positivo:

    - **Infraestructura cloud eficiente**: Al desplegarse en Azure Container Apps con escalado automático a cero cuando no hay solicitudes, el sistema no consume recursos computacionales en periodos de inactividad, reduciendo el consumo energético frente a servidores dedicados 24/7.
    - **Energía renovable**: Microsoft Azure opera varios de sus centros de datos con energía 100% renovable y tiene compromisos de carbono negativo para 2030, reduciendo la huella de carbono del proyecto.
    - **Sin residuos físicos**: Al ser un sistema enteramente digital (sin hardware dedicado, sin impresión masiva de reportes), su operación no genera residuos físicos.
    - **Desmaterialización**: AnzenCore reemplaza procesos manuales de revisión de código (que pueden requerir impresión de documentos) por análisis digital automatizado.
    - **Eficiencia energética del motor de análisis**: El motor de análisis estático está optimizado para procesar APKs en segundos, minimizando el tiempo de cómputo y el consumo energético asociado.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

5. <span id="_Toc52661356" class="anchor"></span>**Análisis Financiero**

    El plan financiero evalúa la inversión requerida y los beneficios esperados del proyecto AnzenCore desde el punto de vista económico.

    5.1. Justificación de la Inversión

        5.1.1. Beneficios del Proyecto

        **Beneficios Tangibles:**

        | Beneficio | Estimación |
        |---|---|
        | Reducción del tiempo de detección de vulnerabilidades en APKs | De 2–5 días (revisión manual) a menos de 1 minuto (análisis automatizado) |
        | Ahorro en herramientas comerciales equivalentes (MobSF Pro, AppScan, Checkmarx) | S/. 1,800 – S/. 7,500 anuales por licencia |
        | Reducción de costos de corrección tardía de vulnerabilidades | El costo de corregir una vulnerabilidad en producción es 6–100x mayor que en desarrollo (IBM System Sciences Institute) |
        | Generación de reportes PDF automáticos | Ahorro estimado de 2–4 horas por reporte generado manualmente |

        **Beneficios Intangibles:**

        - Mejora de la cultura de seguridad (DevSecOps) en los equipos de desarrollo.
        - Aumento de la confianza de los clientes en las aplicaciones desarrolladas.
        - Ventaja competitiva para los desarrolladores que demuestren prácticas de seguridad verificadas.
        - Disponibilidad de información objetiva para toma de decisiones sobre lanzamiento de aplicaciones.
        - Contribución al ecosistema de herramientas open-source en español para Latinoamérica.
        - Formación práctica del equipo en áreas de alta demanda laboral (DevSecOps, Cloud, Python).

        5.1.2. Criterios de Inversión

            5.1.2.1. Relación Beneficio/Costo (B/C)

            Dado el carácter académico del proyecto, la evaluación B/C se realiza comparando el valor generado frente al costo de oportunidad de las horas invertidas.

            | Concepto | Valor (S/.) |
            |---|---|
            | Costo total del proyecto | 7,875.00 |
            | Beneficio estimado (ahorro en licencias comerciales equivalentes, primer año) | 3,600.00 |
            | Beneficio estimado (ahorro en horas de revisión manual, primer año – 50 escaneos) | 6,250.00 |
            | **Beneficio total estimado (primer año)** | **9,850.00** |
            | **Relación B/C** | **1.25** |

            **B/C = 1.25 > 1 → Se acepta el proyecto.**

            5.1.2.2. Valor Actual Neto (VAN)

            Considerando una tasa de descuento del 10% anual (costo de oportunidad de capital estimado para proyectos de software en entornos académicos peruanos) y un horizonte de 2 años de uso:

            | Año | Beneficio Neto (S/.) | Factor de descuento (10%) | Valor Actual (S/.) |
            |---|---|---|---|
            | 0 | -7,875.00 | 1.000 | -7,875.00 |
            | 1 | 9,850.00 | 0.909 | 8,953.85 |
            | 2 | 8,500.00 | 0.826 | 7,021.00 |
            | **VAN** | | | **8,099.85** |

            **VAN = S/. 8,099.85 > 0 → Se acepta el proyecto.**

            5.1.2.3. Tasa Interna de Retorno (TIR)

            Aplicando el método de interpolación con los flujos de caja estimados:

            | Año | Flujo Neto (S/.) |
            |---|---|
            | 0 | -7,875.00 |
            | 1 | 9,850.00 |
            | 2 | 8,500.00 |

            **TIR ≈ 102%**

            El Costo de Oportunidad de Capital (COK) estimado es del 10% anual.

            **TIR (102%) > COK (10%) → Se acepta el proyecto.**

            El proyecto genera una rentabilidad significativamente superior al costo de oportunidad del capital, lo que confirma su viabilidad económica.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

6. <span id="_Toc52661357" class="anchor"></span>**Conclusiones**

El análisis de factibilidad realizado para el proyecto **AnzenCore – Plataforma de Análisis de Seguridad para Aplicaciones Móviles** arroja los siguientes resultados:

| Dimensión | Resultado | Conclusión |
|---|---|---|
| **Técnica** | El equipo posee las competencias necesarias y las tecnologías seleccionadas (Python, FastAPI, Streamlit, Supabase, Azure) son maduras y gratuitas | **VIABLE** |
| **Económica** | El costo real desembolsado es de S/. 375.00; la infraestructura es gratuita. B/C = 1.25, VAN = S/. 8,099.85 | **VIABLE** |
| **Operativa** | El sistema es fácil de operar, mantenible por CI/CD automatizado y aporta beneficios concretos a los usuarios | **VIABLE** |
| **Legal** | Cumple con la Ley N° 29733 (datos personales), Ley N° 30096 (delitos informáticos) y todas las licencias son open-source permisivas | **VIABLE** |
| **Social** | Democratiza el acceso a herramientas de seguridad en español para desarrolladores peruanos y latinoamericanos | **VIABLE** |
| **Ambiental** | Infraestructura cloud de bajo consumo energético con escalado a cero; Microsoft Azure tiene compromisos de energía renovable | **VIABLE** |

**El proyecto AnzenCore es factible en todas sus dimensiones.** Se recomienda proceder con su desarrollo e implementación dentro del plazo establecido de 2 a 3 meses, priorizando los objetivos específicos OE1 (motor de análisis) y OE2 (dashboard) como núcleo funcional del sistema.
