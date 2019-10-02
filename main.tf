terraform {
  backend "gcs" {
    bucket = "mazegen-tf-state"
    prefix = "terraform/state"
  }
}

data "archive_file" "app" {
  type        = "zip"
  source_dir  = "${path.root}/app/"
  output_path = "${path.root}/pkg/mazegen.zip"
}

provider "google" {
  project     = "${var.project}"
  region      = "${var.region}"
}

resource "google_storage_bucket" "application_bucket" {
  name = "application_bucket"
}

resource "google_storage_bucket_object" "application_package" {
  name    = "mazegen.zip"
  bucket  = "${google_storage_bucket.application_bucket.name}"
  source  = "${path.root}/pkg/mazegen.zip"
}

resource "google_cloudfunctions_function" "application_function" {
  name                  = "mazegen-function"
  description           = "Maze Generator"
  available_memory_mb   = 256
  source_archive_bucket = "${google_storage_bucket.application_bucket.name}"
  source_archive_object = "${google_storage_bucket_object.application_package.name}"
  timeout               = 120
  entry_point           = "entry"
  trigger_http          = true
  runtime               = "python37"
}
