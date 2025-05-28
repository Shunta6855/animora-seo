# ---------------------------------------------------------------------------------  # 
#                                   設定ファイル                                       #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv

# ----------------------------------
# パス設定
# ----------------------------------
URL_DIR = "data/result_dfs"
ARTICLE_DIR = "data/article"
ARTICLE_STRUCTURE_DIR = "data/article_structure"
ARTICLE_TEXT_DIR = "data/article_text"
BASE_DIR = Path(__file__).resolve().parent.parent.parent # animalia-seo/
BLOG_SAVE_DIR = BASE_DIR.parent / "animora-homepage" / "src" / "content" / "blog"
IMAGE_SAVE_DIR = BASE_DIR.parent / "animora-homepage" / "public" / "images" / "blog"


# ----------------------------------
# 機密情報の取得
# ----------------------------------
_ = load_dotenv(find_dotenv())

# --------- Creating RAG Index --------- #
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
TITLE_INDEX_NAME = os.getenv("TITLE_INDEX_NAME")
H2_INDEX_NAME = os.getenv("H2_INDEX_NAME")

# --------- Draft Generation --------- #
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")

# --------- Guardrails --------- #
CS_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
CS_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
GROUND_ENDPOINT = CS_ENDPOINT # 同じリージョン内であれば同一

# --------- Image Picker --------- #
AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")
TEXT_EMBEDDING_DEPLOYMENT_NAME = os.getenv("TEXT_EMBEDDING_DEPLOYMENT_NAME")

# Unsplash
UNSPLASH_SEARCH_URL = "https://api.unsplash.com/search/photos"
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

# Pexel
PEXEL_API_KEY = os.getenv("PEXEL_API_KEY")
PEXEL_SEARCH_URL = "https://api.pexels.com/v1/search"

# Pixabay
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
PIXABAY_SEARCH_URL = "https://pixabay.com/api/"

# ----------------------------------
# Animora説明文(RAG用)
# ----------------------------------
animora_doc = [{
    "id": "animora-doc",
    "heading": "animora",
    "content": (
        "animoraは、日々のお題に沿ってペットの写真を投稿できるSNSアプリです。"
        "このアプリは、ペットを飼っているユーザーが日々のタスクを通じて正しい飼育方法を学びつつ、"
        "他の飼い主とのコミュニティを形成することを目的としています。"
        "アプリの主な機能は以下の2つです:"
        "- 画像投稿機能: ユーザーは自由にペットの写真を投稿できるほか、1日1回「登録しているペットに関するお題(タスク)」が送られ、そのテーマに沿った写真を投稿することが求められます。"
        "- コミュニティ機能: テーマフォトコンテスト、ペット飼育に関するQ&A、散歩ルートの共有などの機能を順次実装する予定です。"
    )
}]
