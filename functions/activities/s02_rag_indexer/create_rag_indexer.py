# ---------------------------------------------------------------------------------  # 
#  検索上位記事のH2セクションをRAG用に Azure AI Search にインデックスとして保存するアクティビティ #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import re, json, hashlib
from pathlib import Path
from azure.search.documents import SearchClient, IndexDocumentsBatch
from config.settings import animora_doc

# ----------------------------------
# ハッシュ生成関数(ID生成用)
# ----------------------------------
def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u3000", " ")).strip().lower()

def doc_id_for_title(title: str) -> str:
    return hashlib.sha256(normalize(title).encode()).hexdigest()[:32]

def doc_id_for_h2(h2: str) -> str:
    return hashlib.sha256(normalize(h2).encode()).hexdigest()[:32]


# ----------------------------------
# H2セクション・Animora docs をインデックスとして保存するクラス
# ----------------------------------
class SearchUploader:
    def __init__(self, client: SearchClient, cache_path: Path):
        self.client = client
        self.chunk_size = 100
        self.cache_path = cache_path
        self.uploaded_ids = self._load_uploaded_ids()

    def _load_uploaded_ids(self) -> set[str]:
        if self.cache_path.exists():
            return set(json.loads(self.cache_path.read_text()))
        return set()

    def _save_uploaded_ids(self):
        self.cache_path.write_text(json.dumps(list(self.uploaded_ids), ensure_ascii=False))

    def _upload_filtered_docs(self, docs: list[dict]):
        new_docs = [d for d in docs if d["id"] not in self.uploaded_ids]
        if not new_docs:
            print("All documents already uploaded")
            return

        for i in range(0, len(new_docs), self.chunk_size):
            batch_docs = new_docs[i:i+self.chunk_size]
            batch = IndexDocumentsBatch()
            for d in batch_docs:
                batch.add_upload_actions([d])
            result = self.client.index_documents(batch)
            success_ids = [r.key for r in result if r.succeeded]
            self.uploaded_ids.update(success_ids)
            print(f"Uploaded {len(success_ids)} documents")

        self._save_uploaded_ids()
            
    def upload_titles(self, titles: list[dict]):
        docs = [
            {**t, "id": doc_id_for_title(t["title"])}
            for t in titles
        ]
        self._upload_filtered_docs(docs)

    def upload_h2_docs(self, raw_docs: list[dict]):
        docs = [
            {**d, "id": doc_id_for_h2(d["heading"])}
            for d in raw_docs
        ]
        self._upload_filtered_docs(docs)

    def upload_animora_docs(self):
        docs = [
            {**d, "id": doc_id_for_h2(d["heading"])}
            for d in animora_doc
        ]
        self._upload_filtered_docs(docs)


    