# 🔄 Integración y Despliegue Automático (`.github/workflows/`)

Este proyecto utiliza GitHub Actions para automatizar el despliegue de una instancia de **Kestra** en Google Cloud Platform (GCP), así como la validación y despliegue de los flujos de trabajo. El flujo completo asegura que los flujos se validen correctamente antes de ser desplegados, y que el entorno de ejecución esté listo y funcional tras cada cambio.



## Secretos requeridos
Asegúrate de configurar los siguientes secretos en tu repositorio para que los workflows funcionen correctamente:

| Secreto                      | Descripción                                           |
|-----------------------------|-------------------------------------------------------|
| `KESTRA_USER`               | Usuario administrador de Kestra                      |
| `KESTRA_PASSWORD`           | Contraseña del usuario administrador                 |
| `KESTRA_HOSTNAME`           | Dirección IP o hostname donde corre Kestra           |
| `POSTGRES_DB`               | Nombre de la base de datos PostgreSQL                |
| `POSTGRES_USER`             | Usuario para la base de datos                        |
| `POSTGRES_PASSWORD`         | Contraseña para la base de datos                     |
| `SECRET_CLIENTE_ID_BASE64`  | Credencial codificada del cliente de Spotify         |
| `SECRET_CLIENTE_SECRET_BASE64` | Secreto codificado del cliente de Spotify         |
| `SECRET_PROJECT_ID_BASE64`  | ID del proyecto en GCP (codificado)                  |
| `SECRET_GCP_CREDENTIALS_BASE64` | Credenciales del servicio GCP (base64)           |
| `GCP_CREDENTIALS_JSON`      | JSON de autenticación para el acceso a GCP           |
| `GCP_PROJECT_ID`            | ID del proyecto en GCP                               |
| `GCP_INSTANCE_NAME`         | Nombre de la instancia de GCP                        |
| `GCP_ZONE`                  | Zona donde se encuentra la instancia                 |



## Workflows
### 1. `ci-cd-deploy-instance.yml`: despliegue de la instancia Kestra en GCP
Este workflow se ejecuta cuando se hace un pull request a la rama `main` que modifica el archivo `kestra/docker-compose.yaml`. Sus pasos principales incluyen:

- Validar que todas las variables de entorno estén definidas correctamente.
- Subir los archivos `.env` y `docker-compose.yaml` a la instancia de GCP.
- Reiniciar la instancia Docker Compose que ejecuta Kestra.
- Verificar la salud del servidor.
- Lanzar automáticamente el flujo de `init-prod-kv` si existe.

Este workflow garantiza que el entorno de ejecución de Kestra esté actualizado y funcional después de cada cambio estructural.


### 2. `ci-cd-deploy-flows.yml`: validación y despliegue de flujos Kestra
Este workflow se activa con un pull request a la rama `main` cuando se modifican archivos dentro de `kestra/flows/**`.

Consta de tres trabajos secuenciales:

#### `validate`
- Valida todos los flujos en `./kestra/flows` usando la acción oficial de Kestra.
- Se conecta a la instancia para verificar que la estructura de los flujos sea válida.

#### `prod`
- Despliega los flujos validados en los siguientes `namespaces`:
  - `spotify-dwh-insights.prod`
  - `spotify-dwh-insights.ingestion`
  - `spotify-dwh-insights.transformation`
- Utiliza la acción oficial de Kestra para realizar el despliegue sin eliminar flujos existentes (`delete: false`).

#### `run-init-kv`
- Verifica que la instancia de Kestra esté activa.
- Lanza automáticamente el flujo `init-prod-kv`, que inicializa claves en el KV Store necesarias para el entorno productivo.


## 🚀 Estado de los Workflows CI/CD

| Descripción | Estado |
|------------|--------|
| Despliegue de Flujos Kestra | [![CI-CD-Deploy-Kestra-Flows](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-deploy-flows.yml/badge.svg)](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-deploy-flows.yml) |
| Despliegue de Instancia Kestra | [![CI-CD-Deploy-Kestra-Instance](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-deploy-instance.yml/badge.svg)](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-deploy-instance.yml) |

Estos badges muestran el estado actual de los procesos de CI/CD en GitHub Actions para desplegar tanto los flujos de Kestra como la instancia en GCP usando Terraform.