# ---------------------------------------------------------------------------------  # 
#                            Azure上にリソースグループを作成する                          #
# ---------------------------------------------------------------------------------  #

# リソースの定義
resource "azurerm_resource_group" "this" {
    name = "${var.project_name}-rg"
    location = var.location
}
    # azurerm_resource_group: Terraformプロバイダのリソースタイプの1つ
    # this: このリソースにTerraform内部でアクセスする際の名前
        # 他のリソースで参照する場合はazurerm_resource_group.thisと書く


