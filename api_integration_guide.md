# Guía de Integración de API

Para que el otro grupo (o cualquier microservicio externo, como un Analizador de Vulnerabilidades) pueda consumir nuestra API, hemos habilitado un endpoint específico que no requiere autenticación ni manejo de sesiones.

## Endpoint Disponible

Este endpoint analiza un repositorio público de GitHub de forma *stateless* (sin guardar el reporte en el historial de un usuario específico, aunque sí registra la acción en nuestros logs internos).

- **URL:** `/api/analysis/external/github`
- **Método HTTP:** `POST`
- **Content-Type:** `application/x-www-form-urlencoded` o `multipart/form-data`

### Parámetros Requeridos

Deberán enviar los datos en el cuerpo (body) de la petición usando formato de formulario (form data):

| Parámetro | Tipo | Descripción |
| :--- | :--- | :--- |
| `repo_url` | `string` | La URL completa del repositorio de GitHub que desean analizar (ej: `https://github.com/usuario/repo`). |

### Estructura de Respuesta

La API responderá con un JSON (Content-Type: `application/json`) con el siguiente formato:

```json
{
  "status": "success",
  "project_name": "NombreDelRepositorio",
  "loc": 1250,
  "complexity": 45,
  "code_smells": 12
}
```

> [!NOTE]
> - `loc`: Líneas de código (Lines of Code).
> - `complexity`: Complejidad ciclomática calculada del código.
> - `code_smells`: Cantidad de "code smells" (malas prácticas) detectadas.

---

## Ejemplos de Consumo

A continuación, se muestran ejemplos de cómo el otro grupo podría consumir esta API utilizando diferentes lenguajes y herramientas.

### Usando cURL (Terminal)

```bash
curl -X POST https://anestatico.onrender.com/api/analysis/external/github \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "repo_url=https://github.com/usuario/repo"
```

### Usando JavaScript (Fetch API)

```javascript
async function analyzeRepo(repoUrl) {
  const formData = new FormData();
  formData.append("repo_url", repoUrl);

  try {
    const response = await fetch("https://anestatico.onrender.com/api/analysis/external/github", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`);
    }

    const result = await response.json();
    console.log("Resultados del análisis:", result);
  } catch (error) {
    console.error("Error al consumir la API:", error);
  }
}

analyzeRepo("https://github.com/usuario/repo");
```

### Usando Python (Requests)

```python
import requests

def analyze_repo(repo_url):
    url = "https://anestatico.onrender.com/api/analysis/external/github"
    data = {
        "repo_url": repo_url
    }
    
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        print("Análisis exitoso:", response.json())
    else:
        print("Error:", response.status_code, response.text)

analyze_repo("https://github.com/usuario/repo")
```

> [!TIP]
> Esta es la URL real de producción. El otro grupo ya puede copiar y pegar estos ejemplos directamente para hacer las pruebas de conexión.
