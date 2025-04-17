# 🔄 Integración y Despliegue Automático (`.github/workflows/`)

Este proyecto utiliza **GitHub Actions** para automatizar aspectos clave del ciclo de vida de desarrollo:

1. Provisionamiento de infraestructura con **Terraform** en GCP.
2. Despliegue de una instancia de **Kestra** en GCP.
3. Validación y despliegue de flujos de trabajo de Kestra.
4. Construcción y publicación de una imagen Docker a DockerHub cuando se modifican los archivos del pipeline.
5. Escaneo automático de secretos sensibles con GitGuardian.
6. Validación de estilo y calidad de código con Pre-Commit.


## Secretos requeridos

Asegúrate de configurar los siguientes secretos en tu repositorio para que los workflows funcionen correctamente:

| Secreto                          | Descripción                                                  |
|----------------------------------|--------------------------------------------------------------|
| `KESTRA_USER`                    | Usuario administrador de Kestra                             |
| `KESTRA_PASSWORD`               | Contraseña del usuario administrador                        |
| `KESTRA_HOSTNAME`               | Dirección IP o hostname donde corre Kestra                  |
| `POSTGRES_DB`                   | Nombre de la base de datos PostgreSQL                       |
| `POSTGRES_USER`                 | Usuario para la base de datos                               |
| `POSTGRES_PASSWORD`             | Contraseña para la base de datos                            |
| `SECRET_CLIENTE_ID_BASE64`      | Credencial codificada del cliente de Spotify                |
| `SECRET_CLIENTE_SECRET_BASE64`  | Secreto codificado del cliente de Spotify                   |
| `SECRET_PROJECT_ID_BASE64`      | ID del proyecto en GCP (codificado)                         |
| `SECRET_GCP_CREDENTIALS_BASE64` | Credenciales del servicio GCP (base64)                      |
| `GCP_CREDENTIALS_JSON`          | JSON de autenticación para el acceso a GCP                  |
| `GCP_PROJECT_ID`                | ID del proyecto en GCP                                      |
| `GCP_INSTANCE_NAME`             | Nombre de la instancia de GCP                               |
| `GCP_ZONE`                      | Zona donde se encuentra la instancia                        |
| `DOCKER_USERNAME`               | Usuario de Docker Hub para publicar la imagen               |
| `DOCKERHUB_TOKEN`               | Token de acceso a Docker Hub                                |
| `GITGUARDIAN_API_KEY`           | API key para realizar escaneos de seguridad con GitGuardian |


## Workflows disponibles

### 1. `ci-cd-terraform.yml`: provisión de infraestructura con Terraform

Se ejecuta cuando se **fusiona un pull request a `main`** que modifica archivos dentro de la carpeta `terraform/`.

Pasos principales:

- Autentica en Google Cloud utilizando el secreto `GCP_CREDENTIALS_JSON`.
- Establece variables de entorno necesarias para los recursos de Terraform (usando secretos de GitHub).
- Inicializa, valida, planifica y aplica automáticamente los cambios de infraestructura con Terraform.
- Espera que la instancia esté saludable.
- Lanza el flujo `init-prod-kv` para inicializar claves necesarias en el KV Store.


### 2. `ci-cd-deploy-instance.yml`: despliegue de la instancia de Kestra en GCP

Se ejecuta cuando se **fusiona un pull request a `main`** que modifica `kestra/docker-compose.yaml`.

Pasos principales:

- Crea un archivo `.env` con secretos y variables necesarias.
- Verifica que todas las variables estén definidas correctamente.
- Valida el archivo `docker-compose.yaml`.
- Copia los archivos necesarios a la instancia de GCP.
- Reinicia el entorno de ejecución Docker en GCP para aplicar cambios.


### 3. `ci-cd-deploy-flows.yml`: validación y despliegue de flujos Kestra

Se ejecuta cuando se **fusiona un pull request a `main`** que modifica archivos en `kestra/flows/**`.

Consta de tres jobs secuenciales:

#### `validate`
- Valida todos los flujos de `./kestra/flows` usando la acción oficial de Kestra.

#### `prod`
- Despliega los flujos a los namespaces:
  - `spotify-dwh-insights.prod`
  - `spotify-dwh-insights.ingestion`
  - `spotify-dwh-insights.transformation`
- Usa `delete: false` para evitar eliminar flujos existentes.

#### `run-init-kv`
- Espera que la instancia esté saludable.
- Lanza el flujo `init-prod-kv` para inicializar claves necesarias en el KV Store.


### 4. `ci-cd-build-deploy-docker-image.yml`: construir y publicar imagen Docker

Se ejecuta en cada **push a la rama `develop`** si se modifican:

- `dlt/dockerfile`
- `dlt/spotify_data_pipeline.py`

Pasos clave:

- Construye una imagen Docker con dos tags:
  - `latest`
  - `v<AAAAMMDD>` (con la fecha actual)
- Publica ambas imágenes a Docker Hub bajo `rj24/spotify-pipeline`.


### 5. `ci-sec-secrets-scan.yml`: escaneo de secretos sensibles

Este workflow se ejecuta en cada **push o pull request a ramas distintas de `main`**, para detectar posibles secretos expuestos en el código.

Pasos clave:

- Realiza checkout completo del repositorio (con historial).
- Ejecuta `ggshield` usando la acción oficial de **GitGuardian**.


### 6. `ci-qa-pre-commit.yml`: validación de estilo y calidad de código
Este workflow se ejecuta automáticamente en cada push o pull request a cualquier rama, y se encarga de aplicar validaciones automáticas de estilo y calidad sobre los archivos modificados.

Pasos clave:
- Realiza el checkout del código fuente.
- Instala Python y `pre-commit`, junto con dependencias del sistema necesarias (por ejemplo, para gitleaks).
- Compara los cambios entre el commit base y el commit actual:
  - En un pull request, compara contra la rama base.
  - En un push directo, compara con el commit anterior (HEAD^).
- Ejecuta los hooks configurados en `.pre-commit-config.yaml` (por ejemplo, `isort`, `black`, `gitleaks`, etc.).

Este workflow asegura que cualquier cambio subido al repositorio pase por validaciones automáticas antes de ser fusionado


## Estado de los Workflows CI/CD

| Descripción                         | Estado |
|------------------------------------|--------|
| Provisión de Infraestructura       | [![CI-CD-Terraform](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-terraform.yml/badge.svg)](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-terraform.yml) |
| Despliegue de Instancia Kestra     | [![CI-CD-Deploy-Kestra-Instance](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-deploy-instance.yml/badge.svg)](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-deploy-instance.yml) |
| Despliegue de Flujos Kestra        | [![CI-CD-Deploy-Kestra-Flows](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-deploy-flows.yml/badge.svg)](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-deploy-flows.yml) |
| Docker Build & Deploy              | [![CI-CD-Build-Deploy-Docker](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-build-deploy-docker-image.yml/badge.svg)](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-build-deploy-docker-image.yml) |
| Escaneo de Secretos         | [![CI-SEC-Secrets-Scan](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-sec-secrets-scan.yml/badge.svg)](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-sec-secrets-scan.yml) |
| Validación de Código         | [![Code Style & Quality](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-qa-pre-commit.yml/badge.svg)](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-qa-pre-commit.yml) |
