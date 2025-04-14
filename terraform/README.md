# ☁️ Infraestructura como Código

Esta carpeta contiene los archivos de configuración de Terraform utilizados para definir y gestionar la infraestructura en Google Cloud Platform (GCP) para el proyecto **Spotify DWH Insights**. Los recursos están organizados en archivos separados para facilitar la legibilidad, modularidad y mantenimiento.



## Archivos de Configuración
- **`main.tf`**: Archivo principal donde se define el proveedor de GCP, la autenticación y orquesta la ejecución de los recursos declarados en otros archivos.
- **`variables.tf`**: Definición de variables reutilizables como zona, proyecto, credenciales, y parámetros de configuración de recursos.
- **`outputs.tf`**: Define las salidas que Terraform mostrará luego de aplicar la infraestructura, como la IP pública de la instancia.


### Recursos específicos
- **`compute_instance.tf`**: Contiene la configuración de la instancia de VM (Compute Engine) donde se despliega Kestra usando Docker Compose.
- **`network.tf`**: Reglas de firewall para exponer puertos necesarios (por ejemplo, el 8080 para acceder a la interfaz de Kestra).
- **`bigquery.tf`**: Crea datasets de BigQuery con configuraciones específicas como expiración de tablas.
- **`gcs.tf`**: Crea un bucket de Google Cloud Storage con reglas de ciclo de vida para automatizar la limpieza de archivos temporales o incompletos.


### Consideraciones de Seguridad
Los secretos sensibles como credenciales, claves y contraseñas no se almacenan en los archivos de configuración. En su lugar, se cargan como variables de entorno y codificación Base64.



## Flujo de trabajo en Terraform
Antes de ejecutar las sentencias descritas a continuación, asegúrate de crear un bucket en Google Cloud Storage (GCS) para almacenar el archivo de estado de Terraform. Se ha creado un script para facilitar esta tarea; para más detalles, consulta la carpeta [`scripts`](../scripts/).


### Configuración de las credenciales de Google Cloud
Primero, establece la variable de entorno con el archivo de credenciales de GCP:
```bash
export GOOGLE_CREDENTIALS="path/to/your/gcs-storage-key.json"
```

Para verificar que la variable de entorno esté configurada correctamente, ejecuta:
```bash
echo $GOOGLE_CREDENTIALS
```


### Configuración de variables adicionales
Además de la variable `GOOGLE_CREDENTIALS`, necesitarás configurar otras variables de entorno para que Terraform funcione correctamente. A continuación, establece las siguientes variables:

```bash
export TF_VAR_postgres_db="your_postgres_db"
export TF_VAR_postgres_user="your_postgres_user"
export TF_VAR_postgres_password="your_postgres_password"

export TF_VAR_kestra_user="your_kestra_user"
export TF_VAR_kestra_password="your_kestra_password"

export TF_VAR_secret_cliente_id="your_client_id_base64_encoded"
export TF_VAR_secret_cliente_secret="your_client_secret_base64_encoded"
export TF_VAR_secret_project_id="your_project_id_base64_encoded"
export TF_VAR_secret_gcp_credentials="your_gcp_credentials_base64_encoded_json"
```


### Codificación Base64 para las variables `TF_VAR_secret_`
Es importante recordar que las variables que contienen `TF_VAR_secret_` deben estar codificadas en base64 para proteger su contenido. A continuación, te mostramos cómo codificar estos valores:

- **Para un archivo JSON** (como las credenciales de GCP), puedes usar el siguiente comando para obtener su versión codificada en base64:
```bash
base64 gcs-storage-key.json
```

Esto generará una cadena base64 que podrás utilizar para la variable `TF_VAR_secret_gcp_credentials`.


- **Para valores de texto** (como los IDs de cliente o secretos), utiliza el siguiente comando para codificar el valor en base64:
```bash
echo -n "mi_valor_secreto" | base64
```

Esto generará una cadena base64 que puedes usar para las variables `TF_VAR_secret_cliente_id`, `TF_VAR_secret_cliente_secret`, y `TF_VAR_secret_project_id`.



### Inicialización de Terraform
Obtener proveedores y configurar el backend de GCP:
```bash
terraform init
```


### Desarrollo y validación
Formatear los archivos de Terraform:
```bash
terraform fmt
```

Validar la sintaxis de los archivos de Terraform:
```bash
terraform validate
```


### Ejecución y aplicación del plan
Ver el plan de ejecución:
```bash
terraform plan
```

Aplicar el plan de ejecución:
```bash
terraform apply
```

Al ejecutar `terraform apply`, se creará lo siguiente:
- Una instancia de VM con Docker Compose para desplegar Kestra
- Un bucket de GCS para almacenar datos intermedios
- Datasets de BigQuery para análisis
- Reglas de red que permiten acceder a la interfaz de Kestra


### Eliminar recursos (Opcional)
Eliminar todos los recursos creados:
```bash
terraform destroy
```

Para más detalles sobre el uso de cada archivo y cómo aplicarlos, consulta la [documentación de Terraform](https://www.terraform.io/docs).