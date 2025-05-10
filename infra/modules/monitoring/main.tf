# ---------------------------------------------------------------------------------  # 
#                     Application Insightsの利用(Azure Monitor)                      #
# ---------------------------------------------------------------------------------  #

# Log Analytics Workspaceの作成
resource "azurerm_log_analytics_workspace" "law" {
    name = "${var.project_name}-law"
    location = var.location
    resource_group_name = var.resource_group_name
    sku                 = "PerGB2018"
    retention_in_days   = 30  # ログの保存期間
}

# Application Insightsの作成
resource "azurerm_application_insights" "this" {
    name = "${var.project_name}-appinsights"
    location = var.location
    resource_group_name = var.resource_group_name
    application_type = "web"
    workspace_id = azurerm_log_analytics_workspace.law.id
}

