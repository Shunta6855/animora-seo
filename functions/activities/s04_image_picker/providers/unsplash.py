# ---------------------------------------------------------------------------------  # 
# 　　　　　　              検索キーワードから画像を取得するアクティビティ　　　             　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import requests
from .base import BaseProvider
from config.settings import UNSPLASH_SEARCH_URL, UNSPLASH_ACCESS_KEY

# ----------------------------------
# Unsplashクラス
# ----------------------------------
class Unsplash(BaseProvider):
    name = "Unsplash"

    def __init__(self):
        self.search_url = UNSPLASH_SEARCH_URL

    def search(self, query: str, limit: int) -> list[dict]:
        params = {
            "query": query,
            "per_page": limit,
            "orientation": "landscape"
        }
        headers = {
            "Accept-Version": "v1",
            "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
        }
        resp = requests.get(
            self.search_url, 
            params=params, 
            headers=headers, 
            timeout=10)
        resp.raise_for_status()
        results = resp.json().get("results", [])
        return [
            dict(
                url=item["urls"]["regular"],
                alt=item.get("alt_description") or query,
                credit=f"Photo by {item['user']['name']} / Unsplash"
            )
            for item in results
        ]