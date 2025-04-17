# 🔄 Orquestación con Kestra

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
# ⚠️ Usa nombres reales y evita valores por defecto en producción
# ⚠️ Nunca dejes estos valores en texto plano en archivos versionados

# PostgreSQL Configuration
export POSTGRES_DB="<nombre_de_tu_base_de_datos>"
export POSTGRES_USER="<usuario_de_postgresql>"
export POSTGRES_PASSWORD="<contraseña_de_postgresql>"

# Kestra Admin Credentials
export KESTRA_USER="<usuario_debe_ser_correo_valido>"
export KESTRA_PASSWORD="<contraseña_de_kestra>"
```

Puedes agregar estas variables a tu archivo `~/.bashrc` o ejecutarlas directamente en tu terminal.

Para verificar que las variables de entorno se han configurado correctamente, puedes ejecutar los siguientes comandos:

```bash
echo $POSTGRES_DB
echo $POSTGRES_USER
echo $POSTGRES_PASSWORD
echo $KESTRA_USER
echo $KESTRA_PASSWORD
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
export SECRET_PROJECT_ID="$(echo -n "<project_id>" | base64)"
export SECRET_CLIENTE_SECRET="$(echo -n "<cliente_secret>" | base64)"
export SECRET_GCP_CREDENTIALS="$(base64 gcs-storage-key.json)"  
```

Luego, en el `docker-compose.yml`, se pueden referenciar de esta manera:

```bash
environment:
  SECRET_CLIENTE_ID: ${SECRET_CLIENTE_ID}  
  SECRET_CLIENTE_SECRET: ${SECRET_CLIENTE_SECRET} 
  SECRET_PROJECT_ID: ${SECRET_PROJECT_ID}
  SECRET_GCP_CREDENTIALS: ${SECRET_GCP_CREDENTIALS}
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
Este flujo en Kestra se encarga de extraer datos desde la API de Spotify y almacenarlos en Google Cloud Storage (GCS) y BigQuery. Utiliza un contenedor de Docker con la imagen `rj24/spotify-pipeline` para ejecutar el script `spotify_data_pipeline.py`, que se encuentra dentro del contenedor. 

#### **Propósito:**
- Conectar con la API de Spotify utilizando credenciales almacenadas en secrets.
- Extraer datos sobre álbumes recientes de determinados artistas.
- Guardar la información en el Data Lake (GCS) dentro del bucket definido en la variable `BUCKET_NAME`.
- Cargar la información procesada dentro de un dataset de BigQuery (`DATASET_NAME`).

#### **Frecuencia de ejecución:**
- Este flujo se ejecuta automáticamente todos los días a las 6:00 AM y 6:00 PM UTC-3 (`cron: "0 6,18 * * *"`).
- En caso de fallo, Kestra intentará reintentar la ejecución hasta 3 veces, con un intervalo de espera de 5 minutos entre cada intento (`retry.maxAttempt: 3`, `retry.delay: PT5M`).

#### **Funcionamiento del código:**
- La tarea principal (`elt_api_spotify_tracks`) se ejecuta dentro de un contenedor Docker usando la imagen `rj24/spotify-pipeline:v3.0`.
- Se utilizan variables de entorno (`SECRET_CLIENTE_ID`, `SECRET_CLIENTE_SECRET`, `SECRET_GCP_CREDENTIALS`) para autenticarse en la API de Spotify y en GCP.
- El script `spotify_data_pipeline.py` es el encargado del procesamiento de datos y está dentro de la imagen de Docker.

Para conocer más sobre cómo se extraen y procesan los datos dentro del contenedor, se debe revisar la carpeta [`dlt`](../dlt/), ya que allí se encuentra la lógica del script `spotify_data_pipeline.py`.


### Flow `spotify-tracks-dbt-daily.yaml`

#### **Descripción:**
Este flujo ejecuta un modelo de transformación utilizando dbt para transformar los datos previamente cargados a BigQuery desde la API de Spotify. Utiliza el contenedor oficial `ghcr.io/kestra-io/dbt-bigquery`.

#### **Propósito:**
- Clonar el repositorio con los modelos de dbt.
- Construir todos los modelos de transformación de datos (`dbt build`) ubicados en el directorio `dbt/musics_data_modeling`.
- Cargar los modelos finales a BigQuery dentro del dataset configurado.

#### **Frecuencia de ejecución:**
- Este flujo se ejecuta automáticamente todos los días a las 8:00 AM y 8:00 PM UTC-3 (`cron: "0 8,20 * * *"`).
- En caso de fallo, Kestra intentará reintentar la ejecución hasta 3 veces, con un intervalo de espera de 5 minutos entre cada intento (`retry.maxAttempt: 3`, `retry.delay: PT5M`).

#### **Funcionamiento del código:**
- Se clona el repositorio `spotify-dwh-insights` en su rama principal.
- Luego se ejecuta `dbt debug`, `dbt deps` y `dbt build` apuntando al proyecto `musics_data_modeling`.
- Se usan secretos para las credenciales GCP (`GCP_CREDENTIALS`, `PROJECT_ID`) y valores almacenados en variables Kestra (`DATASET_NAME_DBT`, `LOCATION`).


### Flow `init-prod-kv.yaml`

#### **Descripción:**
Este flujo de inicialización configura el almacenamiento de claves y valores (KV Store) en Kestra para el proyecto Spotify DWH Insights. Define valores clave necesarios para la ejecución de otros flujos, como nombres de datasets, buckets y ubicación en GCP.

#### **Propósito:**
- Configurar las variables globales necesarias para el resto de los flujos del proyecto.
- Centralizar la gestión de parámetros como el bucket de GCS, nombres de datasets de BigQuery y la región de GCP.
- Asegurar que otros flujos puedan reutilizar esta información sin definirla explícitamente.

#### **Claves configuradas:**
- `LOCATION`: Región de GCP (por ejemplo, US).
- `BUCKET_NAME`: Nombre del bucket en Google Cloud Storage donde se almacenan los datos.
- `DATASET_NAME`: Dataset de BigQuery donde se carga la información cruda desde la API de Spotify.
- `DATASET_NAME_DBT`: Dataset de BigQuery donde se almacenan los modelos finales generados con dbt.

#### **Frecuencia de ejecución:**
- Este flujo se ejecuta automáticamente cada hora (`cron: "0 * * * *"`) en la zona horaria `America/Asuncion`.

#### **Funcionamiento del código:**
- Cada tarea utiliza el plugin `io.kestra.plugin.core.kv.Set` para definir una clave de configuración.
- Las claves se almacenan en el namespace `spotify-dwh-insights`, que luego es utilizado por otros flujos como `ingestion_spotify-api-tracks-bigquery-daily.yaml` y `spotify-tracks-dbt-daily.yaml`.
- Esto permite desacoplar la configuración del código, facilitando la reutilización y mantenimiento del pipeline.
