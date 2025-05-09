# ---------------------------------------------------------------------------------  # 
#                    記事生成フローを自動実行するDurable Functionの定義                    #
# ---------------------------------------------------------------------------------  #

# Storage Accountの作成
resource "azurerm_storage_account" "sa" {
    name = "${var.project_name}-storage"
    location = var.location
    resource_group_name = var.resource_group_name
    account_tier = "Standard"
    account_replication_type = "LRS" # ローカル冗長(コスト安・開発向け)

    public_network_access_enabled = false
    https_traffic_only_enabled = true

    min_tls_version = "TLS1_2"
    tags = {
        project = var.project_name
    }
}

# Function Appの実行基盤
resource "azurerm_service_plan" "plan" {
    name = "${var.project_name}-plan"
    location = var.location
    resource_group_name = var.resource_group_name
    os_type = "Linux"
    sku_name = "Y1" # Consumption (従量課金)
    kind = "FunctionApp"
}

# Function Appの作成
resource "azurerm_function_app" "this" {
    name = "${var.project_name}-func"
    location = var.location
    resource_group_name = var.resource_group_name
    app_service_plan_id = azurerm_service_plan.plan.id
    storage_account_name = azurerm_storage_account.sa.name
    storage_account_access_key = azurerm_storage_account.sa.primary_access_key
    app_settings = {
        FUNCTIONS_WORKER_RUNTIME = "python"
        WEBSITE_RUN_FROM_PACKAGE = "1"
        OPENAI_ENDPOINT = var.openai_endpoint
        OPENAI_API_KEY = "Microsoft.KeyVault(VaultName=)${var.kv_name};SecretName=AZURE_OPENAI-KEY"
        VISION_ENDPOINT = var.vision_endpoint
        VISION_API_KEY = "Microsoft.KeyVault(VaultName=)${var.kv_name};SecretName=AZURE_VISION-KEY"
        BING_ENDPOINT = var.bing_endpoint
        BING_API_KEY = "Microsoft.KeyVault(VaultName=)${var.kv_name};SecretName=AZURE_BING-KEY"
        SEARCH_ENDPOINT = var.search_endpoint
        SEARCH_API_KEY = "Microsoft.KeyVault(VaultName=)${var.kv_name};SecretName=AZURE_SEARCH-KEY"
    }
    identity {
      type = "SystemAssigned"
    }
}
