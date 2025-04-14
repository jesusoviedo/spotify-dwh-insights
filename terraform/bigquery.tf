resource "google_bigquery_dataset" "spotify-dataset-raw" {
  dataset_id                  = var.bq_dataset_name
  project                     = var.project
  location                    = var.location
  default_table_expiration_ms = var.bq_table_expiration_ms
}
