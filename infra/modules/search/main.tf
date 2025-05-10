# ---------------------------------------------------------------------------------  # 
#                            Azure AI Search Serviceを作成する                         #
# ---------------------------------------------------------------------------------  #

# Search Service本体
resource "azurerm_search_service" "this" {
    name = "${var.project_name}-search"
    location = var.location
    resource_group_name = var.resource_group_name
    sku = var.search_sku
    replica_count = 1
    partition_count = 1
}