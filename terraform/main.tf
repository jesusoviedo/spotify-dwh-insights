terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~>6.8.0"
    }
  }

  backend "gcs" {
    bucket = "spotify-dwh-insights-terraform"
    prefix = "data-dev"
  }
}

provider "google" {
  #credentials = file("GOOGLE_APPLICATION_CREDENTIALS")
  project     = var.project
  region      = var.region
}


resource "google_storage_bucket" "spotify-gcs" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 20
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "spotify-dataset-raw" {
  dataset_id                  = var.bq_dataset_name
  project                     = var.project
  location                    = var.location
  default_table_expiration_ms = var.bq_table_expiration_ms
}