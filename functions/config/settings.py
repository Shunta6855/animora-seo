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
IMAGE_SAVE_DIR = BASE_DIR.parent / "animora-homepage" / "public" / "images"

# ----------------------------------
# 機密情報の取得
# ----------------------------------
_ = load_dotenv(find_dotenv())

# --------- Creating RAG Index --------- #
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
H2_INDEX_NAME = os.getenv("H2_INDEX_NAME")

# --------- Draft Generation --------- #
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")

# --------- Guardrails --------- #
CS_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
CS_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
GROUND_ENDPOINT = CS_ENDPOINT # 同じリージョン内であれば同一

# --------- Image Picker --------- #
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")
TEXT_EMBEDDING_DEPLOYMENT_NAME = os.getenv("TEXT_EMBEDDING_DEPLOYMENT_NAME")


# ----------------------------------
# Animora説明文(RAG用)
# ----------------------------------
animora_doc = {
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
}


# ----------------------------------
# プロンプト設定
# ----------------------------------
def get_structure_prompt(scraped_text, keyword):
    """
    Generate a prompt for the generative AI model to create an article structure.
    """
    prompt = f"""
        あなたはSEO記事の構成を作成するプロフェッショナルなライターです。
        以下の制約に従って、検索上位の記事情報からSEOに強い記事の見出し構成を作成してください。

        【キーワード】  
        {keyword}

        【参考情報（検索上位記事の見出し・本文）】  
        {scraped_text}

        【出力フォーマット】  
        - Markdown形式
        - 記事構成は見出し(h1, h2, h3)のみを記述
        - h1は1つのみ
        - h2は最大3つ
        - 各h2配下のh3は最大3つまで
        - それ以外の文章や説明、前置き、ポイントなどは一切記述しないこと
        - 出力は以下のような形式にしてください：

        # タイトル(h1)

        ## セクション1(h2)
        ### 小見出し1(h3)
        ### 小見出し2(h3)

        ## セクション2(h2)
        ### 小見出し1(h3)
        ...

        【内容に含める要素】
        - 「animalia」というSNSアプリを他のアプリと並列に、さりげなく紹介してください。
        - animalia は、日々のお題に沿ってペットの写真を投稿できるSNSアプリです
        - このアプリは、ペットを飼っているユーザーが日々のタスクを通じて正しい飼育方法を学びつつ、他の飼い主とのコミュニティを形成することを目的としています。
        - アプリの主な機能は以下の2つです: 
            - 画像投稿機能: ユーザーは自由にペットの写真を投稿できるほか、1日1回「登録しているペットに関するお題(タスク)」が送られ、そのテーマに沿った写真を投稿することが求められます。
            - コミュニティ機能: テーマフォトコンテスト、ペット飼育に関するQ&A、散歩ルートの共有などの機能を順次実装する予定です。
        animaliaの紹介は広告的になりすぎないように注意してください。

        この制約に従って、SEOに強い記事構成(見出し)を生成してください。
        """
    return prompt

def get_text_prompt(structure, scraped_text, keyword):
    """
    Generate a prompt for the generative AI model to create an article text.
    """
    prompt = f"""
        あなたはSEO記事の構成を作成するプロフェッショナルなライターです。
        以下の制約に従って、以下の構成に基づいて参考情報を参照しつつSEOに強い記事本文を作成してください。
        【記事構成】
        {structure}

        【キーワード】  
        {keyword}

        【参考情報（検索上位記事の見出し・本文）】  
        {scraped_text}

        【想定読者】
        20〜40代の犬・猫などのペットを飼っている方で、SNSを通じて情報共有や学習をしたいと考えている人々。

        【執筆方針】 
        - 構成で示した各見出し（#, ##, ###）をそのまま活用し、段落ごとに本文を執筆してください。
        - 各見出しの下には、4〜6文程度の読みやすい文章を記述してください。
        - 出力形式はMarkdownで、コードブロックや注釈は不要です。

        【内容に含める要素】
        - 「animalia」というSNSアプリを他のアプリと並列に、さりげなく紹介してください。
        - animalia は、日々のお題に沿ってペットの写真を投稿できるSNSアプリです
        - このアプリは、ペットを飼っているユーザーが日々のタスクを通じて正しい飼育方法を学びつつ、他の飼い主とのコミュニティを形成することを目的としています。
        - アプリの主な機能は以下の2つです: 
            - 画像投稿機能: ユーザーは自由にペットの写真を投稿できるほか、1日1回「登録しているペットに関するお題(タスク)」が送られ、そのテーマに沿った写真を投稿することが求められます。
            - コミュニティ機能(実装予定): テーマフォトコンテスト、ペット飼育に関するQ&A、散歩ルートの共有などの機能を順次実装する予定です。
        animaliaの紹介は広告的になりすぎないように注意してください。

        【トーンとスタイル】
        - 読み手に寄り添う、親しみやすく信頼感のある語り口
        - SEOを意識した自然なキーワード挿入
        - 無駄な冗長表現は避け、簡潔に

        【禁止事項】
        - 記事の冒頭や末尾に「以下に記事を生成します」などの説明は不要です
        - 出力の後にポイントや解説を加えないでください

        この条件に従って、SEOに強く読者にとって価値のある本文を作成してください。
        """
    return prompt