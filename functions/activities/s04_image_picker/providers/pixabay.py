# ---------------------------------------------------------------------------------  # 
# 　　　　　　              検索キーワードから画像を取得するアクティビティ　　　             　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import requests
from .base import BaseProvider
from config.settings import PIXABAY_API_KEY, PIXABAY_SEARCH_URL

# ----------------------------------
# Pixabayクラス
# ----------------------------------
class Pixabay(BaseProvider):
    name = "Pixabay"

    def __init__(self):
        self.search_url = PIXABAY_SEARCH_URL

    def search(self, query: str, limit: int) -> list[dict]:
        params = {
            "key": PIXABAY_API_KEY,
            "q": query,
            "image_type": "photo",
            "per_page": limit,
        }
        resp = requests.get(
            self.search_url, 
            params=params, 
            timeout=10)
        resp.raise_for_status()
        results = resp.json().get("hits", [])
        return [
            dict(
                url=item["largeImageURL"],
                alt=item.get("tags") or query,
                credit=f"Pixabay License (CC0)"
            )
            for item in results
        ]