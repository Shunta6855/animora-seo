# ---------------------------------------------------------------------------------  # 
#                                   Cognitiveの出力                                   #
# ---------------------------------------------------------------------------------  #

output "openai_endpoint" {
    value = azurerm_cognitive_account.openai.endpoint
}

output "vision_endpoint" {
    value = azurerm_cognitive_account.vision.endpoint
}


