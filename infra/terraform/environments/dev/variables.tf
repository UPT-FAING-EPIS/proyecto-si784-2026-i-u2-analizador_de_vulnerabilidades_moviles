variable "project_name" {
  type    = string
  default = "anzencore"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "location" {
  type    = string
  default = "eastus"
}

variable "supabase_url" {
  type      = string
  sensitive = true
}

variable "supabase_key" {
  type      = string
  sensitive = true
}

variable "dashboard_image" {
  type    = string
  default = "mcr.microsoft.com/k8se/quickstart:latest"
}

variable "api_image" {
  type    = string
  default = "mcr.microsoft.com/k8se/quickstart:latest"
}
