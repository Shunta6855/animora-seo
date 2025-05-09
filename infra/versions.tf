# ---------------------------------------------------------------------------------  # 
#                          Terraform本体等のバージョンを制限する                          #
# ---------------------------------------------------------------------------------  #

# Terraform全体の基本設定
terraform {
  required_version = ">= 1.6"
  required_providers {
    # Azure Resource Manager Provider: Azureのリソースを管理するためのプロバイダ
    azurerm = {
        source = "hashicorp/azurerm"
        version = "~> 3.108" # 3.108.x を許容する
    }
    # Azure API Provider: プレビュー機能や未サポートのAzureリソースにアクセスするための補助プロバイダー
    azapi = {
        source = "azure/azapi"
        version = "~> 1.12"
    }
  }
  backend "azurerm" {
      resource_group_name = "rg-tfstate"
      storage_account_name = "sttfstate123"
      container_name = "terraform"
      key = "animora-seo.tfstate"
  }
}

# Azureに接続するための設定
provider "azurerm" {
  features {
    
  }
}

# バックエンドの作成は一度だけPortalか az cli で行う