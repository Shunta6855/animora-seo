# ---------------------------------------------------------------------------------  # 
#              スクレイピングした検索上位記事の見出しと本文から、記事構成を生成する              #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import os

from src.config.config import ARTICLE_TEXT_DIR, SAVE_DIR

# ----------------------------------
# 生成した記事をホームページの記事として保存する関数
# ----------------------------------
def save_article(keyword):
    """
    Save the generated article text to the homepage article directory.
    """
    print(f"Start saving article for keyword: {keyword}")
    os.makedirs(SAVE_DIR, exist_ok=True)

    # 記事の取得
    with open(os.path.join(ARTICLE_TEXT_DIR, f"{keyword}_text.md"), "r", encoding="utf-8") as f:
        article = f.read()

    # 記事の保存
    with open(os.path.join(SAVE_DIR, f"{keyword}.md"), "w", encoding="utf-8") as f:
        f.write(article)

if __name__ == "__main__":
    keyword = "ペットSNS"
    save_article(keyword)