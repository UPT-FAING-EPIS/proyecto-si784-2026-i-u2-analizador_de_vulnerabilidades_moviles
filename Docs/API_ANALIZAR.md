# API AnzenCore — Endpoint `/api/analizar`

API REST para analizar aplicaciones moviles y detectar vulnerabilidades de
seguridad. Pensada para que otros equipos integren el analisis de AnzenCore
sin necesidad de acceder al codigo fuente del analizador.

## URL del endpoint

```
POST {BASE_URL}/api/analizar
```

`BASE_URL` es la direccion donde se despliega esta API (ej.
`http://localhost:8000` en desarrollo).

Content-Type: `multipart/form-data`

## Campos del request

| Campo           | Tipo   | Obligatorio | Descripcion                                                                 |
|-----------------|--------|-------------|------------------------------------------------------------------------------|
| `tipo_analisis` | string | Si          | `"apk"`, `"codigo_fuente"`, `"url"` o `"repo_github"`                         |
| `archivo`       | file   | Si, cuando `tipo_analisis` es `apk` o `codigo_fuente` | Archivo `.apk` o `.zip` con el codigo fuente |
| `url`           | string | Si, cuando `tipo_analisis` es `url` o `repo_github` | URL/host de la app o backend a analizar (`url`), o URL del repo de GitHub (`repo_github`) |

## Ejemplos de request

### Analizar un APK

```bash
curl -X POST "{BASE_URL}/api/analizar" \
  -F "tipo_analisis=apk" \
  -F "archivo=@app-release.apk"
```

### Analizar codigo fuente (zip)

```bash
curl -X POST "{BASE_URL}/api/analizar" \
  -F "tipo_analisis=codigo_fuente" \
  -F "archivo=@codigo-fuente.zip"
```

### Analizar una URL

```bash
curl -X POST "{BASE_URL}/api/analizar" \
  -F "tipo_analisis=url" \
  -F "url=https://api.miapp.com"
```

### Analizar calidad de un repositorio de GitHub

Este modo delega el analisis a un servicio externo de calidad de codigo y
devuelve sus metricas (`metricas_calidad`).

```bash
curl -X POST "{BASE_URL}/api/analizar" \
  -F "tipo_analisis=repo_github" \
  -F "url=https://github.com/usuario/repo"
```

## Formato del response

### 1. Analisis limpio (sin vulnerabilidades)

```json
{
  "estado": "ok",
  "tipo_analisis": "apk",
  "objetivo": "app-release.apk",
  "tamano_bytes": 15234567,
  "resumen": {
    "total_vulnerabilidades": 0,
    "severidad_maxima": "Info",
    "conteo_por_severidad": {
      "Critico": 0,
      "Alto": 0,
      "Medio": 0,
      "Bajo": 0,
      "Info": 0
    }
  },
  "vulnerabilidades": [],
  "fecha_analisis": "2026-06-12T21:03:34.387922+00:00"
}
```

### 2. Analisis con vulnerabilidades encontradas

```json
{
  "estado": "ok",
  "tipo_analisis": "apk",
  "objetivo": "app-release.apk",
  "tamano_bytes": 15234567,
  "resumen": {
    "total_vulnerabilidades": 2,
    "severidad_maxima": "Critico",
    "conteo_por_severidad": {
      "Critico": 1,
      "Alto": 1,
      "Medio": 0,
      "Bajo": 0,
      "Info": 0
    }
  },
  "vulnerabilidades": [
    {
      "id": "insecure_communication-1",
      "tipo": "insecure_communication",
      "titulo": "Uso de HTTP no cifrado",
      "severidad": "Alto",
      "descripcion": "Se detectaron endpoints HTTP sin cifrado dentro del APK.",
      "evidencia": "http://insecure.example.com/api",
      "recomendacion": "Usar HTTPS y validar certificados correctamente.",
      "archivo_origen": "res/values/strings.xml",
      "cwe": "CWE-319",
      "owasp": "M5"
    },
    {
      "id": "hardcoded_secret-2",
      "tipo": "hardcoded_secret",
      "titulo": "Posible secreto hardcodeado",
      "severidad": "Critico",
      "descripcion": "Se detectaron patrones compatibles con tokens, secrets o API keys embebidas.",
      "evidencia": "api_key***1234",
      "recomendacion": "Eliminar secretos del APK y moverlos a un backend seguro.",
      "archivo_origen": "res/values/strings.xml",
      "cwe": "CWE-798",
      "owasp": "M9"
    }
  ],
  "fecha_analisis": "2026-06-12T21:05:10.123456+00:00"
}
```

`severidad` puede ser: `"Critico"`, `"Alto"`, `"Medio"`, `"Bajo"` o `"Info"`.

### 2b. Analisis de calidad de repositorio (`tipo_analisis = "repo_github"`)

```json
{
  "estado": "ok",
  "tipo_analisis": "repo_github",
  "objetivo": "https://github.com/usuario/repo",
  "tamano_bytes": null,
  "resumen": {
    "total_vulnerabilidades": 0,
    "severidad_maxima": "Info",
    "conteo_por_severidad": {
      "Critico": 0,
      "Alto": 0,
      "Medio": 0,
      "Bajo": 0,
      "Info": 0
    }
  },
  "vulnerabilidades": [],
  "metricas_calidad": {
    "proyecto": "repo",
    "lineas_codigo": 1250,
    "complejidad": 45,
    "code_smells": 12
  },
  "fecha_analisis": "2026-06-12T21:59:56.351361+00:00"
}
```

