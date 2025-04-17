# Configuración de GCP para el Proyecto

Este documento describe los pasos necesarios para configurar el entorno en Google Cloud Platform (GCP) antes de desplegar el proyecto.

Si aún no tienes la CLI de gcloud instalada en tu máquina local, puedes seguir las instrucciones oficiales aquí: [instalar la CLI de gcloud](https://cloud.google.com/sdk/docs/install?hl=es-419).

## 1. Crear un Proyecto en GCP
Antes de comenzar, debes tener una cuenta en Google Cloud y haber activado la facturación.

1. Accede a GCP en Google Cloud Console.
2. En la barra superior, haz clic en el Selector de Proyecto y luego en Nuevo Proyecto.
3. Asigna un nombre al proyecto.
4. Selecciona una cuenta de facturación.
5. Haz clic en Crear y espera a que el proyecto esté listo.


## 2. Habilitar las APIs necesarias
Ejecuta el siguiente comando en la terminal con `gcloud` para habilitar las APIs necesarias:

```bash
gcloud services enable storage.googleapis.com \
    bigquery.googleapis.com \
    compute.googleapis.com \
    iam.googleapis.com
```

O puedes hacerlo manualmente desde **APIs & Services** en la consola de GCP.

## 3. Crear cuentas de servicio y asignar permisos
Para permitir que diferentes partes del proyecto accedan a los servicios de GCP, se deben crear una o tres cuentas de servicio con permisos específicos.



### 3.1. Cuenta de servicio
1. Ejecuta el siguiente comando para crear la cuenta de servicio:
```bash
gcloud iam service-accounts create spotify-gcs-bq-ce-sa \
    --description="Cuenta con permisos para GCS, BigQuery y Compute Engine" \
    --display-name="GCS Storage-BigQuery-Compute Engine Service Account"
```

En un entorno de desarrollo, se puede utilizar una única cuenta de servicio con todos los permisos necesarios. Sin embargo, en un entorno de producción, por razones de seguridad, es recomendable utilizar cuentas de servicio separadas para Google Cloud Storage (GCS), BigQuery y Compute Engine, asegurando así un control más granular sobre los permisos y minimizando riesgos.



### 3.2. Asignar permisos para GCS (Data Lake)
Asigna los permisos necesarios:
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:spotify-gcs-bq-ce-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"
```



### 3.3. Asignar permisos para BigQuery (Data Warehouse)
Asigna los permisos necesarios:
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:spotify-gcs-bq-ce-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.admin"
```



### 3.4. Asignar permisos para Compute Engine (Instancias con Docker)
Asigna los permisos necesarios:
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:spotify-gcs-bq-ce-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/compute.admin"
```



### 3.5. Genera y descarga la clave JSON:
```bash
gcloud iam service-accounts keys create gcs-storage-key.json \
    --iam-account=spotify-gcs-bq-ce-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

**⚠️ Importante: No subas este archivo a GitHub.**



## 4. Configurar credenciales en tu entorno local
Si vas a ejecutar el proyecto en tu máquina, exporta las credenciales de las cuentas de servicio:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/gcs-storage-key.json"
```

Si trabajas con múltiples credenciales, puedes configurarlas en tu código o en los scripts de ejecución.



## 5. Verificación
Para asegurarte de que todo está configurado correctamente, ejecuta:

```bash
gcloud auth list
gcloud projects list
gcloud services list
```

Esto te mostrará las cuentas activas, los proyectos disponibles y las APIs habilitadas.


## Asignación de Roles en IAM

Para simplificar los comandos y la configuración en este proyecto, se han asignado roles de tipo admin a algunas cuentas de servicio. Esto permite una gestión más sencilla de los recursos y evita problemas de permisos durante las pruebas.

**⚠️ Importante para entornos productivos**

En entornos productivos, no se recomienda otorgar permisos administrativos amplios. En su lugar, se deben asignar roles específicos según las necesidades de cada servicio. Esto sigue el principio de menor privilegio, reduciendo riesgos de seguridad y acceso no autorizado.

**🔍 Más información sobre roles en IAM**

Para entender qué roles asignar y cómo gestionarlos, consulta la documentación oficial de Google Cloud:

📖 [Lista de roles en IAM](https://cloud.google.com/iam/docs/understanding-roles)

📖 [Administración de permisos con gcloud](https://cloud.google.com/iam/docs/granting-changing-revoking-access?hl=es-419#gcloud)



## Conclución
Ahora tienes un entorno listo en GCP con:
- Un proyecto configurado.
- APIs habilitadas.
- Cuentas de servicio con permisos adecuados.
- Credenciales disponibles para interactuar con GCP.
