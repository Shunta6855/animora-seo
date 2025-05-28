# ---------------------------------------------------------------------------------  # 
# 　　　　　　              検索キーワードから画像を取得するアクティビティ　　　             　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import requests
from .base import BaseProvider
from config.settings import PEXEL_SEARCH_URL, PEXEL_API_KEY

# ----------------------------------
# Pexelsクラス
# ----------------------------------
class Pexels(BaseProvider):
    name = "Pexels"

    def __init__(self):
        self.search_url = PEXEL_SEARCH_URL
        
    def search(self, query: str, limit: int) -> list[dict]:
        params = {
            "query": query,
            "per_page": limit,
            "orientation": "landscape"
        }
        headers = {
            "Authorization": PEXEL_API_KEY
        }
        resp = requests.get(
            self.search_url, 
            params=params, 
            headers=headers, 
            timeout=10)
        resp.raise_for_status()
        results = resp.json()["photos"]
        return [
            dict(
                url=item["src"]["large"],
                alt=item.get("alt") or query,
                credit=f"Photo by {item['photographer']} / Pexels"
            )
            for item in results
        ]