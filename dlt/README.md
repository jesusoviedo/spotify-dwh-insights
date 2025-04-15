# 🚀 Extracción e Ingesta con DLT

Aquí se encuentran los scripts que utilizan **DLT (Data Loading Tool)** para la ingesta de datos. Además, se incluye un archivo **Dockerfile** que permite crear un contenedor Docker, facilitando la integración de este flujo de trabajo en un entorno de **Kestra** o cualquier otra plataforma de orquestación de datos. Con este contenedor, podrás ejecutar los scripts de ingesta de manera eficiente y reutilizable.


## Entorno de desarrollo

Crear entorno e instalar dependencias con pipenv

```bash
pipenv --python 3.12
```

```bash
pipenv install requests requests-cache pandas pyarrow google-cloud-storage google-cloud-bigquery-storage dlt[bigquery]
pipenv install --dev pre-commit ruff black isort
```


## Script `spotify_data_pipeline.py`

Este script carga archivos Parquet con información sobre canciones, álbumes y artistas en Google Cloud Storage (GCS) y guarda los datos en BigQuery.

### Enfoque ELT

Este script implementa un enfoque **ELT (Extract, Load, Transform)** para procesar y cargar datos de la API de Spotify en Google Cloud Storage (GCS) y BigQuery. El flujo de trabajo se divide en tres pasos principales:

1. **Extract (Extraer):**
    - Se obtiene un **token de acceso** desde la API de Spotify usando las credenciales de cliente.
    - Se extraen **nuevos lanzamientos de álbumes y sus canciones** mediante consultas a la API de Spotify.
    - Se realiza una consulta adicional para obtener **información detallada de cada álbum** mediante la API de Spotify.
    - Se obtiene **información de los artistas** involucrados en las canciones mediante la API de Spotify.

2. **Load (Cargar):**
    - Los datos extraídos se guardan inicialmente en archivos **Parquet** de manera local y luego se cargan en un **bucket de Google Cloud Storage (GCS)** para su almacenamiento y posterior procesamiento.

3. **Transform (Transformar):**
    - Una vez que los datos están en GCS, el script utiliza **DLT (Data Loading Tool)** para leer los archivos Parquet desde GCS, transformarlos y cargarlos en **BigQuery**. En este paso, se garantiza que los datos estén organizados y estructurados para su posterior modelado en **DBT**, permitiendo la generación de información valiosa a partir de ellos.
    - Durante este proceso, **DLT** emplea un mecanismo de merge para evitar la duplicación de canciones que ya existen en BigQuery, asegurando que solo se inserten nuevas canciones.

Este enfoque ELT permite almacenar datos crudos en GCS, procesarlos y transformarlos de manera eficiente antes de cargarlos en BigQuery, donde pueden ser modelados con **DBT** para su análisis y visualización.

### Funcionalidad:

1. **Basado en el script `api_spotify.py`:** este script toma como base las funcionalidades del archivo `api_spotify.py`. Para más detalles, consulta el archivo [`README.md`](../scripts/README.md)
2. **Lectura de archivos Parquet:** lee múltiples archivos Parquet que contienen datos sobre canciones.
3. **Carga en GCS:** los archivos Parquet se cargan en Google Cloud Storage (GCS).
4. **Procesamiento con DLT:** utiliza DLT para tomar ciertos archivos de GCS y cargarlos en un dataset de BigQuery.

Antes de ejecutar el script `spotify_data_pipeline.py`, es necesario establecer las siguientes variables de entorno:
- `CLIENTE_ID`: el ID de cliente para autenticarte en la API de Spotify.
- `CLIENTE_SECRET`: el secreto de cliente para autenticarte en la API de Spotify.
- `GOOGLE_APPLICATION_CREDENTIALS`: el archivo de credenciales de servicio de Google Cloud


### Establecer las variables de entorno en Linux (Terminal Bash)
En la terminal, antes de ejecutar el script, puedes setear las variables de entorno con los siguientes comandos:

```bash
export CLIENTE_ID="tu_cliente_id"
export CLIENTE_SECRET="tu_cliente_secret"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/gcs-storage-key.json"
```

Sustituye "tu_cliente_id" y "tu_cliente_secret" por tus valores reales.

### Verificar que las variables se establecieron correctamente
Para asegurarte de que las variables de entorno se configuraron correctamente, puedes ejecutar los siguientes comandos:

```bash
echo $CLIENTE_ID
echo $CLIENTE_SECRET
echo $GOOGLE_APPLICATION_CREDENTIALS
```

Si todo está bien configurado, deberías ver los valores de tus variables.

### Ejecución del script

Ejecuta el script desde la línea de comandos proporcionando nombre del bucket como parámetros:

```bash
pipenv shell
python spotify_data_pipeline.py --bucket_name <nombre_del_bucket> --dataset_name <nombre_del_dataset>
```

Asegúrate de reemplazar `<nombre_del_bucket>` y `<nombre_del_dataset>` con el nombre del bucket donde se deben cargar los archivos y el nombre del dataset donde se almacenara la data raw en BigQuery.


## Creación y Despliegue de la Imagen Docker
Ejecutar el script dentro de un contenedor Docker proporciona varias ventajas, como la portabilidad y la consistencia en cualquier entorno. Al crear y usar una imagen Docker, te aseguras de que el entorno y las dependencias estén configurados de manera idéntica, lo que elimina posibles discrepancias entre diferentes máquinas o sistemas operativos. Esto facilita la ejecución del script en entornos de desarrollo, producción o en plataformas de orquestación como **Kestra**.

Para crear una imagen Docker y subirla a Docker Hub, sigue estos pasos:

### Construir la imagen Docker:
```bash
docker build -t spotify-pipeline:v1.0 .
```


### Iniciar sesión en Docker Hub:
```bash
docker login
```


### Etiquetar la imagen para Docker Hub:
```bash
docker tag spotify-pipeline:v1.0 rj24/spotify-pipeline:v1.0
```


### Subir la imagen a Docker Hub:
```bash
docker push rj24/spotify-pipeline:v1.0
```


### Ejecutar la imagen Docker:
```bash
docker run \
-v /home/joviedo/spotify-dwh-insights/.gcp_credentials:/gcp_credentials \
-e GOOGLE_APPLICATION_CREDENTIALS="/gcp_credentials/gcs-storage-key.json" \
-e CLIENTE_ID=$CLIENTE_ID \
-e CLIENTE_SECRET=$CLIENTE_SECRET \
rj24/spotify-pipeline:v1.0 \
--bucket_name spotify-dwh-insights-music-info \
--dataset_name spotify_raw_data
```