### 3. Error del servidor

Las respuestas de error usan el formato estandar de FastAPI:

```json
{
  "detail": "Error interno al analizar la aplicacion."
}
```

## Tipos de vulnerabilidades que detecta

Para `tipo_analisis = "apk"` y `"codigo_fuente"`:

| `tipo`                    | Severidad | Descripcion                                                |
|---------------------------|-----------|-------------------------------------------------------------|
| `manifest`                | Alto      | `AndroidManifest.xml` no encontrado o APK corrupto (solo `apk`) |
| `dex`                     | Alto/Info | Sin clases DEX, o MultiDex detectado (solo `apk`)            |
| `native_code`              | Medio     | Librerias nativas (`.so`) que pueden ocultar logica sensible |
| `insecure_communication`   | Alto      | Endpoints `http://` sin cifrar dentro del paquete            |
| `hardcoded_secret`          | Critico   | Posibles API keys, tokens o secretos embebidos               |

Para `tipo_analisis = "url"` (`tipo = "remote_scan"`), severidad `Critico`/`Alto`/`Medio`:
SSL/TLS Misconfiguration, Open Ports Detected, Weak Password Policy,
Outdated Dependencies, Missing Security Headers.

Para `tipo_analisis = "repo_github"` no se devuelven `vulnerabilidades`; en su
lugar se devuelven metricas de calidad (`metricas_calidad.lineas_codigo`,
`metricas_calidad.complejidad`, `metricas_calidad.code_smells`) obtenidas del
servicio externo de analisis estatico.

## Codigos de error posibles

| Codigo | Cuando ocurre                                                                 |
|--------|--------------------------------------------------------------------------------|
| 200    | Analisis completado (con o sin vulnerabilidades)                              |
| 400    | `tipo_analisis` invalido, falta `archivo`/`url`, archivo vacio o no es un APK/ZIP valido |
| 422    | Falta el campo obligatorio `tipo_analisis` en el form                          |
| 502    | No se pudo contactar el servicio externo de calidad (`repo_github`)            |
| 500    | Error interno inesperado durante el analisis                                   |

## CORS

El endpoint permite peticiones desde cualquier origen por defecto
(`Access-Control-Allow-Origin: *`). Para restringirlo a origenes especificos,
configurar la variable de entorno `CORS_ORIGINS` con una lista separada por
comas, por ejemplo:

```
CORS_ORIGINS=https://miapp.com,https://otro-equipo.com
```

## Servicio externo de calidad (`repo_github`)

`tipo_analisis = "repo_github"` consume, via `multipart/form-data` con el
parametro `repo_url`, la URL configurada en la variable de entorno
`ANZEN_EXTERNAL_URL` (por defecto
`https://anestatico.onrender.com/api/analysis/external/github`). Para usar
otra instancia, configurar `ANZEN_EXTERNAL_URL` con la URL completa del
endpoint externo.

## Consumir la API desde JavaScript/TypeScript

```ts
type Severidad = "Critico" | "Alto" | "Medio" | "Bajo" | "Info";

interface Vulnerabilidad {
  id: string;
  tipo: string;
  titulo: string;
  severidad: Severidad;
  descripcion: string | null;
  evidencia: string | null;
  recomendacion: string | null;
  archivo_origen: string | null;
  cwe: string | null;
  owasp: string | null;
}

interface MetricasCalidad {
  proyecto: string | null;
  lineas_codigo: number | null;
  complejidad: number | null;
  code_smells: number | null;
}

interface ReporteAnalisis {
  estado: string;
  tipo_analisis: "apk" | "codigo_fuente" | "url" | "repo_github";
  objetivo: string | null;
  tamano_bytes: number | null;
  resumen: {
    total_vulnerabilidades: number;
    severidad_maxima: Severidad;
    conteo_por_severidad: Record<Severidad, number>;
  };
  vulnerabilidades: Vulnerabilidad[];
  metricas_calidad: MetricasCalidad | null;
  fecha_analisis: string;
}

const BASE_URL = "http://localhost:8000";

// Analizar un archivo APK
export async function analizarApk(file: File): Promise<ReporteAnalisis> {
  const form = new FormData();
  form.append("tipo_analisis", "apk");
  form.append("archivo", file);

  const response = await fetch(`${BASE_URL}/api/analizar`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail ?? "Error al analizar la aplicacion.");
  }

  return response.json();
}

// Analizar una URL
export async function analizarUrl(url: string): Promise<ReporteAnalisis> {
  const form = new FormData();
  form.append("tipo_analisis", "url");
  form.append("url", url);

  const response = await fetch(`${BASE_URL}/api/analizar`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail ?? "Error al analizar la aplicacion.");
  }

  return response.json();
}

// Analizar la calidad de un repositorio de GitHub
export async function analizarRepoGithub(repoUrl: string): Promise<ReporteAnalisis> {
  const form = new FormData();
  form.append("tipo_analisis", "repo_github");
  form.append("url", repoUrl);

  const response = await fetch(`${BASE_URL}/api/analizar`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail ?? "Error al analizar la aplicacion.");
  }

  return response.json();
}
```
