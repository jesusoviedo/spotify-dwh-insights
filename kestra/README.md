# 🔄 Orquestación con Kestra (`kestra/`)

Este proyecto utiliza **Kestra** para la orquestación de tareas y flujos. A continuación, se describe cómo configurar y ejecutar el entorno localmente utilizando **Docker Compose** junto con **Docker** para levantar Kestra.

## Configuración inicial

### 1. Crear la carpeta para los flujos de Kestra
Si no tienes una carpeta `flows` en el directorio de trabajo, debes crearla para almacenar los flujos de Kestra.

```bash
mkdir flows
```


### 2. Establecer las variables de entorno
Es necesario establecer las siguientes variables de entorno para la conexión con la base de datos PostgreSQL utilizada por Kestra. Asegúrate de reemplazar los valores de las variables por aquellos que deseas utilizar en tu entorno.

```bash
export POSTGRES_DB="<nombre_de_tu_base_de_datos>"
export POSTGRES_USER="<usuario_de_postgresql>"
export POSTGRES_PASSWORD="<contraseña_de_postgresql>"
```

Puedes agregar estas variables a tu archivo `~/.bashrc` o ejecutarlas directamente en tu terminal.

Para verificar que las variables de entorno se han configurado correctamente, puedes ejecutar los siguientes comandos:

```bash
echo $POSTGRES_DB
echo $POSTGRES_USER
echo $POSTGRES_PASSWORD
```

### 3. Agregar secrets de manera manual con codificación en Base64
Si necesitas almacenar credenciales o claves de acceso de forma segura en Kestra, puedes codificarlas en Base64 antes de agregarlas a los secrets. Esto evita exponer información sensible en archivos de configuración o código.

#### **Paso 1: Codificar el archivo o clave en Base64**
Si tienes un archivo JSON con credenciales (por ejemplo, `gcs-storage-key.json`), puedes codificarlo en Base64 con:

```bash
base64 gcs-storage-key.json
```

Si en lugar de un archivo quieres codificar un valor de texto, usa
```bash
echo -n "mi_valor_secreto" | base64
```
Esto generará una cadena codificada en Base64.

#### **Paso 2: Agregar el secreto a Kestra**
Existen dos maneras recomendadas de agregar el secreto a Kestra:

**1. A través del archivo de configuración de Kestra**

Copia el valor codificado y agrégalo directamente al archivo de configuración de Kestra en la sección de secrets.

**2. Mediante variables de entorno en Docker Compose**

Una alternativa más flexible es definir los secrets como variables de entorno y hacer referencia a ellos en el archivo `docker-compose.yml`.

Para nuestro caso, podemos definir las siguientes variables en la terminal:

```bash
export SECRET_CLIENTE_ID="$(echo -n "<cliente_id>" | base64)"
export SECRET_CLIENTE_SECRET="$(echo -n "<cliente_secret>" | base64)"
export SECRET_GCP_CREDENTIALS="$(base64 gcs-storage-key.json)"  
```

Luego, en el `docker-compose.yml`, se pueden referenciar de esta manera:

```bash
environment:
  CLIENTE_ID: ${SECRET_CLIENTE_ID}  
  CLIENTE_SECRET: ${SECRET_CLIENTE_SECRET} 
  GOOGLE_APPLICATION_CREDENTIALS: ${SECRET_GCP_CREDENTIALS}
```

Esto garantiza que los secrets se mantengan fuera del código y se administren de manera más segura dentro del entorno de ejecución.

### 4. Iniciar los servicios
Una vez que las variables de entorno y secrets estén configuradas, puedes iniciar los servicios utilizando Docker Compose. Esto levantará los contenedores necesarios para ejecutar Kestra y la base de datos PostgreSQL.

```bash
docker compose up
```

Este comando descargará las imágenes de Docker (si no están disponibles) y pondrá en marcha todos los servicios configurados en el archivo `docker-compose.yml`.


### 4. Detener los servicios
Para detener los servicios, puedes usar el siguiente comando:

```bash
docker-compose down
```

Este comando detendrá y eliminará los contenedores creados por Docker Compose.


## Solución de problemas
Si encuentras problemas al ejecutar los servicios, revisa los logs de Docker para identificar cualquier error en la configuración o en el inicio de los contenedo

```bash
docker-compose logs
```

## Flow de Kestra

En esta sección se explica el propósito de cada flujo de Kestra presente en este proyecto:

### Flow `ingestion_spotify-api-tracks-bigquery-daily.yaml`

#### **Descripción:**
Este flujo en Kestra se encarga de extraer datos desde la API de Spotify y almacenarlos en Google Cloud Storage (GCS). Utiliza un contenedor de Docker con la imagen `rj24/spotify-pipeline` para ejecutar el script `spotify_data_pipeline.py`, que se encuentra dentro del contenedor.

#### **Propósito:**
- Conectar con la API de Spotify utilizando credenciales almacenadas en secrets.
- Extraer datos sobre álbumes recientes de determinados artistas.
- Guardar la información en el Data Lake (GCS) dentro del bucket definido en la variable `BUCKET_NAME`.
- Organizar los datos dentro del dataset de BigQuery especificado en `DATASET_NAME`.

#### **Frecuencia de ejecución:**
- Este flujo se ejecuta automáticamente todos los días a las 6:00 AM (UTC) gracias a un trigger basado en cron (`"0 6 * * *"`).
- En caso de fallo, Kestra intentará reintentar la ejecución hasta 3 veces, con un intervalo de espera de 5 minutos entre cada intento (`retry.maxAttempt: 3`, `retry.delay: PT5M`).
- Esto garantiza una mayor resiliencia, reduciendo el impacto de posibles fallos temporales en la API de Spotify o en la infraestructura de procesamiento.

#### **Funcionamiento del código:**
- La tarea principal (`elt_api_spotify_tracks`) se ejecuta dentro de un contenedor de Docker y usa Kestra para gestionar la orquestación.
- Se utilizan variables de entorno (`CLIENTE_ID`, `CLIENTE_SECRET`, `GOOGLE_APPLICATION_CREDENTIALS`) para autenticarse en la API de Spotify y en GCP.
- El script `spotify_data_pipeline.py` es el encargado del procesamiento de datos y está dentro de la imagen de Docker.

 Para conocer más sobre cómo se extraen y procesan los datos dentro del contenedor, se debe revisar la carpeta  [`dlt`](../dlt/), ya que allí se encuentra la lógica del script `spotify_data_pipeline.py`.


