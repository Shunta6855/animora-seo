# ---------------------------------------------------------------------------------  # 
#                                   Key Vaultの出力                                   #
# ---------------------------------------------------------------------------------  #

output "id" {
    value = azurerm_key_vault.this.id
}

output "name" {
    value = azurerm_key_vault.this.name
}

output "access_policy_self" {
    value = azurerm_key_vault_access_policy.self
}

output "access_policy_func" {
    value = azurerm_key_vault_access_policy.func
}