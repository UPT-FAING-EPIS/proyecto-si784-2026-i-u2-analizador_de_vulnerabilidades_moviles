variable "project_name" {
  type        = string
  description = "Nombre base del proyecto."
}

variable "environment" {
  type        = string
  description = "Ambiente de despliegue."
}

variable "location" {
  type        = string
  description = "Region de Azure."
}

variable "supabase_url" {
  type        = string
  sensitive   = true
  description = "URL del proyecto Supabase."
}

variable "supabase_key" {
  type        = string
  sensitive   = true
  description = "Anon key de Supabase."
}

variable "dashboard_image" {
  type        = string
  description = "Imagen Docker del dashboard."
}

variable "api_image" {
  type        = string
  description = "Imagen Docker de la API."
}
