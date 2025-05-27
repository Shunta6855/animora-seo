# ---------------------------------------------------------------------------------  # 
#          　　        SERP上位10記事をスクレイピングするアクティビティ  　                  #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import json, time, uuid
from bs4 import BeautifulSoup
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.settings import URL_DIR

# ----------------------------------
# URL一覧　(=SERP結果) を読み込み、h2セクション単位で dict を返却するクラス
# ----------------------------------
class ArticleScraper:
    def __init__(self):
        self.url_dir = Path(URL_DIR)
        self.response_dir = Path("data/response")

    
    def scrape(self, keyword: str) -> list[dict]:
        """
        Scrape the keyword and return a list of dictionaries

        Args:
            keyword: The keyword to scrape

        Returns:
            A list of dictionaries containing the section title and content
        """
        response_filename = self.response_dir / f"{keyword}_response.json"
        with open(response_filename, "r") as response_file:
            response = json.load(response_file)
            docs = []
            titles = []
            if "items" in response and len(response["items"]) > 0:
                for item in response["items"]:
                    # タイトルの取得
                    pagemap = item.get("pagemap", {})
                    metatags = pagemap.get("metatags", [])
                    if metatags:
                        og_title = metatags[0].get("og:title", "")
                        if og_title:
                            titles.append({"id": str(uuid.uuid4()), "title": og_title})
                        else:
                            titles.append({"id": str(uuid.uuid4()), "title": item.get("title", "")})
                    else:
                        titles.append({"id": str(uuid.uuid4()), "title": item.get("title", "")})

                    # H2-本文の取得
                    url = item.get("link", "")
                    driver = self._init_driver()
                    try:
                        driver.get(url); time.sleep(2) # ページが完全に読み込まれるまで待機
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        for h2, body in self._chunk_h2_sections(soup):
                            if not body: # 空セクションは捨てる
                                continue
                            docs.append({
                                "id": str(uuid.uuid4()),
                                "heading": h2,
                                "content": body,
                            })
                    finally:
                        driver.quit()
            return titles, docs
    
    def _init_driver(self) -> webdriver.Chrome:
        """
        Initialize the Chrome driver
        """
        opts = Options()
        opts.add_argument("--headless=new") # ヘッドレスモード
        opts.add_argument("--disable-gpu") # GPU無効化
        opts.add_argument("--no-sandbox") # サンドボックス無効化
        opts.add_argument("--disable-dev-shm-usage") # /dev/shmの使用無効化
        opts.add_argument("user-agent=Mozilla/5.0")
        return webdriver.Chrome(options=opts)
    
    def _chunk_h2_sections(self, soup: BeautifulSoup):
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
        