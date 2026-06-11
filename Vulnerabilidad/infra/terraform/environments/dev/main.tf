terraform {
  required_version = ">= 1.6.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.116"
    }
  }

  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "tfstateanzencore"
    container_name       = "tfstate"
    key                  = "anzencore-dev.tfstate"
  }
}

provider "azurerm" {
  features {}
}

module "anzencore" {
  source = "../../modules/anzencore_container_apps"

  project_name    = var.project_name
  environment     = var.environment
  location        = var.location
  supabase_url    = var.supabase_url
  supabase_key    = var.supabase_key
  dashboard_image = var.dashboard_image
  api_image       = var.api_image
}
