# ---------------------------------------------------------------------------------  # 
#                          Terraform本体等のバージョンを制限する                          #
# ---------------------------------------------------------------------------------  #

# Terraform全体の基本設定
terraform {
  required_version = ">= 1.1.0"
  required_providers {
    # Azure Resource Manager Provider: Azureのリソースを管理するためのプロバイダ
    azurerm = {
        source = "hashicorp/azurerm"
        version = "~> 4.0.0" # 4.0.0〜4.999.x を許容
    }
    # Azure API Provider: プレビュー機能や未サポートのAzureリソースにアクセスするための補助プロバイダー
    azapi = {
        source = "azure/azapi"
        version = "~> 2.0.0"
    }
  }
  backend "azurerm" {
      resource_group_name = "rg-tfstate-animora-seo"
      storage_account_name = "sttfstateanimoraseo"
      container_name = "tfstate"
      key = "animora-seo.tfstate"
  }
}

# Azureに接続するための設定
provider "azurerm" {
  features {}
}

# バックエンドの作成は一度だけPortalか az cli で行う