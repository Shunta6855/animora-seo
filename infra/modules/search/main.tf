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

# インデックスの作成
resource "azapi_resource" "index" {
    type = "Microsoft.Search/searchServices/indexes@2023-11-01"
    name = "h2_components"
    parent_id = azurerm_search_service.this.id
    body = jsonencode({
        fields = [
            { name = "id", type = "Edm.String", key = true },
            { name = "heading", type = "Edm.String", searchable = true },
            { name = "content", type = "Edm.String", searchable = true, analyzer = "ja.microsoft" },
            { name = "vector", type = "Collection(Edm.Single)", vectorSearchDimensions = 1536, vectorSearchConfiguration = "default" }
        ]
        vectorSearch = { algorithmConfigurations = [{ name = "default", kind = "vector"}]}
    })
}