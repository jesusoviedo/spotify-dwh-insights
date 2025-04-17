## Main
variable "project" {
  description = "Project"
  default     = "spotify-dwh-insights"
}

variable "region" {
  description = "Region"
  default     = "us-east1"
}

variable "zone" {
  description = "Zona"
  default     = "us-east1-b"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}


## GCS
variable "gcs_bucket_name" {
  description = "My bucket name"
  default     = "spotify-dwh-insights-music-info"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}


## Bigquery
variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "spotify_raw_data"
}

variable "bq_table_expiration_ms" {
  description = "Default table expiration"
  default     = 2592000000
}


##
variable "secret_cliente_id" {}

variable "secret_cliente_secret" {}

variable "secret_project_id" {}

variable "secret_gcp_credentials" {}

variable "postgres_db" {}

variable "postgres_user" {}

variable "postgres_password" {}

variable "kestra_user" {}

variable "kestra_password" {}
