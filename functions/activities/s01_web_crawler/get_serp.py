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
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False)
        return save_path











# # Google検索結果を取得する関数
# # ----------------------------------
# def get_search_response(keyword):
#     """
#     Get search response from Custom Search JSON API

#     Args:
#         keyword: The search keyword
#     """
#     print(f"Start getting search response for keyword: {keyword}")
#     timestamp = datetime.datetime.today().strftime("%Y%m%d %H:%M:%S")

#     os.makedirs(DATA_DIR, exist_ok=True)

#     service = build("customsearch", "v1", developerKey=os.getenv("GOOGLE_API_KEY"))

#     # 上位10件の検索結果を取得
#     try:
#         sleep(1)
#         response = service.cse().list(
#             q=keyword,
#             cx=os.getenv("CUSTOM_SEARCH_ENGINE_ID"),
#             lr="lang_ja",
#             num=10,
#             start=1,
#         ).execute()
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         traceback.print_exc()
#         return []
    
#     # 検索結果をJSON形式で保存
#     save_response_dir = os.path.join(DATA_DIR, "response")
#     os.makedirs(save_response_dir, exist_ok=True)
#     out = {
#         "snapshot_ymd": today,
#         "snapshot_timestamp": timestamp,
#         "response": [],
#     }
#     out["response"] = response
#     jsonstr = json.dumps(out, ensure_ascii=False)
#     with open(os.path.join(save_response_dir, f"{keyword}_" + "response" + ".json"), "w", encoding="utf-8") as f:
#         f.write(jsonstr)

# # ----------------------------------
# # Google検索結果をtsv形式にして保存する関数
# # ----------------------------------
# def make_search_results(keyword):
#     """
#     Save Google search results to TSV format
#     """
#     response_filename = os.path.join(DATA_DIR, "response", f"{keyword}_" + "response" + ".json")
#     with open(response_filename, "r") as response_file:
#         response_tmp = json.load(response_file)
#     ymd = response_tmp["snapshot_ymd"]
#     response = response_tmp["response"]
#     results = []
#     cnt = 0
#     if "items" in response and len(response["items"]) > 0:
#         for item in response["items"]:
#             cnt += 1
#             display_link = item.get("displayLink", "")
#             title = item.get("title", "")
#             link = item.get("link", "")
#             snippet = item.get("snippet", "").replace("\n", "")
#             results.append({
#                 "ymd": ymd,
#                 "no": cnt,
#                 "display_link": display_link,
#                 "title": title,
#                 "link": link,
#                 "snippet": snippet,
#             })
#     save_results_dir = os.path.join(DATA_DIR, "result_dfs")
#     os.makedirs(save_results_dir, exist_ok=True)
#     df_results = pd.DataFrame(results)
#     df_results.to_csv(
#         os.path.join(save_results_dir, f"{keyword}_" + "response" + ".tsv"), 
#         sep="\t", index=False,
#         columns=["ymd", "no", "display_link", "title", "link", "snippet"],
#     )

# if __name__ == "__main__":
#     keyword = "ペットSNS"
#     get_search_response(keyword)
#     make_search_results(keyword)

