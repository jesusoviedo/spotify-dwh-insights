# Terraform

## Verificar la instalación de Terraform
Para comprobar si tienes Terraform instalado, ejecuta el siguiente comando:

```bash
terraform --version
```

Si no está instalado, puedes seguir las instrucciones oficiales para instalar Terraform en tu sistema operativo:

🔗 [Terraform Docs - Instalación](https://developer.hashicorp.com/terraform/install)

## Configuración Inicial

### Configurar las credenciales del proveedor
Antes de ejecutar los comandos de Terraform, es necesario configurar las credenciales del proveedor de la nube que se va a utilizar. En este caso, se establece una variable de entorno para las credenciales de GCP:

```bash
export GOOGLE_CREDENTIALS='./gcp_credentials'
```

Esto indica a Terraform dónde encontrar las credenciales de GCP. La ruta `./gcp_credentials` debe ser el archivo que contiene tus credenciales.

### Visualizar la variable de entorno

Para verificar que la variable de entorno ha sido correctamente configurada, puedes ejecutar:

```bash
echo $GOOGLE_CREDENTIALS
```

## Comandos Comunes de Terraform

A continuación, se describen los comandos más utilizados para trabajar con Terraform y gestionar tu infraestructura:

### Inicializar Terraform
El comando terraform init descarga los proveedores de infraestructura y configura el backend. Es esencial ejecutarlo al comenzar a trabajar con Terraform en un proyecto nuevo.

```bash
terraform init
```

### Formatear archivos de Terraform
Utiliza este comando para asegurar que los archivos de configuración de Terraform estén bien formateados y sigan las convenciones de estilo.

```bash
terraform fmt
```

### Validar la sintaxis de Terraform
Antes de aplicar cualquier cambio, puedes verificar que la configuración de Terraform es sintácticamente correcta con:

```bash
terraform validate
```

### Generar un plan de ejecución
Este comando muestra un plan detallado de los cambios que se realizarán en tu infraestructura (creación, modificación, eliminación de recursos) sin ejecutarlos aún. Es útil para revisar lo que ocurrirá antes de aplicar los cambios.

```bash
terraform plan
```

### Aplicar el plan (agregar, modificar o eliminar recursos)
Este comando aplica el plan generado anteriormente y realiza los cambios en tu infraestructura según lo definido en los archivos de configuración.

```bash
terraform apply
```

### Aplicar el plan con autoaprobación
Si deseas ejecutar el plan sin tener que confirmar manualmente, puedes usar la opción -auto-approve, lo que realiza los cambios automáticamente.

```bash
terraform apply -auto-approve
```

### Eliminar todos los recursos
Si deseas destruir todos los recursos creados por Terraform en tu infraestructura, puedes usar el siguiente comando:

```bash
terraform destroy
```

### Eliminar todos los recursos con autoaprobación
Similar al comando anterior, pero con la opción -auto-approve, eliminando todos los recursos sin solicitar confirmación.

```bash
terraform destroy -auto-approve
```

## Documentación
Para obtener más información sobre el uso de terraform, puedes consultar su documentación oficial en:

🔗 [Terraform Documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
