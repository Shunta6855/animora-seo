# ---------------------------------------------------------------------------------  # 
#                                Azure AI Search Serviceの出力                                #
# ---------------------------------------------------------------------------------  #

output "search_endpoint" {
    description = "Endpoint URL of Azure AI Search Service"
    value = "https://${azurerm_search_service.this.name}.search.windows.net"
}

