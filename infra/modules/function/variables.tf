# ---------------------------------------------------------------------------------  # 
#                                       変数の定義                                     #
# ---------------------------------------------------------------------------------  #

# プロジェクト名
variable "project_name" {
    description = "Name of the project"
    type = string
}

# Azureのリージョン(ex: japaneast)
variable "location" {
    description = "Azure region"
    type = string
}

# リソースグループ名
variable "resource_group_name" {
  description = "Resource group name"
  type        = string
} 

# Key Vaultの名前
variable "kv_name" {
  type = string
  description = "Key Vault name (used for Key Vault reference in app_settings)"
}

# Azure OpenAIのエンドポイント
variable "openai_endpoint" {
  type = string
}

# Azure AI Visionのエンドポイント
variable "vision_endpoint" {
  type = string
}

# Azure Bing Search Serviceのエンドポイント
variable "bing_endpoint" {
  type = string
}

# Azure AI Search Serviceのエンドポイント
variable "search_endpoint" {
  type = string
}
