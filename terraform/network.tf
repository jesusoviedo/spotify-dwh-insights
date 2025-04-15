resource "google_compute_firewall" "allow_http" {
  name    = "allow-kestra"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8080", "8081", "9090"]
  }

  target_tags   = ["kestra"]
  source_ranges = ["0.0.0.0/0"]
  direction     = "INGRESS"
}
