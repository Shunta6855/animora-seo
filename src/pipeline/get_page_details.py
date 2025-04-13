# ---------------------------------------------------------------------------------  # 
#                   キーワードに関する過去の指標データを取得する実行コード                    #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from src.config.config import URL_DIR, ARTICLE_DIR

# Chromeドライバ設定
options = Options()
options.add_argument("--headless")  # ヘッドレスモード
options.add_argument("--disable-gpu")  # GPU無効化
options.add_argument("--no-sandbox")  # サンドボックス無効化
options.add_argument("user-agent=Mozilla/5.0")
driver = webdriver.Chrome(options=options)

# ----------------------------------
# URLからページの詳細を取得する関数
# ----------------------------------
def get_page_details(today):
    """
    Get page details from the given URL

    Args:
        today: The date string in the format YYYYMMDD
    """
    os.makedirs(ARTICLE_DIR, exist_ok=True)
    df = pd.read_csv(os.path.join(URL_DIR, f"results_{today}.tsv"), sep="\t")
    scraped = []

    # URLを1つずつ処理
    for i, row in df.iterrows():
        url = row["link"]
        print(f"Scraping URL: {url}")
        
        try:
            driver.get(url)
            time.sleep(2)  # ページが完全に読み込まれるまで待機

            # BeautifulSoupでページを解析
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # 見出しと本文抽出
            headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])]
            paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
            content = "\n".join(headings + paragraphs)
            scraped.append({
                "no": row["no"],
                "url": url,
                "title": row["title"],
                "content": content,
            })
        except Exception as e:
            print(f"Error occurred while scraping {url}: {e}")
            scraped.append({
                "no": row["no"],
                "url": url,
                "title": row["title"],
                "content": "",
            })

    driver.quit()

    df_scraped = pd.DataFrame(scraped)
    df_scraped.to_csv(
        os.path.join(ARTICLE_DIR, f"articles_{today}.tsv"), 
        sep="\t", index=False,
        columns=["no", "url", "title", "content"],
    )

if __name__ == "__main__":
    today = "20250413"
    get_page_details(today)