# ---------------------------------------------------------------------------------  # 
#                       機密情報をAzure Key Vaultを用いて管理する                         #
# ---------------------------------------------------------------------------------  #

# テナントIDを取得
data "azurerm_client_config" "current" {}
    # 現在ログインしているAzureアカウントのテナントIDを取得させるためのデータソース

# Key Vault の作成
resource "azurerm_key_vault" "this" {
    name = "${var.project_name}-kv"
    location = var.location
    resource_group_name = var.resource_group_name
    sku_name = "standard"
    tenant_id =  data.azurerm_client_config.current.tenant_id
    purge_protection_enabled = true
    soft_delete_retention_days = 7
}

# Terraform 実行者(Azure CLIアプリケーション)にもアクセスを許可
resource "azurerm_key_vault_access_policy" "self" {
    key_vault_id = azurerm_key_vault.this.id
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id
    application_id = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
    secret_permissions = ["Get", "List", "Set", "Delete", "Recover", "Purge"]
}

# Function Appの MSI を access-policy に追加する
resource "azurerm_key_vault_access_policy" "func" {
    key_vault_id = azurerm_key_vault.this.id
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = var.func_principal_id # module.function.principal_id
    secret_permissions = ["Get", "List", "Set", "Delete"]
}