# Mobile Analysis Logic (AnzenCore)

Esta referencia contiene las lógicas de análisis estático para detectar vulnerabilidades en APKs y código fuente móvil. Usa esto para construir la clase `ApkAnalyzer` y el motor de detección.

## Estructura de Análisis (APK)
1. Recibir archivo en `bytes`.
2. Leer como `zipfile.ZipFile`.
3. Buscar artefactos clave (Manifiesto, `.dex`, `.so`, bases de datos `.db`, `.sqlite`).

### Reglas Arquitectónicas
- **Ausencia de AndroidManifest.xml**: Riesgo Alto. Indica manipulación del APK (OWASP M8).
- **Ausencia de classes.dex**: Riesgo Alto. No hay código ejecutable.
- **Múltiples archivos .dex (MultiDex)**: Informativo. Requiere escaneo en profundidad.
- **Librerías Nativas (`lib/*.so`)**: Riesgo Medio. Puede ocultar código malicioso (OWASP M7).
- **Bases de datos locales empaquetadas**: Riesgo Medio. Puede exponer datos sensibles o de prueba (OWASP M1).

## Detección por Expresiones Regulares (Patrones Clave)

Se deben leer archivos de texto, `.dex`, `.xml`, `.properties` e inyectarlos por expresiones regulares:

1. **Uso de HTTP en lugar de HTTPS (CWE-319, OWASP M5)**
   - Ignorar: prefijos comunes como `http://schemas.android.com/`, `http://www.w3.org/`.
   - Regla: Detectar `http://` en código Java/Kotlin.
   - Recomendación: Migrar a `https://` y utilizar `HttpsURLConnection`.

2. **Hardcoded Secrets y Tokens (CWE-798, OWASP M9)**
   - Regex: `(?i)(api[_-]?key|apikey|secret|token|bearer)\s*[:=]\s*['\"]?([A-Za-z0-9_\-\.]{16,})`
   - Regex JWT: `eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+`
   - Acción al detectar: Mostrar código pero **enmascarar** el secreto en la evidencia (`clean[:12] + "***" + clean[-6:]`).

3. **Criptografía Débil o Insegura (CWE-327, OWASP M5)**
   - Regex: `MessageDigest\.getInstance\(\s*[\"'](MD5|SHA-1)[\"']\s*\)`
   - Regex: `Cipher\.getInstance\(\s*[\"'](DES|DESede|AES/ECB/PKCS5Padding)[\"']\s*\)`
   - Recomendación: Instar al usuario a usar `SHA-256` y `AES/GCM/NoPadding`.

4. **Configuración Insegura de WebView - XSS (CWE-79, OWASP M7)**
   - Regex: `setJavaScriptEnabled\(\s*true\s*\)`
   - Recomendación: Mantener desactivado si no es estrictamente necesario.

5. **Random Number Generator Inseguro (CWE-330, OWASP M5)**
   - Regex: `new\s+java\.util\.Random\(\s*\)`
   - Recomendación: Usar `java.security.SecureRandom`.

6. **IPs Hardcodeadas (CWE-200, OWASP M9)**
   - Detectar patrones IPv4 que no sean loops locales (`127.0.0.1`, `0.0.0.0`).
   - Recomendación: Extraer variables de entorno o DNS.

## Deduplicación
- Agrupar hallazgos idénticos para evitar saturar el reporte (`set` por tipo, título y archivo fuente).

## Complejidad y Calidad (FolderAnalyzer)
- Calcular Líneas de Código (LOC).
- Ciclos: Detectar keywords (`if`, `for`, `while`, `switch`) para calcular Complejidad Ciclomática.
- Métricas: WMC (Weighted Method Count), NOM (Number of Methods), NOA (Number of Attributes).
