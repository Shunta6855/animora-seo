# ---------------------------------------------------------------------------------  # 
#  検索上位記事のH2セクションをRAG用に Azure AI Search にインデックスとして保存するアクティビティ #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from functions.config.settings import (
    AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_KEY, INDEX_NAME
)


# ----------------------------------
# H2セクションをインデックスとして保存する関数
# ----------------------------------
def upload_documents(docs: list[dict]):
    client = SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=INDEX_NAME,
        credential=AzureKeyCredential(AZURE_SEARCH_KEY)
    )
    CHUNK_SIZE = 100
    for i in range(0, len(docs), CHUNK_SIZE):
        batch = docs[i:i+CHUNK_SIZE]
        result = client.upload_documents(documents=batch)
        if not all(r.succeeded for r in result):
            failed = [r.key for r in result if not r.succeeded]
            raise Exception(f"Failed to upload documents: {failed}")
        print(f"Uploaded {len(batch)} documents")

# animora docsをインデックスとして登録することも忘れず
    