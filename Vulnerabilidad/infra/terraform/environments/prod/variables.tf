variable "project_name" {
  type        = string
  description = "Nombre base del proyecto."
  default     = "anzencore" # Valor por defecto, puede ser sobreescrito
}

variable "environment" {
  type        = string
  description = "Ambiente de despliegue (ej. prod, dev)."
  default     = "prod" # Valor por defecto, puede ser sobreescrito
}

variable "location" {
  type        = string
  description = "Region de Azure para el despliegue."
  default     = "eastus" # Puedes cambiar a tu region preferida
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