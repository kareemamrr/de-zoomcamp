variable "credentials" {
  description = "My credentials"
  default     = "./keys/my-creds.json"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_dataset_name" {
  description = "My Storage Bucket Name"
  default     = "terraform-demo-412211"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}