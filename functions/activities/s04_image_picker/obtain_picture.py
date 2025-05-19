# ---------------------------------------------------------------------------------  # 
# 　　　　　　              検索キーワードから画像を取得するアクティビティ　　　             　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import os, requests, asyncio, aiohttp, math
import numpy as np
from openai import AzureOpenAI
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from functions.config.settings import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    TEXT_EMBEDDING_DEPLOYMENT_NAME,
    AZURE_VISION_ENDPOINT,
    AZURE_VISION_KEY,
    UNSPLASH_ACCESS_KEY,
)
from functions.utils.azure import _embedding

# ----------------------------------
# クライアントの初期化
# ----------------------------------
embedding_client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=TEXT_EMBEDDING_DEPLOYMENT_NAME
)
vision_client = ContentSafetyClient(
    endpoint=AZURE_VISION_ENDPOINT,
    credential=AzureKeyCredential(AZURE_VISION_KEY)
)
UNSPLASH_SEARCH_URL = "https://api.unsplash.com/search/photos"
HEADERS = {
    "Accept-Version": "v1",
    "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
}

# ----------------------------------
# コサイン類似度を計算する関数
# ----------------------------------
def _cosine_similarity(u: list[float], v: list[float]) -> float:
    return float(np.dot(u, v))


# ----------------------------------
# 画像の安全性チェックをする関数
# ----------------------------------
async def _safety_ok(url: str) -> bool:
    try:
        res = vision_client.analyze_image({"url": url}, ["ContentSafety"])
        max_score = max(c.severity for c in res.categories_analysis)
        return max_score <= 3
    except Exception as e:
        return False

# ----------------------------------
# 画像をUnsplashから取得する関数
# ----------------------------------
async def pick_images(keyword: str, draft_json: dict, max_images: int = 4) -> list[dict]:
    """
    Pick images from Unsplash based on the keyword and the draft JSON.
    
    Args:
        keyword: The keyword to search for
        draft_json: The draft JSON
        max_images: The maximum number of images to return
    
    Returns:
        A list of dictionaries containing the image URL and the caption
    """
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
    query_emb = await _embedding(keyword)

    # 各画像のスコア計算 & Safetyフィルタ
    scored: list[tuple] = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for item in items:
            url = item["url"]["regular"]
            alt = item.get("alt_description") or keyword
            tags_text = alt + " " + " ".join(t["title"] for t in item["tags", []])
            tasks.append(
                asyncio.gather(
                    _embedding(tags_text),
                    _safety_ok(url),
                    return_exceptions=True
                )
            )
        results = await asyncio.gather(*tasks)
        # aiohttp: requestsと異なり非同期でHTTP通信ができる
        # ClientSession(): aiohttpにおける接続の管理オブジェクト

    for item, res in zip(items, results):
        emb, safe = res
        if not safe:
            continue
        sim = _cosine_similarity(query_emb, emb)
        if sim >= 0.30:
            scored.append((sim, item))

    # 上位 max_images 件を取得
    scored.sort(key=lambda x: x[0], reverse=True)
    selected = scored[:max_images]

    return [
        {
            "url": item["url"]["regular"],
            "alt": item.get("alt_description") or keyword,
            "credit": f"Photo by {item['user']['name']} / Unsplash",
        }
        for _, item in selected
    ]

