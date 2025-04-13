# ---------------------------------------------------------------------------------  # 
#                   キーワードに関する過去の指標データを取得する実行コード                    #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import os
import datetime
import json
import traceback
import pandas as pd

from time import sleep
from googleapiclient.discovery import build
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

DATA_DIR = "data"
today = datetime.date.today().strftime("%Y%m%d")

# ----------------------------------
# Google検索結果を取得する関数
# ----------------------------------
def get_search_response(keyword):
    """
    Get search response from Custom Search JSON API

    Args:
        keyword: The search keyword
    """
    timestamp = datetime.datetime.today().strftime("%Y%m%d %H:%M:%S")

    os.makedirs(DATA_DIR, exist_ok=True)

    service = build("customsearch", "v1", developerKey=os.getenv("GOOGLE_API_KEY"))

    # 上位10件の検索結果を取得
    try:
        sleep(1)
        response = service.cse().list(
            q=keyword,
            cx=os.getenv("CUSTOM_SEARCH_ENGINE_ID"),
            lr="lang_ja",
            num=10,
            start=1,
        ).execute()
    except Exception as e:
        print(f"Error occurred: {e}")
        traceback.print_exc()
        return []
    
    # 検索結果をJSON形式で保存
    save_response_dir = os.path.join(DATA_DIR, "response")
    os.makedirs(save_response_dir, exist_ok=True)
    out = {
        "snapshot_ymd": today,
        "snapshot_timestamp": timestamp,
        "response": [],
    }
    out["response"] = response
    jsonstr = json.dumps(out, ensure_ascii=False)
    with open(os.path.join(save_response_dir, f"{keyword}_" + today + ".json"), "w", encoding="utf-8") as f:
        f.write(jsonstr)

# ----------------------------------
# Google検索結果をtsv形式にして保存する関数
# ----------------------------------
def make_search_results(keyword):
    """
    Save Google search results to TSV format
    """
    response_filename = os.path.join(DATA_DIR, "response", f"{keyword}_" + today + ".json")
    with open(response_filename, "r") as response_file:
        response_tmp = json.load(response_file)
    ymd = response_tmp["snapshot_ymd"]
    response = response_tmp["response"]
    results = []
    cnt = 0
    if "items" in response and len(response["items"]) > 0:
        for item in response["items"]:
            cnt += 1
            display_link = item.get("displayLink", "")
            title = item.get("title", "")
            link = item.get("link", "")
            snippet = item.get("snippet", "").replace("\n", "")
            results.append({
                "ymd": ymd,
                "no": cnt,
                "display_link": display_link,
                "title": title,
                "link": link,
                "snippet": snippet,
            })
    save_results_dir = os.path.join(DATA_DIR, "result_dfs")
    os.makedirs(save_results_dir, exist_ok=True)
    df_results = pd.DataFrame(results)
    df_results.to_csv(
        os.path.join(save_results_dir, f"{keyword}_" + today + ".tsv"), 
        sep="\t", index=False,
        columns=["ymd", "no", "display_link", "title", "link", "snippet"],
    )

if __name__ == "__main__":
    keyword = "ペットSNS"
    get_search_response(keyword)
    make_search_results(keyword)

