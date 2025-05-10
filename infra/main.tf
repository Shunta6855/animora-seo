# ---------------------------------------------------------------------------------  # 
#                              　　　   メイン処理                                      #
# ---------------------------------------------------------------------------------  #

# リソースグループの作成
module "rg" {
  source = "./modules/rg"
  project_name = var.project_name
  location = var.location
}

# Key Vaultの作成
module "keyvault" {
  source = "./modules/keyvault"
  project_name = var.project_name
  location = var.location
  resource_group_name = module.rg.name
  func_principal_id = module.function.principal_id
}

# Azure AI Serviceの作成
module "cognitive" {
  source = "./modules/cognitive"
  project_name = var.project_name
  location = var.location
  resource_group_name = module.rg.name
  key_vault_id = module.keyvault.id
  openai_sku = var.openai_sku
  vision_sku = var.vision_sku
  kv_access_policy_self = module.keyvault.access_policy_self
}

# Azure AI Search Serviceの作成
module "search" {
  source = "./modules/search"
  project_name = var.project_name
  location = var.location
  resource_group_name = module.rg.name
  search_sku = var.search_sku
  providers = {
    azurerm = azurerm
    azapi = azapi
  }
}

# Azure Function Appの作成
module "function" {
  source = "./modules/function"
  project_name = var.project_name
  location = var.location
  resource_group_name = module.rg.name
  kv_name = module.keyvault.name
  openai_endpoint = module.cognitive.openai_endpoint
  vision_endpoint = module.cognitive.vision_endpoint
  search_endpoint = module.search.search_endpoint
  depends_on = [ module.cognitive, module.search ]
}

# Application Insightsの作成
module "monitoring" {
  source = "./modules/monitoring"
  project_name = var.project_name
  location = var.location
  resource_group_name = module.rg.name
}