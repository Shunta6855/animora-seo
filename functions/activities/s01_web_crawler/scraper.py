# ---------------------------------------------------------------------------------  # 
#          　　        SERP上位10記事をスクレイピングするアクティビティ  　                  #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import os, time, uuid, pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from functions.config.settings import URL_DIR, ARTICLE_DIR

# ----------------------------------
# <h2>ごとに本文を切り出して、yieldする関数
# ----------------------------------
def _chunk_h2_sections(soup: BeautifulSoup):
    """
    Chunk the page into sections based on <h2> tags

    Args:
        soup: BeautifulSoup object representing the page content

    Yields:
        A generator of tuples containing the section title and content
    """
    for h2 in soup.find_all("h2"):
        section_paras = []
        # h2の次要素をたどり、次のh2/h1が来るまで収集
        for sib in h2.next_siblings:
            if getattr(sib, "name", None) in ["h1", "h2"]:
                break
            if getattr(sib, "name", None) == "p":
                section_paras.append(sib.get_text(strip=True))
        yield h2.get_text(strip=True), "\n".join(section_paras)
            # yieldで返すことで、メモリに負担をかけずに、データを逐次処理できる
                # return: 一度に全値を返す
                # yield: 値を一つずつ返す

# ----------------------------------
# URL一覧　(=SERP結果) を読み込み、h2セクション単位で dict を返却
# ----------------------------------
def scrape_keyword(keyword: str) -> list[dict]:
    """
    Scrape the keyword and return a list of dictionaries

    Args:
        keyword: The keyword to scrape

    Returns:
        A list of dictionaries containing the section title and content
    """
    urls_df = pd.read_csv(os.path.join(URL_DIR, f"{keyword}_response.tsv"), sep="\t")
    docs = []

    for _, row in urls_df.iterrows():
        url, title = row["link"], row["title"]
        
        # --- Selenium --- #
        opts = Options()
        opts.add_argument("--headless=new") # ヘッドレスモード
        opts.add_argument("--disable-gpu") # GPU無効化
        opts.add_argument("--no-sandbox") # サンドボックス無効化
        opts.add_argument("--disable-dev-shm-usage") # /dev/shmの使用無効化
        opts.add_argument("user-agent=Mozilla/5.0")
        driver = webdriver.Chrome(options=opts)

        try:
            driver.get(url); time.sleep(2) # ページが完全に読み込まれるまで待機
            soup = BeautifulSoup(driver.page_source, "html.parser")
            for h2, body in _chunk_h2_sections(soup):
                if not body: # 空セクションは捨てる
                    continue
                docs.append({
                    "id": str(uuid.uuid4()),
                    "keyword": keyword,
                    "url": url,
                    "title": title,
                    "heading": h2,
                    "content": body,
                })
        finally:
            driver.quit()
    
    return docs
        


        