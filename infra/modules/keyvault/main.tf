# ---------------------------------------------------------------------------------  # 
#                       機密情報をAzure Key Vaultを用いて管理する                         #
# ---------------------------------------------------------------------------------  #

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

# Function Appの MSI を access-policy に追加する
resource "azurerm_key_vault_access_policy" "func" {
    key_vault_id = azurerm_key_vault.this.id
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = var.func_principal_id # module.function.principal_id
    secret_permissions = ["Get", "List"]
}