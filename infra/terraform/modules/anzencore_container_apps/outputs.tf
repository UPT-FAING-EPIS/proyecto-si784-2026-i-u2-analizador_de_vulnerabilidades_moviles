output "resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "container_registry_login_server" {
  value = azurerm_container_registry.main.login_server
}

output "dashboard_url" {
  value = azurerm_container_app.dashboard.latest_revision_fqdn
}

output "api_url" {
  value = azurerm_container_app.api.latest_revision_fqdn
}
