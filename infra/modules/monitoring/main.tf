# ---------------------------------------------------------------------------------  # 
#                     Application Insightsの利用(Azure Monitor)                      #
# ---------------------------------------------------------------------------------  #

# Application Insightsの作成
resource "azurerm_application_insights" "this" {
    name = "${var.project_name}-appinsights"
    location = var.location
    resource_group_name = var.resource_group_name
    application_type = "web"
}

