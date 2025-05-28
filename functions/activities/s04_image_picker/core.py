# ---------------------------------------------------------------------------------  # 
# 　　　　　　              検索キーワードから画像を取得するアクティビティ　　　             　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
from pathlib import Path
import json
from .utils.query import preprocess_query
from .utils.similarity import get_embedding
from .providers import get_all_providers


# ----------------------------------
# 画像検索コアクラス
# ----------------------------------
class ImagePicker:
    def __init__(self, similarity_threshold: float = 0.30):
        self.providers = get_all_providers()
        self.similarity_threshold = similarity_threshold
        self.cache_dir = Path("data/images")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def pick_images(self, keyword: str, max_images: int = 4):
        cache_path = self.cache_dir / f"{keyword}.json"
        if cache_path.exists():
            print(f"Image already exists: {cache_path}")
            print(f"Skipping ac_pick_images process")
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        
        queries = preprocess_query(keyword)
        query_emb = get_embedding(keyword)
        
        all_images = []
        for provider in self.providers:
            try:
                images = provider.search_with_filter(queries, query_emb, max_images, self.similarity_threshold)
                all_images.extend(images)
                print(f"[{provider.name}] Found {len(images)} images")
            except Exception as e:
                print(f"[{provider.name}] Error: {e}")

        if not all_images:
            print(f"No images found for keyword: {keyword}")
            return []

        all_images.sort(key=lambda x: x[0], reverse=True)
        top_images = [item for _, item in all_images[:max_images]]
        
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(top_images, f, ensure_ascii=False, indent=2)

        return top_images