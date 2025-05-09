# ---------------------------------------------------------------------------------  # 
#                      Function AppのIDトークンを取得するための出力                       #
# ---------------------------------------------------------------------------------  #

# principal_id
output "principal_id" {
    value = azurerm_function_app.this.identity[0].principal_id
}

# client_id
output "client_id" {
    value = azurerm_function_app.this.identity[0].client_id
}