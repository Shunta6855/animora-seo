# ---------------------------------------------------------------------------------  # 
#          　　  　      SERP上位10記事の情報を取得するアクティビティ  　    　              #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import os, json, traceback
from pathlib import Path
from time import sleep
from typing import Any
from googleapiclient.discovery import build
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# ----------------------------------
# Google の検索結果を取得し保存するクラス
# ----------------------------------
class GoogleSearcher:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.engine_id = os.getenv("CUSTOM_SEARCH_ENGINE_ID")
        self.service = build("customsearch", "v1", developerKey=self.api_key)
        self.data_dir = Path("data")
        self.response_dir = self.data_dir / "response"
        self.response_dir.mkdir(parents=True, exist_ok=True)

    def fetch(self, keyword: str) -> dict[str, Any]:
        """
        Perform Google search via Custom Search API

        Args:
            keyword: The search keyword

        Returns:
            Search results in JSON format
        """
        save_path = self.response_dir / f"{keyword}_response.json"
        if save_path.exists():
            print(f"SERP response already exists")
            print(f"Skipping ac_get_serp process")
            print(f"Loading cached response from {save_path}")
            with open(save_path, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # 上位10件の検索結果を取得
        try:
            sleep(1)
            response = self.service.cse().list(
                q=keyword,
                cx=self.engine_id,
                lr="lang_ja",
                num=10,
                start=1,
            ).execute()

        except Exception as e:
            print(f"Error occurred: {e}")
            traceback.print_exc()
            return []
        
        return response

    def save(self, keyword: str, response: dict[str, Any]):
        """
        Save response to JSON file

        Args:
            keyword: The search keyword
            response: The search results
        """
        save_path = self.response_dir / f"{keyword}_response.json"
        if save_path.exists():
            print(f"File already exists: {save_path}")
            return save_path

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False)
        return save_path








