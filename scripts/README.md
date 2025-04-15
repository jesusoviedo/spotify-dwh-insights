# 🛠 Scripts Auxiliares

Esta carpeta contiene scripts en Python para interactuar con la API de Spotify, así como para crear recursos en Google Cloud Platform (GCP).

Antes de consumir la API de Spotify, es necesario completar algunos pasos previos, los cuales se explican en el archivo [`README.md`](../data/README.md) de la carpeta `data`. Allí encontrarás una guía rápida sobre cómo autenticarte y utilizar el servicio de Spotify, junto con ejemplos de respuestas de los endpoints que se emplearán en este proyecto.

## Entorno de desarrollo

Crear entorno e instalar dependencias con pipenv

```bash
pipenv --python 3.12
```

```bash
pipenv install requests requests-cache pandas pyarrow google-cloud-storage
pipenv install --dev pre-commit ruff black isort
```

## Script `api_spotify.py`

El script `api_spotify.py` interactúa con la API de Spotify para obtener información sobre álbumes, canciones y artistas. Este script puede ser utilizado para acceder a datos relacionados con la música almacenados en Spotify, como álbumes recientes, detalles de pistas y artistas asociados. Los datos recuperados pueden ser almacenados o procesados para otros fines, como análisis de datos o visualización.

Antes de ejecutar el script `api_spotify.py`, es necesario establecer las siguientes variables de entorno:
- `CLIENTE_ID`: el ID de cliente para autenticarte en la API de Spotify.
- `CLIENTE_SECRET`: el secreto de cliente para autenticarte en la API de Spotify.

### Establecer las variables de entorno en Linux (Terminal Bash)
En la terminal, antes de ejecutar el script, puedes setear las variables de entorno con los siguientes comandos:

```bash
export CLIENTE_ID="tu_cliente_id"
export CLIENTE_SECRET="tu_cliente_secret"
```

Sustituye "tu_cliente_id" y "tu_cliente_secret" por tus valores reales.

### Verificar que las variables se establecieron correctamente
Para asegurarte de que las variables de entorno se configuraron correctamente, puedes ejecutar los siguientes comandos:

```bash
echo $CLIENTE_ID
echo $CLIENTE_SECRET
```

Si todo está bien configurado, deberías ver los valores de tus variables.

### Ejecución del script

```bash
pipenv shell
python api_spotify.py
```



## Script `gcp_utils.py`

El script `gcp_utils.py` contiene funciones utilitarias para interactuar con los servicios de Google Cloud Platform (GCP). Estas funciones pueden incluir operaciones comunes como la creación y gestión de recursos en GCP, por ejemplo, la creación de buckets en Google Cloud Storage (GCS), la configuración de autenticaciones, o la gestión de datos en Google BigQuery.

### Configura las credenciales de Google Cloud: 
Asegúrate de tener el archivo de credenciales de servicio de Google Cloud y que esté configurado en la variable de entorno `GOOGLE_APPLICATION_CREDENTIALS`. 

Puedes hacer esto con el siguiente comando:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/gcs-storage-key.json"
```

### Verificar que las variables se establecieron correctamente:
Para asegurarte de que las variables de entorno se configuraron correctamente, puedes ejecutar:

```bash
echo $GOOGLE_APPLICATION_CREDENTIALS
```

Si todo está bien configurado, deberías ver el valor de tu variable.


### Creacion de un bucket:

Ejecuta el script desde la línea de comandos proporcionando el tipo de acción y el nombre del bucket como parámetros:

```bash
pipenv shell
python gcp_utils.py gcs-create <nombre_bucket>
```

Asegúrate de reemplazar `<nombre_del_bucket>` con el nombre deseado para el bucket de Google Cloud Storage.
