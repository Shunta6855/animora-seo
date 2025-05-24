# ---------------------------------------------------------------------------------  # 
#  検索上位記事のH2セクションをRAG用に Azure AI Search にインデックスとして保存するアクティビティ #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
from azure.search.documents import SearchClient
from config.settings import animora_doc


# ----------------------------------
# H2セクション・Animora docs をインデックスとして保存するクラス
# ----------------------------------
class SearchUploader:
    def __init__(self, client: SearchClient):
        self.client = client
        self.chunk_size = 100

    def upload_h2_docs(self, docs: list[dict]):
        """
        Upload H2 docs to Azure AI Search

        Args:
            docs (list[dict]): List of H2 docs to upload
        """
        for i in range(0, len(docs), self.chunk_size):
            batch = docs[i:i+self.chunk_size]
            result = self.client.upload_documents(documents=batch)
            if not all(r.succeeded for r in result):
                failed = [r.key for r in result if not r.succeeded]
                raise Exception(f"Failed to upload documents: {failed}")
            print(f"Uploaded {len(batch)} documents")
            
    def upload_animora_docs(self):
        """
        Upload Animora docs to Azure AI Search

        Args:
            docs (list[dict]): List of Animora docs to upload
        """
        result = self.client.upload_documents(documents=animora_doc)
        if not all(r.succeeded for r in result):
            failed_keys = [r.key for r in result if not r.succeeded]
            raise Exception(f"Failed to upload animora docs: {failed_keys}")
        print(f"Uploaded {len(result)} animora docs")

    