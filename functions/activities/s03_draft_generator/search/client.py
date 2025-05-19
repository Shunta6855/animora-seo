# ---------------------------------------------------------------------------------  # 
#                          　       AI Search ヘルパ                                   #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from functions.config.settings import (
    AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_KEY, H2_INDEX_NAME
)

client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=H2_INDEX_NAME,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)

# ----------------------------------
# 関連度の高いインデックスを取得
# ----------------------------------
def top_chunks(query: str, k: int = 5) -> list[dict]:
    results = client.search(
        search_text=query,
        query_type="semantic",
        select=["id", "heading", "content"],
        top=k,
    )
    return [r for r in results]