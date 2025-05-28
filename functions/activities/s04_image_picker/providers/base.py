# ---------------------------------------------------------------------------------  # 
# 　　　　　　              検索キーワードから画像を取得するアクティビティ　　　             　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
from abc import ABC, abstractmethod
from ..utils.similarity import get_embedding, cosine_similarity


# ----------------------------------
# 画像検索プロバイダの基底クラス
# ----------------------------------
class BaseProvider(ABC):
    name: str

    @abstractmethod
    def search(self, query: str, limit: int) -> list[dict]:
        pass

    def search_with_filter(self, queries, query_emb, max_images, threshold) -> list[tuple[float, dict]]:
        """
        Search images and return filtered results.
        """
        results = []
        for q in queries:
            items = self.search(q, 30)
            for item in items:
                emb = get_embedding(item["alt"])
                similarity = cosine_similarity(query_emb, emb)
                if similarity >= threshold:
                    results.append((similarity, item))
            if len(results) >= max_images:
                break
        return results