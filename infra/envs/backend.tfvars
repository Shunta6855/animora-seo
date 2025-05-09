# ---------------------------------------------------------------------------------  # 
#                             リモートステートの保存先設定                                #
# ---------------------------------------------------------------------------------  #

# リモートステートの保存先
resource_group_name = "rg-${var.project_name}"
storage_account_name = "st${var.project_name}"
container_name = "tfstate"
key = "terraform.tfstate"