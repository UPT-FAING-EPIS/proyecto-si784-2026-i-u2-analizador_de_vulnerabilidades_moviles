# AnzenCore Mobile Vulnerability Analyzer Skill

Este repositorio contiene una **Skill para Agentes de IA** que encapsula toda la arquitectura, lógica de análisis de seguridad, y estructura de DevSecOps del proyecto **AnzenCore**.

Con esta skill, cualquier asistente basado en agentes puede construir analizadores de vulnerabilidades móviles complejos usando las mejores prácticas extraídas de AnzenCore (FastAPI, Streamlit, Supabase, Azure, Terraform, SonarQube, etc.).

## Instalación

1. Clona este repositorio o copia la carpeta `skills/anzencore-mobile-vuln-analyzer` en tu directorio `.agents/skills/`.
2. El agente de IA detectará la nueva skill automáticamente por su archivo `SKILL.md`.

## Uso

Simplemente pídele a tu agente:
> "Actúa como un ingeniero experto en seguridad y construye un analizador de vulnerabilidades móviles usando el blueprint de AnzenCore."

El agente invocará esta skill, leerá la carpeta de `references/` e implementará:
- Backend escalable en FastAPI para procesamiento de APKs.
- Lógicas de extracción de código, detección de hardcoded secrets, weak crypto, y mal uso de WebViews.
- Frontend en Streamlit interactivo.
- Infraestructura como código (IaC) en Terraform para Azure.
