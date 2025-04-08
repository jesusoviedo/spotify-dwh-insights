# ☁️ Infraestructura como Código

Esta carpeta contiene los archivos de configuración de Terraform utilizados para definir y gestionar la infraestructura de nuestro proyecto. Cada archivo está organizado para mejorar la legibilidad y el mantenimiento, agrupando recursos y configuraciones específicas. 

## Archivos de Configuración
- **`main.tf`**: Archivo principal que coordina la configuración de otros archivos.
- **`variables.tf`**: Definición de variables utilizadas en otros archivos de configuración.


- **`ec2.tf`**: Configuración para instancias EC2 de AWS.
- **`ecr.tf`**: Configuración para repositorios de imágenes en Amazon ECR.
- **`iam.tf`**: Definición de roles y políticas de IAM (Identity and Access Management).

- **`network.tf`**: Configuración de redes, subredes y componentes relacionados.
- **`outputs.tf`**: Definición de las salidas de Terraform que muestran información importante después de la aplicación.
- **`security_groups.tf`**: Configuración de grupos de seguridad para controlar el acceso a los recursos.



## Carpeta de Scripts

- **`script/`**: Contiene un script Bash para generar pares de claves pública-privada usando `ssh-keygen`. Este script es útil para crear claves para acceder a instancias y otros recursos.


/*/*/*/*


## Flujo de trabajo en Terraform

Antes de ejecutar las sentencias descritas a continuación, asegúrate de crear un bucket en Google Cloud Storage (GCS) para almacenar el archivo de estado de Terraform. Se ha creado un script para facilitar esta tarea; para más detalles, consulta la carpeta [`scripts`](../scripts/).

### Configuración de las credenciales de Google Cloud

Establecer la variable de entorno con las credenciales de GCP:

```bash
export GOOGLE_CREDENTIALS="path/to/your/gcs-storage-key.json"
```

Verificar que la variable de entorno esté configurada correctamente:

```bash
echo $GOOGLE_CREDENTIALS
```

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

### Eliminar recursos (Opcional)

Eliminar todos los recursos creados:

```bash
terraform destroy
```









/*/*/*/*/*/*

## Carpeta de Variables

- **`vars/`**: Contiene ejemplos de archivos `.tfvars` para diferentes ambientes:
  - **`example_dev.tfvars`**: Ejemplo de configuración para el ambiente de desarrollo.
  - **`example_prod.tfvars`**: Ejemplo de configuración para el ambiente de producción.

Para aplicar la configuración de Terraform, asegúrate de haber configurado correctamente los archivos `.tfvars` según el ambiente deseado y utiliza los comandos de Terraform para gestionar la infraestructura.

Para más detalles sobre el uso de cada archivo y cómo aplicarlos, consulta la [documentación de Terraform](https://www.terraform.io/docs).