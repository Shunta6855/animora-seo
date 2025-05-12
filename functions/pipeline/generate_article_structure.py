# ---------------------------------------------------------------------------------  # 
#              スクレイピングした検索上位記事の見出しと本文から、記事構成を生成する              #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import os
import pandas as pd
import google.generativeai as genai

from dotenv import load_dotenv, find_dotenv
from src.utils.markdown import to_markdown
from src.config.config import get_structure_prompt, ARTICLE_DIR, ARTICLE_STRUCTURE_DIR

_ = load_dotenv(find_dotenv())

# APIキーの取得
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# ----------------------------------
# スクレイピングした検索上位記事の見出しと本文から、記事構成を生成する関数
# ----------------------------------
def generate_article_structure(keyword):
    """
    Generate article structure from the scraped article headlines and body text

    Args:
        keyword: The search keyword
    """
    print(f"Start generating article structure for keyword: {keyword}")
    os.makedirs(ARTICLE_STRUCTURE_DIR, exist_ok=True)
    gemini_pro = genai.GenerativeModel("models/gemini-2.0-flash")

    # スクレイピングした記事の読み込み
    df = pd.read_csv(os.path.join(ARTICLE_DIR, f"{keyword}_articles.tsv"), sep="\t")
    all_content = "\n\n".join(df["content"].dropna().astype(str).tolist())

    # 記事構成の生成
    prompt = get_structure_prompt(all_content, keyword)
    response = gemini_pro.generate_content(prompt)
    with open(os.path.join(ARTICLE_STRUCTURE_DIR, f"{keyword}_structure.md"), "w", encoding="utf-8") as f:
        f.write(to_markdown(response.text))

if __name__ == "__main__":
    keyword = "ペットSNS"
    generate_article_structure(keyword)

