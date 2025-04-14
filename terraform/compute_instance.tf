resource "google_compute_instance" "kestra_vm" {
  name         = "kestra-instance"
  machine_type = "e2-medium"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  tags = ["kestra"]

  metadata_startup_script = <<-EOF
    #!/bin/bash

    # Instala Docker y herramientas necesarias
    apt-get update
    apt-get install -y docker.io docker-compose git

    # Accede a secretos desde Google Secret Manager (codificados en Base64)
    export SECRET_CLIENTE_ID="${var.secret_cliente_id}"
    export SECRET_CLIENTE_SECRET="${var.secret_cliente_secret}"
    export SECRET_PROJECT_ID="${var.secret_project_id}"
    export SECRET_GCP_CREDENTIALS="${var.secret_gcp_credentials}"

    export KESTRA_USER="${var.kestra_user}"
    export KESTRA_PASSWORD="${var.kestra_password}"

    export POSTGRES_DB="${var.postgres_db}"
    export POSTGRES_USER="${var.postgres_user}"
    export POSTGRES_PASSWORD="${var.postgres_password}"

    # Clona el repositorio
    cd /opt
    git clone https://github.com/jesusoviedo/spotify-dwh-insights.git

    # Mueve la carpeta de Kestra al lugar deseado
    cd spotify-dwh-insights
    cp -r kestra ../kestra
    cd ..
    rm -rf spotify-dwh-insights
    cd kestra

    # Inicia los servicios de Docker Compose en segundo plano
    docker-compose up -d
  EOF



}