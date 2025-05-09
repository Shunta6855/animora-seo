# ---------------------------------------------------------------------------------  # 
#                            Azure AI Search Serviceを作成する                         #
# ---------------------------------------------------------------------------------  #

# Search Service本体
resource "azurerm_search_service" "svc"{
    name = "${var.project_name}-search-${var.environment}"
    location = 
}