# ---------------------------------------------------------------------------------  # 
#                          　       AI Search ヘルパ                                   #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
from utils.azure import title_search_client, h2_search_client

# ----------------------------------
# 関連度の高いインデックスを取得
# ----------------------------------
def top_title_chunks(query: str, k: int = 5) -> list[dict]:
    results = title_search_client.search(
        search_text=query,
        query_type="semantic",
        semantic_configuration_name="default",
        select=["id", "title"],
        top=k,
    )
    return [r for r in results]

def top_h2_chunks(query: str, k: int = 5) -> list[dict]:
    results = h2_search_client.search(
        search_text=query,
        query_type="semantic",
        semantic_configuration_name="default",
        select=["id", "heading", "content"],
        top=k,
    )
    return [r for r in results]