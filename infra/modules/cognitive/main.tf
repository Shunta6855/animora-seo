# ---------------------------------------------------------------------------------  # 
#                  Azure AI Serviceの利用(openai, vision, bing serach)                  #
# ---------------------------------------------------------------------------------  #

# Azure OpenAI(GPT-4o, Embedding)
resource "azurerm_cognitive_account" "openai" {
    name = "${var.project_name}-openai"
    location = var.location
    resource_group_name = var.resource_group_name
    kind = "OpenAI"
    sku_name = var.openai_sku
}

# Azure AI Vision(タグ + NSFW)
resource "azurerm_cognitive_account" "vision" {
    name = "${var.project_name}-vision"
    location = var.location
    resource_group_name = var.resource_group_name
    kind = "ComputerVision"
    sku_name = var.vision_sku
}

# Azure Bing Search(Bing Web Search)
resource "azurerm_cognitive_account" "search" {
    name = "${var.project_name}-search"
    location = var.location
    resource_group_name = var.resource_group_name
    kind = "Bing.Search.v7"
    sku_name = var.bing_sku
}

# Azure OpenAIのAPIキーをKey Vaultに保存
resource "azurerm_key_vault_secret" "openai_key" {
    name = "${var.project_name}-openai-key"
    value = azurerm_cognitive_account.openai.primary_access_key
    key_vault_id = var.key_vault_id
}

# Azure AI VisionのAPIキーをKey Vaultに保存
resource "azurerm_key_vault_secret" "vision_key" {
    name = "${var.project_name}-vision-key"
    value = azurerm_cognitive_account.vision.primary_access_key
    key_vault_id = var.key_vault_id
}

# Azure Bing SearchのAPIキーをKey Vaultに保存
resource "azurerm_key_vault_secret" "search_key" {
    name = "${var.project_name}-search-key"
    value = azurerm_cognitive_account.search.primary_access_key
    key_vault_id = var.key_vault_id
}
