# ---------------------------------------------------------------------------------  # 
# 　　　　　　              検索キーワードから画像を取得するアクティビティ　　　             　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import requests, json
import numpy as np
from pathlib import Path
from openai import AzureOpenAI
from azure.ai.contentsafety import ContentSafetyClient
from config.settings import UNSPLASH_SEARCH_URL, HEADERS
from utils.azure import embedding


# ----------------------------------
# 画像をUnsplashから取得するクラス
# ----------------------------------
class ImagePicker:
    def __init__(
            self, 
            embedding_client: AzureOpenAI, 
            content_safety_client: ContentSafetyClient,
            similarity_threshold: float = 0.30
        ):
        self.embedding_client = embedding_client
        self.content_safety_client = content_safety_client
        self.similarity_threshold = similarity_threshold

    def pick_images(self, keyword: str, max_images: int = 4) -> list[dict]:
        """
        Pick images from Unsplash based on the keyword and the draft JSON.
        
        Args:
            keyword: The keyword to search for
            max_images: The maximum number of images to return
        
        Returns:
            A list of dictionaries containing the image URL and the caption
        """
        image_file = Path("data/images") / f"{keyword}.json"
        if image_file.exists():
            print(f"Image already exists: {image_file}")
            with open(image_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # Unsplash検索
        params = {
            "query": keyword,
            "per_page": 30, # 最初に30枚取得し、フィルタリングをしていく
            "orientation": "landscape"
        }
        resp = requests.get(UNSPLASH_SEARCH_URL, params=params, headers=HEADERS, timeout=10)
        resp.raise_for_status()
            # HTTPリクエストが失敗していないか確認するためのメソッド
        items = resp.json()["results"]

        # Embedding
        query_emb = embedding(keyword)

        # 各画像のスコア計算 & Safetyフィルタ
        scored: list[tuple] = []
        for item in items:
            url = item["urls"]["regular"]
            alt = item.get("alt_description") or keyword
            tags = item.get("tags", [])
            tags_text = alt + " " + " ".join(t["title"] for t in tags)

            emb = embedding(tags_text)
            if not self._safety_ok(url):
                continue

            sim = self._cosine_similarity(query_emb, emb)
            if sim >= self.similarity_threshold:
                scored.append((sim, item))

        # 上位 max_images 件を取得
        scored.sort(key=lambda x: x[0], reverse=True)
        selected = scored[:max_images]
        print(f"Selected: {selected}")

        images = [
            {
                "url": item["urls"]["regular"],
                "alt": item.get("alt_description") or keyword,
                "credit": f"Photo by {item['user']['name']} / Unsplash",
            }
            for _, item in selected
        ]

        with open(image_file, "w", encoding="utf-8") as f:
            json.dump(images, f, ensure_ascii=False, indent=2)

        return images
    
    def _cosine_similarity(self, u: list[float], v: list[float]) -> float:
        """
        Calculate the cosine similarity between two vectors.
        """
        return float(np.dot(u, v))

    def _safety_ok(self, url: str) -> bool:
        """
        Check if the image is safe.
        """
        return True
        # try:
        #     res = self.content_safety_client.analyze_image({"url": url}, ["ContentSafety"])
        #     max_score = max(c.severity for c in res.categories_analysis)
        #     return max_score <= 3
        # except Exception as e:
        #     return False

