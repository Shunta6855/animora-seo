# ---------------------------------------------------------------------------------  # 
#              スクレイピングした検索上位記事の見出しと本文から、記事構成を生成する              #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import os
import pandas as pd
import google.generativeai as genai

from dotenv import load_dotenv, find_dotenv
from src.utils.markdown import to_markdown
from src.config.config import get_text_prompt, ARTICLE_DIR, ARTICLE_STRUCTURE_DIR, ARTICLE_TEXT_DIR

_ = load_dotenv(find_dotenv())

# APIキーの取得
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# ----------------------------------
# スクレイピングした検索上位記事の見出しと本文、生成した記事構成から、記事本文を生成する関数
# ----------------------------------
def generate_article_text(keyword):
    """
    Generate article text from the scraped article headlines and body text, and the generated article structure

    Args:
        keyword: The search keyword
    """
    print(f"Start generating article text for keyword: {keyword}")
    os.makedirs(ARTICLE_TEXT_DIR, exist_ok=True)
    gemini_pro = genai.GenerativeModel("models/gemini-2.0-flash")

    # 記事構成の読み込み
    with open(os.path.join(ARTICLE_STRUCTURE_DIR, f"{keyword}_structure.md"), "r", encoding="utf-8") as f:
        article_structure = f.read()

    # スクレイピングした記事の読み込み
    df = pd.read_csv(os.path.join(ARTICLE_DIR, f"{keyword}_articles.tsv"), sep="\t")
    all_content = "\n\n".join(df["content"].dropna().astype(str).tolist())

    # 記事生成
    prompt = get_text_prompt(all_content, keyword, article_structure)
    response = gemini_pro.generate_content(prompt)
    with open(os.path.join(ARTICLE_TEXT_DIR, f"{keyword}_text.md"), "w", encoding="utf-8") as f:
        f.write(to_markdown(response.text))

if __name__ == "__main__":
    keyword = "ペットSNS"
    generate_article_text(keyword)