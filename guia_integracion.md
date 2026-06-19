# Guía de Integración: Funcionalidades Extendidas de Análisis

Esta guía describe cómo el equipo integrador puede consumir las nuevas capacidades del motor de análisis estático desde su Frontend, específicamente para:
1. Obtener y mostrar detalles de métricas archivo por archivo (para comparativas).
2. Enviar y analizar el contenido de carpetas locales completas.

---

## 1. Mostrar Detalle por Archivos (Comparativa)

El endpoint actual que utilizan para analizar repositorios de GitHub (`/api/analysis/external/github`) **ya retorna** la información detallada por cada archivo. No necesitan llamar a un nuevo endpoint, solo extraer la información del JSON de respuesta.

### Estructura de la Respuesta

Toda la información por archivo se encuentra dentro del arreglo `code_smells.files` en la respuesta de la API.

```json
{
  "status": "success",
  "project_name": "usuario/repositorio",
  "loc": 1500,
  "complexity": 45,
  "code_smells": {
    "smells": [ ... ],
    "metrics": { "nom": 12, "npm": 10, "noa": 5, "cloc": 100 },
    "files": [
      {
        "file_path": "src/main/DatabaseConnection.java",
        "loc": 43,
        "complexity": 3,
        "metrics": {
           "nom": 2, // Número de Métodos
           "noa": 5  // Número de Atributos
        },
        "smells": [ "Código duplicado detectado...", "Variable no utilizada..." ]
      },
      {
        "file_path": "src/main/ITrabajadorRepository.java",
        "loc": 14,
        "complexity": 0,
        "metrics": {
           "nom": 1,
           "noa": 0
        },
        "smells": []
      }
    ]
  }
}
```

> [!TIP]
> **Instrucciones para la Interfaz Gráfica**
> Para armar la vista de comparativa de archivos, simplemente deben iterar sobre el array `response.data.code_smells.files`. Para cada elemento del arreglo, pueden mapear las propiedades directas como `loc`, `complexity`, y las propiedades anidadas en métricas (`metrics.nom`, `metrics.noa`) a su diseño de "Tarjetas de Archivos".

---

## 2. Analizar una Carpeta Local

Se ha habilitado un **nuevo endpoint** diseñado específicamente para el consumo de servicios externos. Este endpoint permite subir múltiples archivos (toda una carpeta local) sin necesidad de manejar sesiones o guardar estado en nuestra base de datos.

### Endpoint
`POST /api/analysis/external/upload_folder`

### Parámetros Requeridos (FormData)
- `project_name` (Text): El nombre de la carpeta o del proyecto.
- `files` (File Array): La lista de archivos que conforman el directorio.

> [!IMPORTANT]
> Para permitir la selección de carpetas enteras desde el navegador, deben asegurarse de utilizar los atributos `webkitdirectory` y `multiple` en su input de HTML.

### Ejemplo de Implementación en JavaScript / React

```html
<!-- Input HTML para carpetas -->
<input type="file" id="folderInput" webkitdirectory multiple />
```

```javascript
async function analizarCarpetaLocal() {
    const input = document.getElementById('folderInput');
    const files = input.files;
    
    if (files.length === 0) {
        alert("Por favor, selecciona una carpeta.");
        return;
    }

    // 1. Preparar el FormData
    const formData = new FormData();
    // Extraer el nombre base de la carpeta
    const nombreCarpeta = files[0].webkitRelativePath.split('/')[0] || "Carpeta_Local";
    formData.append("project_name", nombreCarpeta);

    // 2. Agregar todos los archivos al FormData
    // Es vital que el campo se llame "files" para que FastAPI lo reconozca como lista
    for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
    }

    // 3. Consumir el nuevo endpoint
    try {
        const response = await fetch("http://<NUESTRO_HOST>/api/analysis/external/upload_folder", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        console.log("Resultados del análisis:", data);
        
        // 4. Mostrar la comparativa
        // Usar data.code_smells.files para alimentar las tarjetas comparativas
        const detallesPorArchivo = data.code_smells.files;
        
    } catch (error) {
        console.error("Error al analizar la carpeta:", error);
    }
}
```

### Respuesta del Endpoint
El endpoint devolverá **exactamente la misma estructura JSON** detallada en la Sección 1. De esta manera, el procesamiento de los resultados en su frontend será 100% reutilizable tanto si analizan un repositorio de GitHub como si analizan una carpeta local.
