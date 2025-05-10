# ---------------------------------------------------------------------------------  # 
#                            Azure AI Serviceの変数の定義                              #
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

# Azure OpenAIのSKU
variable "openai_sku" {
    description = "Azure OpenAI SKU (S0 supports GPT-4o)"
    type = string
    default = "S0"
}

# Azure AI Vision(タグ + NSFW)
variable "vision_sku" {
    description = "Azure AI Vision pricing tier"
    type = string
    default = "S1"
}


# Azure Key VaultのID
variable "key_vault_id" {
    description = "Azure Key Vault ID"
    type = string
}

# Key Vaultのアクセスポリシー(self)
variable "kv_access_policy_self" {
    description = "Access policy for the Key Vault"
    type = object({
        id = string
        tenant_id = string
        object_id = string
        application_id = string
        secret_permissions = list(string)
    })
}