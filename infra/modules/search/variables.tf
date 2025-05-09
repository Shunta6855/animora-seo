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

# Azure AI Search ServiceのSKU
variable "search_sku" {
    description = "Azure Cognitive Search pricing tier"
    type = string
    default = "basic"
}
