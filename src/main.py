# ---------------------------------------------------------------------------------  # 
#                  keyword.csvからキーワードを取得し、記事を生成、保存する                  #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import os
from pathlib import Path
import pandas as pd

from src.pipeline.get_search_response import get_search_response, make_search_results
from src.pipeline.get_page_details import get_page_details
from src.pipeline.generate_article_structure import generate_article_structure
from src.pipeline.generate_article_text import generate_article_text
from src.pipeline.save_article import save_article

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# ----------------------------------
# keyword.csvからキーワードを取得し、記事を生成、保存する
# ----------------------------------
def main():
    """
    Main function to execute the pipeline
    """
    # キーワードの取得
    keyword_df = pd.read_csv(os.path.join(DATA_DIR, "keywords.csv"))
    keywords = keyword_df["keyword"].tolist()

    # 各キーワードに対して処理を実行
    for keyword in keywords[:5]:
        print(f"Start processing keyword: {keyword}")

        # スクレイピングした検索上位記事のURLを取得、tsv形式にして保存
        get_search_response(keyword)
        make_search_results(keyword)

        # スクレイピングした検索上位記事の詳細を取得
        get_page_details(keyword)

        # スクレイピングした検索上位記事の見出しと本文から、記事構成を生成
        generate_article_structure(keyword)

        # スクレイピングした検索上位記事の見出しと本文、生成した記事構成から、記事本文を生成
        generate_article_text(keyword)

        # 生成した記事を保存
        save_article(keyword)

        print(f"Finished processing keyword: {keyword}")

if __name__ == "__main__":
    main()

