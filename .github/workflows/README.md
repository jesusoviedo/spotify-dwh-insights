# 🔄 Integración y Despliegue Automático (`.github/workflows/`)

Este proyecto utiliza **GitHub Actions** para automatizar aspectos clave del ciclo de vida de desarrollo:

1. Despliegue de una instancia de **Kestra** en GCP.
2. Validación y despliegue de flujos de trabajo de Kestra.
3. Construcción y publicación de una imagen Docker a DockerHub cuando se modifican los archivos del pipeline.
4. Escaneo automático de secretos sensibles con GitGuardian.

---

## Secretos requeridos

Asegúrate de configurar los siguientes secretos en tu repositorio para que los workflows funcionen correctamente:

| Secreto                         | Descripción                                               |
|--------------------------------|-----------------------------------------------------------|
| `KESTRA_USER`                  | Usuario administrador de Kestra                          |
| `KESTRA_PASSWORD`              | Contraseña del usuario administrador                     |
| `KESTRA_HOSTNAME`              | Dirección IP o hostname donde corre Kestra               |
| `POSTGRES_DB`                  | Nombre de la base de datos PostgreSQL                    |
| `POSTGRES_USER`                | Usuario para la base de datos                            |
| `POSTGRES_PASSWORD`           | Contraseña para la base de datos                         |
| `SECRET_CLIENTE_ID_BASE64`     | Credencial codificada del cliente de Spotify             |
| `SECRET_CLIENTE_SECRET_BASE64` | Secreto codificado del cliente de Spotify                |
| `SECRET_PROJECT_ID_BASE64`     | ID del proyecto en GCP (codificado)                      |
| `SECRET_GCP_CREDENTIALS_BASE64`| Credenciales del servicio GCP (base64)                   |
| `GCP_CREDENTIALS_JSON`         | JSON de autenticación para el acceso a GCP               |
| `GCP_PROJECT_ID`               | ID del proyecto en GCP                                   |
| `GCP_INSTANCE_NAME`            | Nombre de la instancia de GCP                            |
| `GCP_ZONE`                     | Zona donde se encuentra la instancia                     |
| `DOCKER_USERNAME`              | Usuario de Docker Hub para publicar la imagen            |
| `DOCKERHUB_TOKEN`              | Token de acceso a Docker Hub                             |
| `GITGUARDIAN_API_KEY`          | API key para realizar escaneos de seguridad con GitGuardian |

---

## Workflows disponibles

### 1. `ci-cd-deploy-instance.yml`: despliegue de la instancia de Kestra en GCP

Se ejecuta cuando se **fusiona un pull request a `master`** que modifica `kestra/docker-compose.yaml`.

Pasos principales:

- Crea un archivo `.env` con secretos y variables necesarias.
- Verifica que todas las variables estén definidas correctamente.
- Valida el archivo `docker-compose.yaml`.
- Copia los archivos necesarios a la instancia de GCP.
- Reinicia el entorno de ejecución Docker en GCP para aplicar cambios.

---

### 2. `ci-cd-deploy-flows.yml`: validación y despliegue de flujos Kestra

Se ejecuta cuando se **fusiona un pull request a `master`** que modifica archivos en `kestra/flows/**`.

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

---

### 3. `ci-cd-build-deploy-docker-image.yml`: construir y publicar imagen Docker

Se ejecuta en cada **push a la rama `develop`** si se modifican:

- `dlt/dockerfile`
- `dlt/spotify_data_pipeline.py`

Pasos clave:

- Construye una imagen Docker con dos tags:
  - `latest`
  - `v<AAAAMMDD>` (con la fecha actual)
- Publica ambas imágenes a Docker Hub bajo `rj24/spotify-pipeline`.

---

### 4. `ci-sec-secrets-scan.yml`: escaneo de secretos sensibles

Este workflow se ejecuta en cada **push o pull request a ramas distintas de `master`**, para detectar posibles secretos expuestos en el código.

Pasos clave:

- Realiza checkout completo del repositorio (con historial).
- Ejecuta `ggshield` usando la acción oficial de **GitGuardian**.

---

## Estado de los Workflows CI/CD

| Descripción                     | Estado |
|--------------------------------|--------|
| Despliegue de Flujos Kestra    | [![CI-CD-Deploy-Kestra-Flows](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-deploy-flows.yml/badge.svg)](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-deploy-flows.yml) |
| Despliegue de Instancia Kestra | [![CI-CD-Deploy-Kestra-Instance](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-deploy-instance.yml/badge.svg)](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-deploy-instance.yml) |
| Docker Build & Deploy          | [![CI-CD-Build-Deploy-Docker](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-build-deploy-docker-image.yml/badge.svg)](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-cd-build-deploy-docker-image.yml) |
| Escaneo de Secretos (Dev)      | [![CI-SEC-Secrets-Scan](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-sec-secrets-scan.yml/badge.svg)](https://github.com/jesusoviedo/spotify-dwh-insights/actions/workflows/ci-sec-secrets-scan.yml) |

---
