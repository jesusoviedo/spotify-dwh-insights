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
  project = var.project
  region  = var.region
}